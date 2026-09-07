// План запроса деревом.
//
// `EXPLAIN ANALYZE` в текстовом виде — это стена моноширинных строк, в которой
// вложенность задана отступами, а время размазано по узлам. Опытный человек
// читает её за минуту; студент, ради которого курс «Индексы и производительность»
// и написан, — не читает вообще. Поэтому берётся FORMAT JSON и рисуется дерево,
// где у каждого узла видно собственное время, долю от общего и расхождение
// оценки планировщика с фактом.
//
// Про доли важное: `Actual Total Time` у узла — накопительное, оно включает
// потомков. Показывать его как «время узла» — обычная ошибка чтения плана,
// из-за которой корень всегда выглядит самым дорогим. Здесь считается
// собственное время: своё минус сумма детей, и всё умножается на число проходов.

const esc = (v) => String(v).replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" })[c]);

function ms(value) {
  if (value >= 100) return Math.round(value) + " мс";
  if (value >= 1) return value.toFixed(1) + " мс";
  return value.toFixed(2) + " мс";
}

function num(value) {
  return new Intl.NumberFormat("ru-RU").format(Math.round(value));
}

/** Итог EXPLAIN (FORMAT JSON) приходит либо строкой, либо уже разобранным. */
export function parsePlan(rows) {
  const raw = rows && rows.length ? Object.values(rows[0])[0] : null;
  if (!raw) return null;
  const data = typeof raw === "string" ? JSON.parse(raw) : raw;
  return Array.isArray(data) ? data[0] : data;
}

function inclusive(node) {
  return (node["Actual Total Time"] || 0) * (node["Actual Loops"] || 1);
}

function self(node) {
  const children = node.Plans || [];
  return Math.max(0, inclusive(node) - children.reduce((sum, c) => sum + inclusive(c), 0));
}

/** Строка вида «Seq Scan on students s» — что именно делает узел и над чем. */
function heading(node) {
  const parts = [node["Node Type"]];
  if (node.Strategy && node.Strategy !== "Plain") parts.push(node.Strategy);
  if (node["Join Type"] && node["Node Type"] !== "Nested Loop") parts.push(node["Join Type"]);
  let text = parts.join(" · ");
  if (node["Index Name"]) text += ` по индексу ${node["Index Name"]}`;
  return text;
}

function target(node) {
  if (!node["Relation Name"]) return "";
  const alias = node.Alias && node.Alias !== node["Relation Name"] ? ` ${node.Alias}` : "";
  return `${node["Relation Name"]}${alias}`;
}

/** Условия узла: по ним видно, что именно отсекается и на каком шаге. */
function conditions(node) {
  const out = [];
  for (const key of ["Index Cond", "Filter", "Hash Cond", "Join Filter", "Recheck Cond"]) {
    if (node[key]) out.push([key, node[key]]);
  }
  if (node["Group Key"]) out.push(["Group Key", node["Group Key"].join(", ")]);
  if (node["Sort Key"]) out.push(["Sort Key", node["Sort Key"].join(", ")]);
  return out;
}

// Замечания — то, ради чего план вообще открывают. Каждое отвечает на вопрос
// «почему медленно», а не описывает узел ещё раз другими словами.
function flags(node) {
  const out = [];
  const loops = node["Actual Loops"] || 1;
  const actual = node["Actual Rows"] || 0;
  const planned = node["Plan Rows"] || 0;

  if (planned > 0 && actual > 0) {
    const ratio = actual > planned ? actual / planned : planned / actual;
    if (ratio >= 10) {
      out.push(
        actual > planned
          ? `Планировщик ожидал ${num(planned)} строк, пришло ${num(actual)} — занижено в ${Math.round(ratio)} раз. ` +
              "Из-за таких расхождений выбирается неудачный способ соединения; помогает ANALYZE."
          : `Планировщик ожидал ${num(planned)} строк, пришло ${num(actual)} — завышено в ${Math.round(ratio)} раз.`,
      );
    }
  }

  const removed = node["Rows Removed by Filter"];
  if (node["Node Type"] === "Seq Scan" && removed >= 1000 && removed > actual * 5) {
    out.push(
      `Последовательный просмотр отбросил ${num(removed)} строк из прочитанных. ` +
        `Условие «${node.Filter || ""}» просится в индекс.`,
    );
  }

  if (node["Node Type"] === "Sort" && node["Sort Method"] && /external/i.test(node["Sort Method"])) {
    out.push("Сортировка не поместилась в память и ушла на диск (work_mem).");
  }

  if (loops > 100) {
    out.push(`Узел выполнен ${num(loops)} раз — вложенный цикл по внешней выборке.`);
  }

  return out;
}

function renderNode(node, total, depth) {
  const own = self(node);
  const share = total > 0 ? Math.min(100, (own / total) * 100) : 0;
  const rel = target(node);
  const conds = conditions(node);
  const notes = flags(node);
  const loops = node["Actual Loops"] || 1;
  const buffers = node["Shared Hit Blocks"] || 0;

  let html = `<li class="plan-node${share >= 30 ? " plan-hot" : ""}">`;
  html += `<div class="plan-bar"><i style="width:${share.toFixed(1)}%"></i></div>`;
  html += `<div class="plan-head"><b>${esc(heading(node))}</b>`;
  if (rel) html += ` <span class="plan-rel mono">${esc(rel)}</span>`;
  html += `<span class="plan-share">${share.toFixed(0)}%</span></div>`;

  const meta = [
    `собственное время ${ms(own)}`,
    `строк ${num(node["Actual Rows"] || 0)}`,
    `оценка ${num(node["Plan Rows"] || 0)}`,
  ];
  if (loops > 1) meta.push(`проходов ${num(loops)}`);
  if (buffers) meta.push(`буферов ${num(buffers)}`);
  html += `<div class="plan-meta">${esc(meta.join(" · "))}</div>`;

  for (const [key, value] of conds) {
    html += `<div class="plan-cond mono"><span>${esc(key)}</span> ${esc(value)}</div>`;
  }
  for (const note of notes) {
    html += `<div class="plan-flag">${esc(note)}</div>`;
  }

  const children = node.Plans || [];
  if (children.length) {
    html += "<ul class='plan-children'>";
    for (const child of children) html += renderNode(child, total, depth + 1);
    html += "</ul>";
  }
  html += "</li>";
  return html;
}

/**
 * Рисует разобранный план.
 * @param {object} plan результат parsePlan
 * @returns {string} готовая разметка
 */
export function renderPlan(plan) {
  if (!plan || !plan.Plan) return "<div class='trainer-note'>План не разобрался.</div>";
  const exec = plan["Execution Time"] || inclusive(plan.Plan);
  const planning = plan["Planning Time"] || 0;

  return (
    "<ul class='plan-tree'>" +
    renderNode(plan.Plan, exec, 0) +
    "</ul>" +
    `<div class="trainer-note">Планирование ${ms(planning)}, выполнение ${ms(exec)}. ` +
    "Проценты — собственное время узла, без вложенных.</div>"
  );
}

/** Типы узлов-просмотров в порядке появления — для сравнения «до и после индекса». */
export function scanNodes(plan) {
  const out = [];
  (function walk(node) {
    if (!node) return;
    if (/Scan/.test(node["Node Type"] || "")) {
      out.push({
        type: node["Node Type"],
        relation: node["Relation Name"] || "",
        index: node["Index Name"] || "",
      });
    }
    for (const child of node.Plans || []) walk(child);
  })(plan && plan.Plan);
  return out;
}
