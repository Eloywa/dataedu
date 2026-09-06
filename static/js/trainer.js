// SQL-тренажёр: PostgreSQL в браузере через PGlite (WebAssembly).
// Вся работа — на стороне клиента; сервер Django только отдаёт страницу.
// Библиотека вшита в static/vendor/pglite — ни один внешний запрос не уходит:
// тренажёр работает без интернета, и IP студента не утекает в зарубежный CDN.
import { PGlite } from "../vendor/pglite/index.js";
import { rowsLabel } from "./plural.js";

// Фиксированный учебный набор — одинаковый для всех. Пересоздаётся при сбросе.
const SEED = `
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS groups;
CREATE TABLE groups (
  id      integer PRIMARY KEY,
  name    text NOT NULL,
  curator text
);
INSERT INTO groups (id, name, curator) VALUES
  (1, 'ПИ-101', 'Иванов И. И.'),
  (2, 'ПИ-102', 'Петрова О. И.'),
  (3, 'МО-201', 'Сидоров С. С.');
CREATE TABLE students (
  id        integer PRIMARY KEY,
  full_name text NOT NULL,
  group_id  integer REFERENCES groups(id),
  xp        integer NOT NULL DEFAULT 0
);
INSERT INTO students (id, full_name, group_id, xp) VALUES
  (1,  'Анна Соколова',     1, 320),
  (2,  'Дмитрий Соколов',   1, 180),
  (3,  'Мария Иванова',     1, 240),
  (4,  'Павел Кузнецов',    2, 90),
  (5,  'Ольга Попова',      2, 410),
  (6,  'Артём Михайлов',    2, 0),
  (7,  'Полина Захарова',   2, 150),
  (8,  'Денис Григорьев',   3, 200),
  (9,  'Виктория Иванова',  3, 365),
  (10, 'Глеб Тимофеев',     3, 130),
  (11, 'Егор Новиков',      1, 275),
  (12, 'Софья Морозова',    3, 55);
`;

// Сколько строк рисовать. Ограничение не косметическое: студент, изучающий
// generate_series, одной строкой делает миллион записей, и попытка отрисовать
// их все вешает вкладку намертво — вместе с несохранённым запросом.
const RENDER_LIMIT = 200;

// Сколько запросов помнить. Больше и не нужно: история — чтобы вернуться на
// шаг-другой назад, а не журнал за всё занятие.
const HISTORY_LIMIT = 20;

const $ = (id) => document.getElementById(id);
let db = null;
let history = [];
let historyPos = -1;

// Отметка об удачном запуске: серверу уходит только факт (для аналитики и
// достижения «Первый запрос»), сам SQL остаётся в браузере.
async function logRun() {
  const root = $("trainer");
  const url = root && root.dataset.logUrl;
  if (!url) return; // гость — не логируем
  try {
    const res = await fetch(url, {
      method: "POST",
      headers: { "X-CSRFToken": root.dataset.csrf },
    });
    const data = await res.json();
    if (data.achievement) setStatus("Достижение: «" + data.achievement + "»", "ok");
  } catch {
    // молча: аналитика не должна мешать работе тренажёра
  }
}

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

// Время округляем до десятых: PGlite работает в WebAssembly, и разброс между
// одинаковыми запусками больше, чем разница в сотых долях миллисекунды.
function ms(value) {
  return value < 10 ? value.toFixed(1) : Math.round(value);
}

async function makeDb() {
  const d = await PGlite.create();
  await d.exec(SEED);
  return d;
}

