// Автопроверка задания: запрос студента выполняется в браузере (PGlite) на заготовке
// данных задания; строки-результат уходят на сервер, который независимо ставит вердикт.
// Эталонный SQL студенту не отдаётся.
// Библиотека вшита в static/vendor/pglite — см. комментарий в trainer.js.
import { PGlite } from "../vendor/pglite/index.js";
import { rowsLabel } from "./plural.js";
import { setupEditor } from "./sql/editor.js";
import { classify } from "./sql/errors.js";
import { bindDiagram, fitDiagram, readSchema, renderDiagram } from "./sql/schema.js";

// Сколько строк показать в таблице задания: достаточно, чтобы понять, что в ней лежит,
// и не вытеснить редактор за край экрана.
const PREVIEW_ROWS = 6;

const $ = (id) => document.getElementById(id);
const root = $("assignment");
const checkUrl = root.dataset.checkUrl;
const csrf = root.dataset.csrf;
const setup = JSON.parse(($("setup-sql") && $("setup-sql").textContent) || '""');

// Без этого вызова поле нечитаемо: текст `.trainer-input` прозрачный, его показывает
// слой подсветки, который создаёт редактор. Именно так задание и сломалось, когда
// поле перевели на общий стиль с тренажёром, а обвязку не подключили.
const editor = setupEditor($("sql"), { symbolsHost: $("symbols") });

function esc(v) {
  return String(v).replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" })[c]);
}
function fmt(v) {
  if (v === null || v === undefined) return "NULL";
  return typeof v === "object" ? JSON.stringify(v) : String(v);
}
function setStatus(text, kind) {
  const el = $("status");
  el.textContent = text;
  el.className = "trainer-status mono" + (kind ? " " + kind : "");
}

async function freshDb() {
  const d = await PGlite.create();
  if (setup) await d.exec(setup);
  return d;
}

function quoteIdent(name) {
  return '"' + String(name).replace(/"/g, '""') + '"';
}

/** Одна таблица задания: столбцы с типами и первые строки. */
async function tableCard(db, table) {
  const name = quoteIdent(table.name);
  const [rows, count] = await Promise.all([
    db.query(`SELECT * FROM ${name} LIMIT ${PREVIEW_ROWS}`),
    db.query(`SELECT count(*)::int AS n FROM ${name}`),
  ]);
  const total = count.rows[0].n;
  const columns = table.columns.map((c) => c.name);

  let html = '<div class="task-table">';
  html += `<div class="task-table-head"><b class="task-table-name">${esc(table.name)}</b>`;
  html += `<span class="task-table-count">${rowsLabel(total)}</span></div>`;
  html += '<div class="trainer-table-wrap"><table class="trainer-table">';
  html += `<caption class="visually-hidden">Таблица ${esc(table.name)}</caption><thead><tr>`;
  html += table.columns
    .map((c) => `<th>${esc(c.name)}<span class="task-type">${esc(c.type)}</span></th>`)
    .join("");
  html += "</tr></thead><tbody>";
  for (const row of rows.rows) {
    html += "<tr>" + columns.map((c) => `<td>${esc(fmt(row[c]))}</td>`).join("") + "</tr>";
  }
  html += "</tbody></table></div>";
  if (total > rows.rows.length) {
    html += `<p class="trainer-note">Показаны первые ${rows.rows.length} — в запросе участвуют все.</p>`;
  }
  return html + "</div>";
}

/** Схема и содержимое заготовки задания: то, с чем студенту предстоит работать. */
async function showTables(db) {
  const host = $("task-tables");
  if (!host) return;
  const schema = await readSchema(db);
  const cards = await Promise.all(schema.tables.map((table) => tableCard(db, table)));

  // Диаграмма нужна там, где есть что соединять: у одной таблицы рисовать нечего.
  const diagram = schema.links.length
    ? `<div class="task-diagram">${renderDiagram(schema, {}, { note: false })}</div>`
    : "";
  host.innerHTML = `${diagram}<div class="task-tables">${cards.join("")}</div>`;

  const box = host.querySelector(".task-diagram");
  if (box) {
    bindDiagram(box);
    fitDiagram(box, { maxHeight: 260, maxScale: 1 });
  }
}

function renderTable(res) {
  const out = $("output");
  if (!res || !res.fields || res.fields.length === 0) {
    out.innerHTML = '<div class="trainer-note">Запрос не вернул таблицу.</div>';
    return { cols: [], rows: [] };
  }
  const cols = res.fields.map((f) => f.name);
  let html = '<div class="trainer-table-wrap"><table class="trainer-table"><thead><tr>';
  html += cols.map((c) => `<th>${esc(c)}</th>`).join("") + "</tr></thead><tbody>";
  for (const row of res.rows) {
    html += "<tr>" + cols.map((c) => `<td>${esc(fmt(row[c]))}</td>`).join("") + "</tr>";
  }
  html += `</tbody></table></div><div class="trainer-note">${rowsLabel(res.rows.length)}</div>`;
  out.innerHTML = html;
  return { cols, rows: res.rows.map((r) => cols.map((c) => r[c])) };
}

// Ошибку разбирает тот же модуль, что и в тренажёре: студент, привыкший к
// пояснению в песочнице, не должен терять его ровно там, где решает задачу.
// Класс ошибки уходит на сервер — из него собирается отчёт «на чём спотыкаются».
function showError(msg) {
  const { code, hint } = classify(msg);
  $("output").innerHTML =
    `<div class="trainer-error mono">${esc(msg)}</div>` +
    (hint ? `<div class="diag-hint">${esc(hint)}</div>` : "");
  const url = root.dataset.errorUrl;
  if (!url) return;
  fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrf },
    body: JSON.stringify({ error: code }),
  }).catch(() => {
    // молча: учёт не должен мешать решению задачи
  });
}
// Вердикт с разбором: три проверки (столбцы / число строк / состав строк) и одна
// подсказка о вероятной причине. Содержимое эталона сервер не присылает — только
// количества, поэтому подсказка не выдаёт ответ.
function showVerdict(passed, checks, hint) {
  let html = `<div class="verdict ${passed ? "ok" : "fail"}">${passed ? "✓ Верно" : "✗ Неверно"}</div>`;
  if (checks && checks.length) {
    html += '<ul class="diag-list mono">';
    for (const c of checks) {
      html +=
        `<li class="${c.ok ? "diag-ok" : "diag-fail"}">` +
        `<span class="diag-mark">${c.ok ? "✓" : "✗"}</span>` +
        `<span class="diag-label">${esc(c.label)}</span>` +
        `<span class="diag-detail">${esc(c.detail)}</span></li>`;
    }
    html += "</ul>";
  }
  if (hint) html += `<div class="diag-hint">${esc(hint)}</div>`;
  $("verdict").innerHTML = html;
}

