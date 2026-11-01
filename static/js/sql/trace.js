// Как выполняется запрос: план превращается в последовательность шагов.
//
// Студент пишет запрос сверху вниз — SELECT, FROM, WHERE, — а база выполняет его совсем
// в другом порядке: сначала читает таблицы, потом отбирает, соединяет, группирует, и
// только в конце выбирает столбцы. Это самое частое непонимание на первых занятиях, и
// обычным результатом его не показать: таблица на выходе не говорит, как она получилась.
//
// Шаги строятся не из разбора текста запроса, а из настоящего плана: то, что здесь
// показано, база действительно сделала, с настоящими числами строк. Обход идёт от
// листьев к корню — в этом порядке данные и текут.
//
// Промежуточные строки план не хранит, поэтому они запрашиваются отдельно, запросом,
// собранным из условий самого плана. Такой запрос — реконструкция, и она может не
// совпасть с тем, что было на деле. Поэтому показывается она только после сверки: число
// строк обязано совпасть с тем, что отчитался план. Не совпало — на шаге остаются одни
// числа. Придуманная таблица в учебном инструменте хуже, чем её отсутствие.
//
// Всё выполняется в транзакции с откатом: можно посмотреть и на UPDATE, не меняя базу.

import { pluralRu, rowsLabel } from "../plural.js";
import { parsePlan } from "./plan.js";

const SAMPLE = 8; // сколько строк показывать на шаге
const BUDGET_MS = 1500; // сколько времени готовы потратить на примеры строк

const SCANS = new Set(["Seq Scan", "Index Scan", "Index Only Scan", "Bitmap Heap Scan"]);
const JOINS = new Set(["Hash Join", "Merge Join", "Nested Loop"]);

// Служебные узлы: данных они не меняют и студенту только мешали бы. Хеш-таблица и
// индекс упоминаются в описании соединения и чтения, к которым относятся.
const TRANSPARENT = new Set([
  "Hash",
  "Materialize",
  "Memoize",
  "Gather",
  "Gather Merge",
  "Bitmap Index Scan",
  "BitmapAnd",
  "BitmapOr",
]);

// Узлы, для которых промежуточные строки не восстановить: они остаются с числами.
// Подпись, описание и короткое имя для цепочки шагов.
const GENERIC = {
  "Subquery Scan": ["Берём результат подзапроса", "Подзапрос уже посчитан — дальше с ним работают как с таблицей.", "подзапрос"],
  "CTE Scan": ["Читаем результат WITH", "Именованный подзапрос из WITH посчитан — дальше с ним работают как с таблицей.", "WITH"],
  "Function Scan": ["Вызываем функцию", "Строки даёт функция из FROM, например generate_series.", "функция"],
  "Values Scan": ["Читаем список VALUES", "Строки заданы прямо в тексте запроса.", "VALUES"],
  Append: ["Складываем наборы строк", "Результаты частей идут друг за другом, как при UNION ALL.", "UNION"],
  "Merge Append": ["Складываем наборы строк", "Результаты частей сливаются с сохранением порядка.", "UNION"],
  SetOp: ["Сравниваем наборы строк", "Так работают INTERSECT и EXCEPT.", "наборы"],
  "Recursive Union": ["Повторяем рекурсивную часть", "WITH RECURSIVE повторяется, пока появляются новые строки.", "рекурсия"],
  Result: ["Вычисляем значения", "Для этого не нужно читать таблицу: значения считаются сразу.", "значения"],
  ProjectSet: ["Разворачиваем функцию в строки", "Функция в SELECT возвращает набор, и каждая строка размножается.", "функция"],
  LockRows: ["Блокируем строки", "Так работает SELECT ... FOR UPDATE: строки закрыты для других транзакций.", "блокировка"],
};

/** Ошибка, которую можно показать как есть: это объяснение, а не сбой. */
export class TraceError extends Error {}

