// Схема базы: список таблиц и ER-диаграмма.
//
// И то и другое читается из самой базы после каждого успешного запроса, а не
// вписано в шаблон. Раньше в разметке лежали две демонстрационные таблицы, и
// созданная студентом третья в списке не появлялась — панель врала ровно тогда,
// когда становилась нужна.
//
// Диаграмма нужна не для украшения. Курс начинается со связей между таблицами,
// а увидеть связь в тексте CREATE TABLE студент не может: REFERENCES — это одно
// слово в середине определения. На диаграмме то же самое — стрелка.

const esc = (v) => String(v).replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" })[c]);

/**
 * Читает структуру схемы public двумя запросами.
 * Отдельный запрос на таблицу дал бы столько же обращений, сколько таблиц,
 * ради одного и того же соединения — тот самый N+1, про который курс и написан.
 */
export async function readSchema(db) {
  const cols = await db.query(`
    SELECT table_name, column_name, data_type, ordinal_position
    FROM information_schema.columns
    WHERE table_schema = 'public'
    ORDER BY table_name, ordinal_position
  `);

  const keys = await db.query(`
    SELECT tc.constraint_type AS kind,
           tc.table_name      AS src,
           kcu.column_name    AS src_col,
           ccu.table_name     AS dst,
           ccu.column_name    AS dst_col
    FROM information_schema.table_constraints tc
    JOIN information_schema.key_column_usage kcu
      ON kcu.constraint_name = tc.constraint_name
     AND kcu.constraint_schema = tc.constraint_schema
    LEFT JOIN information_schema.constraint_column_usage ccu
      ON ccu.constraint_name = tc.constraint_name
     AND ccu.constraint_schema = tc.constraint_schema
    WHERE tc.table_schema = 'public'
      AND tc.constraint_type IN ('PRIMARY KEY', 'FOREIGN KEY')
  `);

  const tables = new Map();
  for (const r of cols.rows) {
    if (!tables.has(r.table_name)) {
      tables.set(r.table_name, { name: r.table_name, columns: [], pk: new Set(), fk: new Set() });
    }
    tables.get(r.table_name).columns.push({ name: r.column_name, type: r.data_type });
  }

  const links = [];
  const seen = new Set();
  for (const r of keys.rows) {
    const t = tables.get(r.src);
    if (!t) continue;
    if (r.kind === "PRIMARY KEY") {
      t.pk.add(r.src_col);
    } else if (r.dst) {
      t.fk.add(r.src_col);
      const id = `${r.src}.${r.src_col}->${r.dst}.${r.dst_col}`;
      if (!seen.has(id)) {
        seen.add(id);
        links.push({ src: r.src, srcCol: r.src_col, dst: r.dst, dstCol: r.dst_col });
      }
    }
  }

  return { tables: [...tables.values()], links };
}

// --- Список -----------------------------------------------------------------

export function renderList(schema) {
  if (!schema.tables.length) {
    return "<div class='schema-empty'>Таблиц нет. Создайте их или нажмите «Сбросить базу».</div>";
  }
  return schema.tables
    .map(
      (t) =>
        `<div class="schema-table"><b>${esc(t.name)}</b>` +
        `<span class="schema-cols">(${t.columns.map((c) => esc(c.name)).join(", ")})</span></div>`,
    )
    .join("");
}

// --- Диаграмма ---------------------------------------------------------------

const CHAR = 7.1; // ширина знака в 12px моноширинном начертании, с запасом
const ROW = 17;
const HEAD = 26;
const PAD_X = 14;
const GAP_X = 34;
const GAP_Y = 56;

function box(table) {
  const lines = table.columns.map((c) => `${c.name}  ${c.type}`);
  const widest = Math.max(table.name.length + 2, ...lines.map((l) => l.length));
  return {
    table,
    w: Math.max(140, Math.round(widest * CHAR) + PAD_X * 2),
    h: HEAD + table.columns.length * ROW + 8,
    x: 0,
    y: 0,
  };
}

/**
 * Раскладка по ярусам: таблица лежит ниже всех, на кого ссылается.
 * Получается привычный вид справочника — справочные таблицы сверху, журналы
 * снизу. Циклы (таблица, ссылающаяся сама на себя, или взаимные ссылки)
 * ограничены глубиной, иначе обход не закончится.
 */