// --- Разбор ошибок PostgreSQL ------------------------------------------------
//
// Сообщения приходят по-английски и в терминах движка: «relation does not exist»
// ничего не говорит второкурснику, который ищет опечатку в названии таблицы.
// Здесь — перевод самых частых на язык учебной задачи. Оригинал остаётся рядом:
// умение читать вывод СУБД — тоже часть курса, прятать его нельзя.
const ERROR_HINTS = [
  [/relation "(.+?)" does not exist/i, (m) => `Таблицы «${m[1]}» в базе нет. Проверьте название — список таблиц слева.`],
  [/column "(.+?)" does not exist/i, (m) => `Столбца «${m[1]}» нет. Разверните таблицу в списке слева, чтобы увидеть её столбцы.`],
  [/column (.+?) must appear in the GROUP BY/i, (m) => `Столбец ${m[1]} не агрегирован: при GROUP BY каждый столбец из SELECT либо перечислен в группировке, либо обёрнут в агрегат — count, sum, avg.`],
  [/syntax error at or near "(.+?)"/i, (m) => `Синтаксическая ошибка около «${m[1]}». Обычно причина раньше этого места: пропущенная запятая, скобка или ключевое слово.`],
  [/operator does not exist: (.+)/i, (m) => `Несовместимые типы в сравнении (${m[1]}). Число со строкой напрямую сравнивать нельзя — приведите тип через CAST или ::.`],
  [/division by zero/i, () => "Деление на ноль. Отсеките нулевой делитель через NULLIF или условие в WHERE."],
  [/duplicate key value violates unique constraint/i, () => "Такое значение уже есть, а столбец объявлен уникальным. Это и есть ограничение целостности в работе."],
  [/null value in column "(.+?)".*not-null/i, (m) => `Столбец «${m[1]}» объявлен NOT NULL — значение обязательно.`],
  [/violates foreign key constraint/i, () => "Внешний ключ ссылается на несуществующую строку. Сначала добавьте запись в таблицу, на которую ссылаетесь."],
  [/permission denied|must be owner/i, () => "Операция запрещена. В песочнице доступны обычные запросы и работа с таблицами, но не администрирование сервера."],
];

function explainError(message) {
  for (const [pattern, build] of ERROR_HINTS) {
    const m = pattern.exec(message);
    if (m) return build(m);
  }
  return null;
}

function showError(message) {
  const hint = explainError(message);
  $("output").innerHTML =
    `<div class="trainer-error mono">${esc(message)}</div>` +
    (hint ? `<div class="diag-hint">${esc(hint)}</div>` : "");
}

// --- Схема из самой базы -----------------------------------------------------

async function refreshSchema() {
  const body = $("schema").querySelector(".schema-body");
  try {
    // Столбцы и таблицы одним запросом: отдельный запрос на таблицу дал бы
    // столько же обращений, сколько таблиц, ради одного и того же соединения.
    const res = await db.query(`
      SELECT table_name, column_name, data_type
      FROM information_schema.columns
      WHERE table_schema = 'public'
      ORDER BY table_name, ordinal_position
    `);
    const tables = new Map();
    for (const r of res.rows) {
      if (!tables.has(r.table_name)) tables.set(r.table_name, []);
      tables.get(r.table_name).push(r.column_name);
    }
    if (!tables.size) {
      body.innerHTML = "<div class='schema-empty'>Таблиц нет. Создайте их или нажмите «Сбросить базу».</div>";
      return;
    }
    body.innerHTML = [...tables]
      .map(
        ([name, cols]) =>
          `<div class="schema-table"><b>${esc(name)}</b>` +
          `<span class="schema-cols">(${cols.map(esc).join(", ")})</span></div>`,
      )
      .join("");
  } catch {
    body.textContent = "Не удалось прочитать схему.";
  }
}

// --- История -----------------------------------------------------------------

function remember(sql) {
  history = [sql, ...history.filter((q) => q !== sql)].slice(0, HISTORY_LIMIT);
  historyPos = -1;
  renderHistory();
}

function renderHistory() {
  const box = $("history");
  const list = $("history-list");
  box.hidden = history.length === 0;
  list.innerHTML = history
    .map((q, i) => `<li><button type="button" class="history-item mono" data-i="${i}">${esc(q)}</button></li>`)
    .join("");
}

// --- Выполнение --------------------------------------------------------------