const q = (name) => '"' + String(name).replace(/"/g, '""') + '"';

function total(node) {
  return Math.round((node["Actual Rows"] || 0) * (node["Actual Loops"] || 1));
}

function firstChild(node) {
  const plans = node.Plans || [];
  return plans.find((p) => p["Parent Relationship"] === "Outer") || plans[0] || null;
}

/** Настоящий источник данных: сквозь служебные узлы. */
function real(node) {
  let current = node;
  while (current && TRANSPARENT.has(current["Node Type"]) && (current.Plans || []).length === 1) {
    current = current.Plans[0];
  }
  return current;
}

function joinSides(node) {
  const plans = node.Plans || [];
  return [
    plans.find((p) => p["Parent Relationship"] === "Outer") || plans[0],
    plans.find((p) => p["Parent Relationship"] === "Inner") || plans[1],
  ];
}

function walk(node, visit) {
  for (const child of node.Plans || []) walk(child, visit);
  visit(node);
}

function tablesUnder(node) {
  const out = [];
  walk(node, (n) => {
    if (n["Relation Name"] && !out.includes(n["Relation Name"])) out.push(n["Relation Name"]);
  });
  return out;
}

function sideLabel(node) {
  const names = tablesUnder(node);
  return names.length ? names.join(" + ") : "промежуточного результата";
}

// --- Текст условий ------------------------------------------------------------

/** Слово целиком. `\b` здесь не годится: он не считает кириллицу буквами. */
function wordPattern(word, suffix = "") {
  const literal = String(word).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return new RegExp(`(?<![\\p{L}\\d_])${literal}${suffix || "(?![\\p{L}\\d_])"}`, "gu");
}

/** Условие для показа: без приведений типов, которые дописал планировщик, и лишних скобок. */
function readable(expr, alias) {
  let text = String(expr || "")
    .replace(
      /::(?:character varying|double precision|timestamp (?:with|without) time zone|[A-Za-z_]\w*)(?:\[\])?/g,
      "",
    )
    .trim();
  if (alias) text = text.replace(wordPattern(alias, "\\."), "");
  while (text.startsWith("(") && text.endsWith(")") && balanced(text.slice(1, -1))) {
    text = text.slice(1, -1).trim();
  }
  return text;
}

function balanced(text) {
  let depth = 0;
  for (const ch of text) {
    if (ch === "(") depth += 1;
    if (ch === ")") depth -= 1;
    if (depth < 0) return false;
  }
  return depth === 0;
}

const IDENT = String.raw`"?([\p{L}_][\p{L}\d_]*)"?`;

function columnRefs(expr, aliases) {
  // Строковые значения вырезаются: в 'a.b' точка — не обращение к столбцу.
  const clean = String(expr || "").replace(/'(?:[^']|'')*'/g, "''");
  const out = [];
  for (const m of clean.matchAll(new RegExp(`${IDENT}\\.${IDENT}`, "gu"))) {
    const table = aliases.get(m[1]);
    if (table) out.push({ table, column: m[2] });
  }
  return out;
}

/** Пары столбцов из условия соединения: по ним находится линия на диаграмме. */
function joinLinks(expr, aliases) {
  const clean = String(expr || "").replace(/'(?:[^']|'')*'/g, "''");
  const out = [];
  const pattern = new RegExp(`${IDENT}\\.${IDENT}\\s*=\\s*${IDENT}\\.${IDENT}`, "gu");
  for (const m of clean.matchAll(pattern)) {
    const srcTable = aliases.get(m[1]);
    const dstTable = aliases.get(m[3]);
    if (srcTable && dstTable) out.push({ srcTable, srcCol: m[2], dstTable, dstCol: m[4] });
  }
  return out;
}

function shortName(expr) {
  const plain = new RegExp(`^${IDENT}\\.${IDENT}$`, "u").exec(expr);
  return plain ? plain[2] : readable(expr);
}

function format(value) {
  if (value === null || value === undefined) return "NULL";
  if (value instanceof Date) return value.toISOString().replace("T00:00:00.000Z", "");
  return typeof value === "object" ? JSON.stringify(value) : String(value);
}

// --- Промежуточные строки: запрос из условий плана ------------------------------

function scanConds(node) {
  return [node.Filter, node["Index Cond"], node["Recheck Cond"]].filter(Boolean);
}

function relation(node) {
  return `${q(node.Schema || "public")}.${q(node["Relation Name"])} AS ${q(node.Alias || node["Relation Name"])}`;
}

/** Части SELECT, дающего те же строки, что и узел, либо null, если восстановить нельзя. */
function source(node, ctx) {
  const type = node["Node Type"];
  if (SCANS.has(type)) {
    return node["Relation Name"] ? { from: relation(node), where: scanConds(node) } : null;
  }
  if (TRANSPARENT.has(type)) {
    return (node.Plans || []).length === 1 ? source(node.Plans[0], ctx) : null;
  }
  if (JOINS.has(type)) return joinSource(node, ctx);

  const child = firstChild(node);
  const src = child && source(child, ctx);
  if (!src) return null;

  if (type === "Aggregate" || type === "Group") {
    if (src.grouped || src.limit != null) return null;
    return { ...src, grouped: true, groupBy: node["Group Key"] || [], having: node.Filter || null };
  }
  if (type === "Sort" || type === "Incremental Sort") {
    return src.limit != null ? null : { ...src, orderBy: node["Sort Key"] || [] };
  }
  if (type === "Limit") {
    // Смещения в плане нет, и `LIMIT` без него показал бы не те строки.
    return ctx.hasOffset ? null : { ...src, limit: total(node) };
  }
  if (type === "Unique") return { ...src, distinct: true };
  return null;
}