function layout(schema) {
  const boxes = new Map(schema.tables.map((t) => [t.name, box(t)]));
  const parents = new Map(schema.tables.map((t) => [t.name, new Set()]));
  for (const l of schema.links) {
    if (l.src !== l.dst && parents.has(l.src)) parents.get(l.src).add(l.dst);
  }

  const depth = new Map();
  const resolve = (name, guard) => {
    if (depth.has(name)) return depth.get(name);
    if (guard.has(name)) return 0; // цикл — обрываем
    guard.add(name);
    let d = 0;
    for (const p of parents.get(name) || []) {
      if (boxes.has(p)) d = Math.max(d, resolve(p, guard) + 1);
    }
    guard.delete(name);
    depth.set(name, d);
    return d;
  };
  for (const name of boxes.keys()) resolve(name, new Set());

  const tiers = [];
  for (const [name, d] of depth) {
    (tiers[d] = tiers[d] || []).push(boxes.get(name));
  }

  let y = 10;
  let width = 0;
  for (const tier of tiers) {
    if (!tier) continue;
    tier.sort((a, b) => a.table.name.localeCompare(b.table.name));
    const total = tier.reduce((s, b) => s + b.w, 0) + GAP_X * (tier.length - 1);
    width = Math.max(width, total);
    let x = 0;
    for (const b of tier) {
      b.x = x;
      b.y = y;
      x += b.w + GAP_X;
    }
    y += Math.max(...tier.map((b) => b.h)) + GAP_Y;
  }

  // Центрируем ярусы друг относительно друга — иначе диаграмма клинится влево.
  for (const tier of tiers) {
    if (!tier) continue;
    const total = tier.reduce((s, b) => s + b.w, 0) + GAP_X * (tier.length - 1);
    const shift = (width - total) / 2 + 10;
    for (const b of tier) b.x += shift;
  }

  return { boxes, width: width + 20, height: y - GAP_Y + 20 };
}

function columnY(b, name) {
  const i = b.table.columns.findIndex((c) => c.name === name);
  return b.y + HEAD + (i < 0 ? 0 : i) * ROW + ROW / 2 - 2;
}

/** Связь рисуется от столбца-ссылки к столбцу-ключу — по стороне, которая ближе. */
function edge(from, to, link) {
  const y1 = columnY(from, link.srcCol);
  const y2 = columnY(to, link.dstCol);
  const leftward = from.x + from.w / 2 > to.x + to.w / 2;
  const x1 = leftward ? from.x : from.x + from.w;
  const x2 = leftward ? to.x + to.w : to.x;
  const bend = Math.max(30, Math.abs(x2 - x1) / 2);
  const c1 = leftward ? x1 - bend : x1 + bend;
  const c2 = leftward ? x2 + bend : x2 - bend;
  return (
    `<path class="er-link" d="M ${x1} ${y1} C ${c1} ${y1}, ${c2} ${y2}, ${x2} ${y2}" />` +
    `<circle class="er-dot" cx="${x1}" cy="${y1}" r="3" />` +
    `<circle class="er-dot er-dot-one" cx="${x2}" cy="${y2}" r="3" />`
  );
}

export function renderDiagram(schema) {
  if (!schema.tables.length) {
    return "<div class='schema-empty'>Таблиц нет — рисовать нечего.</div>";
  }
  const { boxes, width, height } = layout(schema);

  let edges = "";
  for (const link of schema.links) {
    const from = boxes.get(link.src);
    const to = boxes.get(link.dst);
    if (from && to && from !== to) edges += edge(from, to, link);
  }

  let nodes = "";
  for (const b of boxes.values()) {
    nodes += "<g>";
    nodes += `<rect class="er-box" x="${b.x}" y="${b.y}" width="${b.w}" height="${b.h}" rx="6" />`;
    nodes += `<rect class="er-head" x="${b.x}" y="${b.y}" width="${b.w}" height="${HEAD}" rx="6" />`;
    nodes += `<text class="er-title" x="${b.x + PAD_X}" y="${b.y + 17}">${esc(b.table.name)}</text>`;
    b.table.columns.forEach((c, i) => {
      const y = b.y + HEAD + i * ROW + 12;
      const mark = b.table.pk.has(c.name) ? "PK" : b.table.fk.has(c.name) ? "FK" : "";
      nodes += `<text class="er-col${mark ? " er-key" : ""}" x="${b.x + PAD_X}" y="${y}">${esc(c.name)}</text>`;
      nodes += `<text class="er-mark" x="${b.x + b.w - PAD_X}" y="${y}">${mark}</text>`;
    });
    nodes += "</g>";
  }

  const links = schema.links.length;
  return (
    `<div class="er-scroll"><svg class="er" viewBox="0 0 ${width} ${height}" ` +
    `width="${width}" height="${height}" role="img" ` +
    `aria-label="Диаграмма схемы: ${schema.tables.length} таблиц, ${links} связей">` +
    edges +
    nodes +
    "</svg></div>" +
    `<div class="trainer-note">Таблиц: ${schema.tables.length} · связей по внешним ключам: ${links}. ` +
    "Линия идёт от ссылающегося столбца к ключу, на который он ссылается.</div>"
  );
}
