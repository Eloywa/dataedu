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

const $ = (id) => document.getElementById(id);
let db = null;

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
    if (data.achievement) setStatus("🏆 Достижение: «" + data.achievement + "»", "ok");
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

async function makeDb() {
  const d = await PGlite.create();
  await d.exec(SEED);
  return d;
}

function renderResult(res) {
  const out = $("output");
  if (!res) {
    out.innerHTML = "";
    return;
  }
  if (!res.fields || res.fields.length === 0) {
    const n = res.affectedRows;
    out.innerHTML = `<div class="trainer-note">Выполнено${n != null ? ` · строк затронуто: ${n}` : ""}.</div>`;
    return;
  }
  const cols = res.fields.map((f) => f.name);
  let html = '<div class="trainer-table-wrap"><table class="trainer-table"><thead><tr>';
  html += cols.map((c) => `<th>${esc(c)}</th>`).join("");
  html += "</tr></thead><tbody>";
  for (const row of res.rows) {
    html += "<tr>" + cols.map((c) => `<td>${esc(fmt(row[c]))}</td>`).join("") + "</tr>";
  }
  html += "</tbody></table></div>";
  html += `<div class="trainer-note">${rowsLabel(res.rows.length)}</div>`;
  out.innerHTML = html;
}

function showError(msg) {
  $("output").innerHTML = `<div class="trainer-error mono">${esc(msg)}</div>`;
}

async function run() {
  const sql = $("sql").value.trim();
  if (!sql || !db) return;
  $("run").disabled = true;
  try {
    const results = await db.exec(sql); // массив результатов по стейтментам
    const withRows = [...results].reverse().find((r) => r.fields && r.fields.length);
    renderResult(withRows || results[results.length - 1]);
    logRun();
  } catch (e) {
    showError(e && e.message ? e.message : String(e));
  } finally {
    $("run").disabled = false;
  }
}

async function reset() {
  $("reset").disabled = true;
  setStatus("Сброс базы…");
  db = await makeDb();
  $("output").innerHTML = "";
  setStatus("База сброшена — готово", "ok");
  $("reset").disabled = false;
}

async function init() {
  try {
    db = await makeDb();
    setStatus("Готово — выполняйте запросы", "ok");
    $("run").disabled = false;
    $("reset").disabled = false;
  } catch (e) {
    setStatus("Не удалось загрузить PGlite: " + (e && e.message ? e.message : e), "err");
  }
}

$("run").addEventListener("click", run);
$("reset").addEventListener("click", reset);
$("sql").addEventListener("keydown", (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
    e.preventDefault();
    run();
  }
});

init();