function joinSource(node, ctx) {
  const [outer, inner] = joinSides(node);
  const left = source(outer, ctx);
  const right = source(inner, ctx);
  if (!left || !right || left.grouped || right.grouped || left.limit != null || right.limit != null) {
    return null;
  }

  const on = [node["Hash Cond"], node["Merge Cond"], node["Join Filter"]].filter(Boolean);
  const where = [];
  const type = node["Join Type"] || "Inner";
  // Условие на внешней стороне внешнего соединения обязано быть в ON: в WHERE оно
  // выбросило бы строки без пары, ради которых LEFT JOIN и пишут.
  if (type === "Inner") where.push(...left.where, ...right.where);
  else if (type === "Left") {
    on.push(...right.where);
    where.push(...left.where);
  } else if (type === "Right") {
    on.push(...left.where);
    where.push(...right.where);
  } else if (type !== "Full" || left.where.length || right.where.length) {
    return null; // Semi и Anti: это EXISTS и NOT EXISTS, через JOIN их не выразить
  }
  if (node.Filter) where.push(node.Filter);

  const keyword = { Inner: "JOIN", Left: "LEFT JOIN", Right: "RIGHT JOIN", Full: "FULL JOIN" }[type];
  const rightFrom = right.joined ? `(${right.from})` : right.from;
  return {
    from: `${left.from} ${keyword} ${rightFrom} ON ${on.length ? on.join(" AND ") : "TRUE"}`,
    where,
    joined: true,
  };
}

function selectSql(src, list) {
  let sql = `SELECT ${src.distinct ? "DISTINCT " : ""}${list} FROM ${src.from}`;
  if (src.where.length) sql += ` WHERE ${src.where.join(" AND ")}`;
  if (src.grouped && src.groupBy.length) sql += ` GROUP BY ${src.groupBy.join(", ")}`;
  if (src.having) sql += ` HAVING ${src.having}`;
  if (src.orderBy && src.orderBy.length) sql += ` ORDER BY ${src.orderBy.join(", ")}`;
  if (src.limit != null) sql += ` LIMIT ${src.limit}`;
  return sql;
}

/** Совпало ли число строк с планом: всего или за один проход вложенного цикла. */
function matches(count, node) {
  return count === total(node) || Math.abs(count - (node["Actual Rows"] || 0)) <= 0.5;
}

function tableSample(res, count) {
  const columns = res.fields.map((f) => f.name);
  return {
    columns,
    rows: res.rows.map((row) => ({ cells: columns.map((c) => format(row[c])) })),
    total: count,
  };
}

/** Строки на выходе узла — только если реконструкция сошлась с планом по числу строк. */
function outputLoader(node, ctx) {
  const src = source(node, ctx);
  const outputs = node.Output || [];
  if (!src || !outputs.length) return null;

  return async (probe) => {
    const inner = selectSql(src, outputs.map((expr, i) => `${expr} AS c${i}`).join(", "));
    const counted = await probe(`SELECT count(*)::int AS n FROM (${inner}) t`);
    if (!counted) return null;

    // Сортировка под LIMIT отдаёт наверх только верхушку: строк в реконструкции больше,
    // чем в плане, и это верно — у отсортированного набора верхушка та же самая.
    const count = counted.rows[0].n;
    const top = /Sort$/.test(node["Node Type"]) && count > total(node) ? total(node) : null;
    if (top === null && !matches(count, node)) return null;

    const res = await probe(`SELECT * FROM (${inner}) t LIMIT ${Math.min(SAMPLE, top ?? SAMPLE)}`);
    if (!res) return null;
    return {
      columns: outputs.map(shortName),
      rows: res.rows.map((row) => ({ cells: outputs.map((_, i) => format(row[`c${i}`])) })),
      total: top ?? count,
    };
  };
}

/**
 * Строки таблицы с отметкой, прошли ли они условие.
 * Берётся начало таблицы как есть: так видно, что проверяется каждая строка подряд.
 * Если в это начало не попала ни одна подходящая — добираются отдельно, иначе студент
 * увидел бы одни отброшенные строки и решил, что не подошло ничего.
 */
function filterLoader(node, base, filter) {
  const alias = q(node.Alias || node["Relation Name"]);
  const from = relation(node);
  const where = base ? ` WHERE ${base}` : "";

  return async (probe) => {
    const passed = `${filter}${base ? ` AND ${base}` : ""}`;
    const counted = await probe(`SELECT count(*)::int AS n FROM ${from} WHERE ${passed}`);
    if (!counted || !matches(counted.rows[0].n, node)) return null;

    const flagged = `SELECT ${alias}.*, COALESCE(${filter}, FALSE) AS dataedu_keep FROM ${from}`;
    let res = await probe(`${flagged}${where} LIMIT ${SAMPLE}`);
    if (!res) return null;
    let rows = res.rows;
    if (counted.rows[0].n > 0 && !rows.some((row) => row.dataedu_keep)) {
      const kept = await probe(`${flagged} WHERE ${passed} LIMIT 5`);
      if (!kept) return null;
      rows = [...kept.rows, ...rows.slice(0, 3)];
      res = kept;
    }

    const columns = res.fields.map((f) => f.name).filter((name) => name !== "dataedu_keep");
    return {
      columns,
      marked: true,
      rows: rows.map((row) => ({
        cells: columns.map((c) => format(row[c])),
        state: row.dataedu_keep ? "kept" : "dropped",
      })),
      total: counted.rows[0].n,
    };
  };
}

// --- Шаги ---------------------------------------------------------------------