function renderResult(res, elapsed) {
  const out = $("output");
  if (!res) {
    out.innerHTML = "";
    return;
  }
  const timing = `<span class="trainer-timing">${ms(elapsed)} мс</span>`;

  if (!res.fields || res.fields.length === 0) {
    const n = res.affectedRows;
    out.innerHTML =
      `<div class="trainer-note">Выполнено${n != null ? ` · строк затронуто: ${n}` : ""} ${timing}</div>`;
    return;
  }

  const cols = res.fields.map((f) => f.name);
  const shown = res.rows.slice(0, RENDER_LIMIT);
  let html = '<div class="trainer-table-wrap"><table class="trainer-table"><thead><tr>';
  html += cols.map((c) => `<th>${esc(c)}</th>`).join("");
  html += "</tr></thead><tbody>";
  for (const row of shown) {
    html += "<tr>" + cols.map((c) => `<td>${esc(fmt(row[c]))}</td>`).join("") + "</tr>";
  }
  html += "</tbody></table></div>";
  html += `<div class="trainer-note">${rowsLabel(res.rows.length)} ${timing}`;
  if (res.rows.length > RENDER_LIMIT) {
    html += ` · показаны первые ${RENDER_LIMIT}`;
  }
  html += "</div>";
  out.innerHTML = html;
}

// План запроса выводится как есть, моноширинным блоком: это текст, у которого
// значим каждый отступ — по ним и читается вложенность узлов плана.
function renderPlan(rows, elapsed) {
  const text = rows.map((r) => Object.values(r)[0]).join("\n");
  $("output").innerHTML =
    `<div class="trainer-plan mono">${esc(text)}</div>` +
    `<div class="trainer-note">План построен за <span class="trainer-timing">${ms(elapsed)} мс</span>. ` +
    "Читается снизу вверх: нижние узлы выполняются первыми.</div>";
}

async function execute({ plan = false } = {}) {
  const sql = $("sql").value.trim();
  if (!sql || !db) return;
  $("run").disabled = true;
  $("explain").disabled = true;
  try {
    const started = performance.now();
    if (plan) {
      // ANALYZE действительно выполняет запрос — иначе в плане не будет
      // фактического числа строк, а именно расхождение оценки с фактом и
      // объясняет, почему запрос медленный.
      const res = await db.query(`EXPLAIN (ANALYZE, BUFFERS) ${sql}`);
      renderPlan(res.rows, performance.now() - started);
    } else {
      const results = await db.exec(sql);
      const elapsed = performance.now() - started;
      const withRows = [...results].reverse().find((r) => r.fields && r.fields.length);
      renderResult(withRows || results[results.length - 1], elapsed);
    }
    remember(sql);
    await refreshSchema();
    logRun();
  } catch (e) {
    showError(e && e.message ? e.message : String(e));
  } finally {
    $("run").disabled = false;
    $("explain").disabled = false;
  }
}

async function reset() {
  $("reset").disabled = true;
  setStatus("Сброс базы…");
  db = await makeDb();
  $("output").innerHTML = "";
  await refreshSchema();
  setStatus("База сброшена — готово", "ok");
  $("reset").disabled = false;
}

async function init() {
  try {
    db = await makeDb();
    await refreshSchema();
    setStatus("Готово — выполняйте запросы", "ok");
    $("run").disabled = false;
    $("explain").disabled = false;
    $("reset").disabled = false;
  } catch (e) {
    setStatus("Не удалось загрузить PGlite: " + (e && e.message ? e.message : e), "err");
  }
}

$("run").addEventListener("click", () => execute());
$("explain").addEventListener("click", () => execute({ plan: true }));
$("reset").addEventListener("click", reset);

$("history-list").addEventListener("click", (e) => {
  const item = e.target.closest(".history-item");
  if (!item) return;
  $("sql").value = history[Number(item.dataset.i)];
  $("sql").focus();
});

$("sql").addEventListener("keydown", (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
    e.preventDefault();
    execute();
    return;
  }
  // Ctrl+↑/↓ листает историю. Именно с модификатором: голые стрелки нужны для
  // перемещения по многострочному запросу, и перехватывать их нельзя.
  if ((e.ctrlKey || e.metaKey) && (e.key === "ArrowUp" || e.key === "ArrowDown")) {
    if (!history.length) return;
    e.preventDefault();
    historyPos =
      e.key === "ArrowUp"
        ? Math.min(historyPos + 1, history.length - 1)
        : Math.max(historyPos - 1, -1);
    $("sql").value = historyPos === -1 ? "" : history[historyPos];
  }
});

init();