function showVerdictError(message) {
  $("verdict").innerHTML =
    `<div class="verdict fail">✗ Не проверено</div>` +
    `<div class="diag-hint">${esc(message)}</div>`;
}

async function check() {
  const sql = $("sql").value.trim();
  if (!sql) return;
  $("check").disabled = true;
  $("verdict").innerHTML = "";
  try {
    const db = await freshDb(); // свежая БД на каждую проверку
    const results = await db.exec(sql);
    const res = [...results].reverse().find((r) => r.fields && r.fields.length) || results[results.length - 1];
    const { cols, rows } = renderTable(res);

    const resp = await fetch(checkUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-CSRFToken": csrf },
      body: JSON.stringify({ sql, columns: cols, rows }),
    });
    const data = await resp.json();
    if (!resp.ok) {
      // Например, у задания не посчитан эталон — это не ошибка студента.
      showVerdictError(data.message || "Проверка недоступна: " + resp.status);
    } else {
      showVerdict(!!data.passed, data.checks, data.hint);
    }
  } catch (e) {
    showError(e && e.message ? e.message : String(e));
    showVerdictError("Запрос не выполнился — исправьте ошибку в SQL и попробуйте снова.");
  } finally {
    $("check").disabled = false;
  }
}

async function init() {
  try {
    const db = await freshDb(); // прогрев PGlite: заодно есть откуда взять таблицы задания
    setStatus("Готово — напишите запрос и нажмите «Проверить»", "ok");
    $("check").disabled = false;
    $("resetdb").disabled = false;
    await showTables(db).catch(() => {
      // Решить задачу можно и без показа таблиц: это не повод блокировать проверку.
      const host = $("task-tables");
      if (host) host.textContent = "Не удалось показать таблицы.";
    });
  } catch (e) {
    setStatus("Не удалось загрузить PGlite: " + (e && e.message ? e.message : e), "err");
  }
}

$("check").addEventListener("click", check);
$("resetdb").addEventListener("click", () => {
  $("sql").value = "";
  editor.refresh(); // присваивание не порождает `input`, и подложка осталась бы старой
  $("output").innerHTML = "";
  $("verdict").innerHTML = "";
});
$("sql").addEventListener("keydown", (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
    e.preventDefault();
    check();
  }
});

init();