function bitmapIndexName(node) {
  let name = null;
  walk(node, (n) => {
    if (n["Node Type"] === "Bitmap Index Scan" && n["Index Name"]) name = n["Index Name"];
  });
  return name;
}

function scanSteps(node, ctx) {
  const table = node["Relation Name"];
  const alias = node.Alias || table;
  const type = node["Node Type"];
  const kept = total(node);
  const loops = node["Actual Loops"] || 1;
  const removed = Math.round((node["Rows Removed by Filter"] || 0) * loops);
  const before = kept + removed;
  const indexName = node["Index Name"] || bitmapIndexName(node);
  const indexCond = node["Index Cond"] || node["Recheck Cond"];
  const filter = node.Filter;

  const common = { active: [table], table, alias, tables: [table], chip: table };
  const refs = (expr) => columnRefs(expr, ctx.aliases);
  const steps = [];

  if (indexName) {
    const by = indexCond ? ` по условию ${readable(indexCond, alias)}` : "";
    const onlyIndex = type === "Index Only Scan"
      ? " Все нужные столбцы лежат в самом индексе, поэтому таблицу открывать незачем."
      : "";
    const repeat = loops > 1
      ? ` Поиск повторён ${loops} ${pluralRu(loops, "раз", "раза", "раз")} — по разу на каждую строку другой стороны соединения.`
      : "";
    steps.push({
      ...common,
      kind: "index",
      title: `Ищем в таблице ${table} по индексу`,
      text:
        `Индекс ${indexName} ведёт сразу к нужным строкам${by}, поэтому таблица не просматривается целиком. ` +
        `Найдено: ${rowsLabel(before)}.${onlyIndex}${repeat}`,
      rowsIn: null,
      rowsOut: before,
      columns: refs(indexCond),
      clauses: ["FROM", "JOIN", "WHERE"],
      load: indexCond && !filter ? outputLoader(node, ctx) : null,
    });
  } else {
    steps.push({
      ...common,
      kind: "read",
      title: `Читаем таблицу ${table}`,
      text:
        "Seq Scan: база просматривает таблицу строка за строкой" +
        (filter ? " — индекса под это условие нет или он здесь не выгоден" : "") +
        `. Прочитано: ${rowsLabel(before)}.`,
      rowsIn: null,
      rowsOut: before,
      columns: (node.Output || []).flatMap(refs),
      clauses: ["FROM", "JOIN"],
      load: async (probe) => {
        const res = await probe(`SELECT ${q(alias)}.* FROM ${relation(node)} LIMIT ${SAMPLE}`);
        return res && tableSample(res, before);
      },
    });
  }

  if (filter) {
    const dropped = removed;
    steps.push({
      ...common,
      kind: "filter",
      chip: "WHERE",
      title: "Оставляем строки по условию",
      text:
        `Каждая строка проверяется на условие ${readable(filter, alias)}. ` +
        `Подошло: ${rowsLabel(kept)}, отброшено: ${rowsLabel(dropped)}.`,
      note:
        type === "Seq Scan" && dropped >= 1000 && dropped > kept * 5
          ? `Прочитано: ${rowsLabel(before)}, а нужно: ${rowsLabel(kept)}. Это условие просится в индекс.`
          : null,
      rowsIn: before,
      rowsOut: kept,
      columns: refs(filter),
      clauses: ["WHERE", "JOIN"],
      load: filterLoader(node, indexCond, filter),
    });
  }
  return steps;
}

function joinStep(node, ctx) {
  const [outerNode, innerNode] = joinSides(node);
  const outer = real(outerNode);
  const inner = real(innerNode);
  const outerName = sideLabel(outer);
  const innerName = sideLabel(inner);
  const nOuter = total(outer);
  const nInner = total(inner);
  const out = total(node);
  const type = node["Node Type"];
  const joinType = node["Join Type"] || "Inner";

  // В цикле с индексом условие соединения записано не в самом узле, а в поиске по индексу.
  let innerCond = null;
  walk(innerNode, (n) => {
    if (n["Index Cond"] && !innerCond) innerCond = n["Index Cond"];
  });
  const cond = node["Hash Cond"] || node["Merge Cond"] || node["Join Filter"] || innerCond;
  const on = cond ? readable(cond) : null;

  const how = {
    "Hash Join": `Hash Join: по ${innerName} (${rowsLabel(nInner)}) строится хеш-таблица ключей, а затем каждая строка ${outerName} (${rowsLabel(nOuter)}) находит в ней пару сразу, без перебора.`,
    "Merge Join": `Merge Join: обе стороны отсортированы по ключу, и база идёт по ним одновременно, как по двум спискам.`,
    "Nested Loop": `Nested Loop: для каждой строки ${outerName} (${rowsLabel(nOuter)}) база ищет пару в ${innerName}. Это дёшево, пока внешних строк немного.`,
  }[type];

  const notes = [];
  const kinds = {
    Left: "LEFT JOIN: строки слева сохраняются, даже если пары нет — вместо значений справа будет NULL.",
    Right: "Внешнее соединение: строки одной стороны сохраняются, даже если пары нет — вместо значений другой будет NULL.",
    Full: "FULL JOIN: сохраняются строки обеих сторон, даже без пары.",
    Semi: "Это проверка существования (EXISTS или IN): строка остаётся, если пара есть, но столбцы другой таблицы к ней не добавляются.",
    Anti: "Это NOT EXISTS: остаются только строки, у которых пары нет.",
  };
  if (kinds[joinType]) notes.push(kinds[joinType]);
  if (!cond) notes.push("Условия нет: каждая строка соединяется с каждой — это декартово произведение.");

  const links = joinLinks(cond, ctx.aliases);
  const offKey = links.filter(
    (l) =>
      !ctx.schema.links.some(
        (fk) =>
          (fk.src === l.srcTable && fk.srcCol === l.srcCol && fk.dst === l.dstTable && fk.dstCol === l.dstCol) ||
          (fk.src === l.dstTable && fk.srcCol === l.dstCol && fk.dst === l.srcTable && fk.dstCol === l.srcCol),
      ),
  );
  if (offKey.length) {
    notes.push("Внешнего ключа между этими столбцами нет: база соединит строки, но не следит, что такие пары вообще имеют смысл.");
  }

  return {
    kind: "join",
    chip: "JOIN",
    title: `Соединяем ${outerName} и ${innerName}`,
    text: `${how}${on ? ` Условие: ${on}.` : ""} Получилось: ${rowsLabel(out)}.`,
    note: notes.join(" ") || null,
    // Две стороны показываются порознь: сумма читалась бы как «было 12 строк, стало 9»,
    // будто соединение что-то отбросило.
    inputs: [nOuter, nInner],
    rowsIn: nOuter + nInner,
    rowsOut: out,
    active: [...tablesUnder(outer), ...tablesUnder(inner)],
    tables: tablesUnder(node),
    columns: columnRefs(cond, ctx.aliases),
    links,
    innerTable: tablesUnder(inner)[0] || null,
    clauses: ["JOIN", "WHERE", "FROM"],
    load: outputLoader(node, ctx),
  };
}

function groupStep(node, ctx) {
  const child = real(firstChild(node));
  const before = child ? total(child) : 0;
  const out = total(node);
  const keys = node["Group Key"] || [];
  const aggregates = (node.Output || [])
    .filter((expr) => /\(/.test(expr))
    .map((expr) => readable(expr));
  const removed = Math.round((node["Rows Removed by Filter"] || 0) * (node["Actual Loops"] || 1));

  // DISTINCT планировщик часто выполняет той же группировкой. Студент её не писал, и
  // подпись GROUP BY сбила бы с толку: называем так, как записано в запросе.
  if (ctx.hasDistinct && !ctx.hasGroupBy) {
    return {
      kind: "distinct",
      chip: "DISTINCT",
      title: "Убираем повторяющиеся строки",
      text: `Одинаковые строки схлопываются в одну. Было: ${rowsLabel(before)}, осталось: ${rowsLabel(out)}.`,
      rowsIn: before,
      rowsOut: out,
      active: [],
      tables: tablesUnder(node),
      columns: keys.flatMap((expr) => columnRefs(expr, ctx.aliases)),
      clauses: ["SELECT"],
      load: outputLoader(node, ctx),
    };
  }

  const counting = aggregates.length ? ` Для каждой считается: ${aggregates.join(", ")}.` : "";
  const having = node.Filter
    ? ` Условие HAVING ${readable(node.Filter)} отбросило групп: ${removed}.`
    : "";

  const text = keys.length
    ? `Строки с одинаковым значением ${keys.map((k) => readable(k)).join(", ")} складываются в одну группу. ` +
      `Было: ${rowsLabel(before)}, получилось: ${out} ${pluralRu(out, "группа", "группы", "групп")}.${counting}${having}`
    : `Все строки сворачиваются в одну с итогом: ${aggregates.join(", ") || "агрегат"}. Было: ${rowsLabel(before)}.${having}`;

  return {
    kind: "group",
    chip: keys.length ? "GROUP BY" : "итог",
    title: keys.length ? `Группируем по ${keys.map((k) => readable(k)).join(", ")}` : "Считаем итог по всем строкам",
    text,
    rowsIn: before,
    rowsOut: out,
    active: [],
    tables: tablesUnder(node),
    columns: [...keys, ...(node.Output || [])].flatMap((expr) => columnRefs(expr, ctx.aliases)),
    clauses: keys.length ? ["GROUP BY", "HAVING"] : ["SELECT"],
    load: outputLoader(node, ctx),
  };
}

/** Ключ сортировки словами: «(round(avg(s.xp), 0)) DESC» — это «round(…), по убыванию». */
function sortKey(expr) {
  const match = /^(.*?)(?:\s+(ASC|DESC))?(?:\s+NULLS (?:FIRST|LAST))?$/s.exec(String(expr).trim());
  const key = readable(match[1]);
  return match[2] === "DESC" ? `${key} (по убыванию)` : key;
}

function sortStep(node, ctx) {
  const keys = (node["Sort Key"] || []).map(sortKey);
  const child = real(firstChild(node));
  const before = child ? total(child) : total(node);
  const out = total(node);
  const method = node["Sort Method"] || "";
  let note = null;
  if (/top-N/i.test(method)) {
    note = "Нужны только первые строки, поэтому база не сортирует всё целиком, а держит в памяти лучшие (top-N heapsort).";
  } else if (/external/i.test(method)) {
    note = "Сортировка не поместилась в память и ушла на диск — это заметно медленнее.";
  }
  return {
    kind: "sort",
    chip: "ORDER BY",
    title: `Сортируем по ${keys.join(", ")}`,
    text:
      out < before
        ? `Отсортировано: ${rowsLabel(before)}, дальше передано: ${rowsLabel(out)} — выше в плане стоит LIMIT.`
        : `Строк столько же, сколько было (${rowsLabel(before)}), меняется только их порядок.`,
    note,
    rowsIn: before,
    rowsOut: out,
    active: [],
    tables: tablesUnder(node),
    columns: (node["Sort Key"] || []).flatMap((k) => columnRefs(k, ctx.aliases)),
    clauses: ["ORDER BY"],
    load: outputLoader(node, ctx),
  };
}

function limitStep(node, ctx) {
  const out = total(node);
  const child = real(firstChild(node));
  return {
    kind: "limit",
    chip: "LIMIT",
    title: "Обрезаем результат по LIMIT",
    text: `Как только нужное число строк набрано, база останавливается: то, что ниже в плане, дальше не выполняется. Осталось: ${rowsLabel(out)}.`,
    rowsIn: child ? total(child) : null,
    rowsOut: out,
    active: [],
    tables: tablesUnder(node),
    columns: [],
    clauses: ["LIMIT", "OFFSET"],
    load: outputLoader(node, ctx),
  };
}

function uniqueStep(node, ctx) {
  const child = real(firstChild(node));
  const before = child ? total(child) : null;
  return {
    kind: "distinct",
    chip: "DISTINCT",
    title: "Убираем повторяющиеся строки",
    text: `Одинаковые строки схлопываются в одну. Осталось: ${rowsLabel(total(node))}.`,
    rowsIn: before,
    rowsOut: total(node),
    active: [],
    tables: tablesUnder(node),
    columns: [],
    clauses: ["SELECT"],
    load: outputLoader(node, ctx),
  };
}

function windowStep(node, ctx) {
  const out = total(node);
  return {
    kind: "window",
    chip: "OVER",
    title: "Считаем оконную функцию",
    text: `В отличие от GROUP BY, окно не сворачивает строки: к каждой добавляется значение, посчитанное по соседним. Строк по-прежнему: ${out}.`,
    rowsIn: out,
    rowsOut: out,
    active: [],
    tables: tablesUnder(node),
    columns: (node.Output || []).flatMap((expr) => columnRefs(expr, ctx.aliases)),
    clauses: ["SELECT"],
    load: null,
  };
}

function modifyStep(node) {
  const operation = node.Operation || "";
  const table = node["Relation Name"];
  const child = real(firstChild(node));
  const rows = child ? total(child) : 0;
  const titles = {
    Insert: `Добавляем строки в ${table}`,
    Update: `Обновляем строки в ${table}`,
    Delete: `Удаляем строки из ${table}`,
  };
  return {
    kind: "modify",
    chip: operation === "Insert" ? "INSERT" : operation === "Delete" ? "DELETE" : "UPDATE",
    title: titles[operation] || `Изменяем ${table}`,
    text: `Затронуто: ${rowsLabel(rows)}. Здесь изменение показано и сразу отменено — база осталась как была. Чтобы применить его, нажмите «Выполнить».`,
    rowsIn: rows,
    rowsOut: rows,
    active: table ? [table] : [],
    tables: table ? [table] : [],
    columns: [],
    clauses: ["UPDATE", "SET", "DELETE", "INSERT", "VALUES"],
    load: null,
  };
}

function genericStep(node) {
  const type = node["Node Type"];
  const [title, text, chip] = GENERIC[type] || [`Этап плана: ${type}`, "", type];
  const rows = total(node);
  return {
    kind: "other",
    chip,
    title,
    text: `${text} На выходе: ${rowsLabel(rows)}.`.trim(),
    rowsIn: null,
    rowsOut: rows,
    active: tablesUnder(node).slice(0, 1),
    tables: tablesUnder(node),
    columns: [],
    clauses: [],
    load: null,
  };
}

function stepsFor(node, ctx) {
  const type = node["Node Type"];
  if (SCANS.has(type)) return scanSteps(node, ctx);
  if (JOINS.has(type)) return [joinStep(node, ctx)];
  if (type === "Aggregate" || type === "Group") return [groupStep(node, ctx)];
  if (type === "Sort" || type === "Incremental Sort") return [sortStep(node, ctx)];
  if (type === "Limit") return [limitStep(node, ctx)];
  if (type === "Unique") return [uniqueStep(node, ctx)];
  if (type === "WindowAgg") return [windowStep(node, ctx)];
  if (type === "ModifyTable") return [modifyStep(node)];
  return [genericStep(node)];
}

// --- Подсветка частей запроса -----------------------------------------------------

const CLAUSE = new RegExp(
  "\\b(select|from|(?:(?:inner|left|right|full|cross)\\s+(?:outer\\s+)?)?join|where|group\\s+by|having|" +
    "order\\s+by|limit|offset|insert\\s+into|values|update|set|delete\\s+from|returning)\\b",
  "gi",
);

/**
 * Части запроса верхнего уровня. Строки, комментарии и скобки заглушаются пробелами:
 * слово from внутри строки или подзапроса — не начало раздела FROM. Длины совпадают,
 * поэтому найденные позиции верны и для исходного текста.
 */
function clauseSpans(sql) {
  let masked = "";
  let depth = 0;
  let i = 0;
  while (i < sql.length) {
    const ch = sql[i];
    if (ch === "'" || ch === '"') {
      let j = i + 1;
      while (j < sql.length && (sql[j] !== ch || sql[j + 1] === ch)) j += sql[j] === ch ? 2 : 1;
      masked += " ".repeat(Math.min(j + 1, sql.length) - i);
      i = j + 1;
    } else if (sql.startsWith("--", i)) {
      const end = sql.indexOf("\n", i);
      const stop = end < 0 ? sql.length : end;
      masked += " ".repeat(stop - i);
      i = stop;
    } else if (sql.startsWith("/*", i)) {
      const end = sql.indexOf("*/", i + 2);
      const stop = end < 0 ? sql.length : end + 2;
      masked += " ".repeat(stop - i);
      i = stop;
    } else {
      if (ch === "(") depth += 1;
      masked += depth > 0 ? " " : ch;
      if (ch === ")") depth = Math.max(0, depth - 1);
      i += 1;
    }
  }

  const marks = [...masked.matchAll(CLAUSE)];
  return marks.map((m, n) => {
    const word = m[1].toUpperCase().replace(/\s+/g, " ");
    const name = word.endsWith("JOIN") ? "JOIN" : word.split(" ")[0] === "GROUP" ? "GROUP BY"
      : word.split(" ")[0] === "ORDER" ? "ORDER BY" : word.split(" ")[0];
    const end = n + 1 < marks.length ? marks[n + 1].index : sql.length;
    return { name, start: m.index, end, text: sql.slice(m.index, end) };
  });
}

/** Какие части запроса относятся к шагу: первая подходящая по порядку из `clauses`. */
function marksFor(step, spans, sql) {
  const names = step.clauses || [];
  const mentions = (span, word) => Boolean(word) && span.text.search(wordPattern(word)) >= 0;

  if (step.kind === "read" || step.kind === "index") {
    const places = ["FROM", "JOIN", "UPDATE", "DELETE"];
    const own = spans.filter(
      (s) => places.includes(s.name) && (mentions(s, step.table) || mentions(s, step.alias)),
    );
    if (own.length) return own.slice(0, 1);
    // Таблица стоит внутри подзапроса или WITH: на верхнем уровне её нет, и подсвечивать
    // чужой FROM было бы неправдой. Отмечаем сам её FROM, где бы он ни был.
    const literal = String(step.table).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const inside = new RegExp(`\\bfrom\\s+(?:\\w+\\.)?"?${literal}"?`, "iu").exec(sql);
    return inside ? [{ start: inside.index, end: inside.index + inside[0].length }] : [];
  }
  if (step.kind === "join") {
    const own = spans.filter((s) => s.name === "JOIN" && mentions(s, step.innerTable));
    if (own.length) return own;
  }
  if (step.kind === "group" || step.kind === "modify") {
    return spans.filter((s) => names.includes(s.name));
  }
  for (const name of names) {
    const found = spans.filter((s) => s.name === name);
    if (found.length) return found;
  }
  return [];
}

// --- Сборка -------------------------------------------------------------------

/**
 * Откатываемая песочница. Студент мог сам открыть транзакцию в редакторе (курс про
 * транзакции именно этому и учит), и обычный ROLLBACK снёс бы его работу, поэтому
 * внутри чужой транзакции откат идёт к точке сохранения.
 */
async function sandbox(db, work) {
  let own = false;
  try {
    await db.exec("SAVEPOINT dataedu_trace");
  } catch (e) {
    if (/aborted/i.test(e.message || "")) {
      throw new TraceError(
        "Транзакция, начатая в редакторе, прервана ошибкой. Выполните ROLLBACK; — и попробуйте снова.",
      );
    }
    own = true; // транзакции нет: SAVEPOINT вне её запрещён, и это нормально
  }
  if (own) await db.exec("BEGIN");
  try {
    return await work();
  } finally {
    await db.exec(
      own ? "ROLLBACK" : "ROLLBACK TO SAVEPOINT dataedu_trace; RELEASE SAVEPOINT dataedu_trace",
    );
  }
}

/** Запрос, ошибка которого не прерывает транзакцию: восстановить удаётся не всё. */
function prober(db) {
  return async (sql) => {
    await db.exec("SAVEPOINT dataedu_probe");
    try {
      const res = await db.query(sql);
      await db.exec("RELEASE SAVEPOINT dataedu_probe");
      return res;
    } catch {
      await db.exec("ROLLBACK TO SAVEPOINT dataedu_probe; RELEASE SAVEPOINT dataedu_probe");
      return null;
    }
  };
}

function statementKind(sql) {
  const text = sql.replace(/^(?:\s+|--[^\n]*(?:\n|$)|\/\*[\s\S]*?\*\/)+/, "");
  const match = /^(select|with|table|values|insert|update|delete)\b/i.exec(text);
  return match ? match[1].toLowerCase() : null;
}

/**
 * Построить шаги выполнения запроса.
 * @returns {Promise<{sql: string, steps: object[], executionMs: number, planningMs: number}>}
 * @throws {TraceError} если показать выполнение этой команды нельзя
 */
export async function buildTrace(db, sql, schema) {
  const kind = statementKind(sql);
  if (!kind) {
    throw new TraceError(
      "Пошаговый показ работает для SELECT, INSERT, UPDATE и DELETE. CREATE, DROP и другие " +
        "команды меняют саму схему: их результат видно на диаграмме после «Выполнить».",
    );
  }
  const dml =
    kind === "insert" ||
    kind === "update" ||
    kind === "delete" ||
    (kind === "with" && /\b(?:insert|update|delete)\b/i.test(sql));

  let plan;
  let result = null;
  await sandbox(db, async () => {
    try {
      const res = await db.query(`EXPLAIN (ANALYZE, VERBOSE, BUFFERS, FORMAT JSON) ${sql}`);
      plan = parsePlan(res.rows);
      // Сам запрос нужен ради итоговых строк. Изменяющий выполнять второй раз нельзя:
      // он только что отработал под ANALYZE, и строки вставились бы дважды.
      if (!dml) result = await db.query(sql);
    } catch (e) {
      if (/multiple commands/i.test(e.message || "")) {
        throw new TraceError(
          "В поле несколько команд, а показать выполнение можно только для одной. Оставьте нужную.",
        );
      }
      throw e;
    }
  });
  if (!plan || !plan.Plan) throw new TraceError("План не разобрался.");

  const aliases = new Map();
  walk(plan.Plan, (n) => {
    if (n["Relation Name"]) aliases.set(n.Alias || n["Relation Name"], n["Relation Name"]);
  });
  const ctx = {
    aliases,
    schema,
    hasOffset: /\boffset\b/i.test(sql),
    hasDistinct: /\bselect\s+distinct\b/i.test(sql),
    hasGroupBy: /\bgroup\s+by\b/i.test(sql),
  };

  const steps = [];
  walk(plan.Plan, (node) => {
    if (!TRANSPARENT.has(node["Node Type"])) steps.push(...stepsFor(node, ctx));
  });

  if (result && result.fields && result.fields.length) {
    const columns = result.fields.map((f) => f.name);
    const count = result.rows.length;
    steps.push({
      kind: "result",
      chip: "Результат",
      title: "Готовый результат",
      text:
        `SELECT оставляет нужные столбцы. На выходе: ${rowsLabel(count)}. ` +
        "Заметьте: первая строка запроса выполнилась последней.",
      rowsIn: null,
      rowsOut: count,
      active: [],
      tables: tablesUnder(plan.Plan),
      columns: (plan.Plan.Output || []).flatMap((expr) => columnRefs(expr, aliases)),
      clauses: ["SELECT", "RETURNING"],
      sample: {
        columns,
        rows: result.rows.slice(0, SAMPLE).map((row) => ({ cells: columns.map((c) => format(row[c])) })),
        total: count,
      },
    });
  }

  // Примеры строк читают базу в исходном виде, поэтому собираются после отката.
  // Режим «только чтение» не даёт запросу, собранному из плана, ничего изменить:
  // в выражениях могла оказаться, например, nextval().
  const started = performance.now();
  await sandbox(db, async () => {
    await db.exec("SET LOCAL transaction_read_only = on");
    const probe = prober(db);
    for (const step of steps) {
      if (step.load && performance.now() - started < BUDGET_MS) {
        step.sample = await step.load(probe);
      }
      delete step.load;
    }
  });

  const spans = clauseSpans(sql);
  const seen = [];
  for (const step of steps) {
    step.marks = marksFor(step, spans, sql).map((s) => [s.start, s.end]);
    // Условие из ON база тоже применяет при чтении таблицы, и подпись WHERE тут соврала бы.
    if (step.kind === "filter" && !/\bwhere\b/i.test(sql)) step.chip = "ON";
    // Таблицы накапливаются: уже прочитанная не гаснет на следующем шаге, по диаграмме
    // видно, сколько всего база успела задействовать.
    for (const table of step.tables || []) if (!seen.includes(table)) seen.push(table);
    step.tables = [...seen];
    step.links = step.links || [];
  }

  return {
    sql,
    steps,
    executionMs: plan["Execution Time"] || 0,
    planningMs: plan["Planning Time"] || 0,
  };
}
