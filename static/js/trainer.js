// SQL-тренажёр: PostgreSQL в браузере через PGlite (WebAssembly).
// Вся работа — на стороне клиента; сервер Django только отдаёт страницу.
// Библиотека вшита в static/vendor/pglite — ни один внешний запрос не уходит:
// тренажёр работает без интернета, и IP студента не утекает в зарубежный CDN.
import { PGlite } from "../vendor/pglite/index.js";
import { pluralRu, rowsLabel } from "./plural.js";
import { DATASETS, DEFAULT_DATASET, WIPE } from "./sql/datasets.js";
import { classify } from "./sql/errors.js";
import { parsePlan, renderPlan, scanNodes } from "./sql/plan.js";
import { readSchema, renderList, renderDiagram, bindDiagram } from "./sql/schema.js";
import { dumpDatabase } from "./sql/dump.js";

// База живёт в IndexedDB, а не в памяти вкладки. Дело не только в том, что
// созданные студентом таблицы переживают перезагрузку: создание кластера с нуля
// занимает около 1,8 с, и раньше эта секунда с лишним набегала на каждый заход.
const STORE = "idb://dataedu-trainer";

// Служебная таблица лежит в отдельной схеме: в public она попадала бы в список
// таблиц и на диаграмму, и студент считал бы её частью учебных данных.
const META = `
CREATE SCHEMA IF NOT EXISTS dataedu;
CREATE TABLE IF NOT EXISTS dataedu.meta (dataset text NOT NULL);
`;

// Сколько строк рисовать. Ограничение не косметическое: студент, изучающий
// generate_series, одной строкой делает миллион записей, и попытка отрисовать
// их все вешает вкладку намертво — вместе с несохранённым запросом.
const RENDER_LIMIT = 200;

// Сколько запросов помнить. Больше и не нужно: история — чтобы вернуться на
// шаг-другой назад, а не журнал за всё занятие.
const HISTORY_LIMIT = 20;

// Замер повторяет запрос несколько раз и берёт медиану: первый прогон греет
// кеш буферов, а разброс между соседними запусками в WebAssembly заметный.
const MEASURE_RUNS = 5;

// Ниже этого числа строк индекс не нужен, и планировщик его не возьмёт —
// на таком объёме сравнивать «до и после» бессмысленно.
const SMALL_TABLE = 5000;

const $ = (id) => document.getElementById(id);
let db = null;
let dataset = DEFAULT_DATASET;
let restored = false;
let schema = { tables: [], links: [] };
let schemaView = "list";
let queries = [];
let historyPos = -1;
let lastResult = null; // для выгрузки в CSV
const measured = new Map(); // нормализованный SQL → последний замер

// --- Мелочи ------------------------------------------------------------------

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

/** Запрос без лишних пробелов и регистра — чтобы узнать «тот же самый» при замере. */
function normalize(sql) {
  return sql.replace(/\s+/g, " ").trim().toLowerCase().replace(/;$/, "");
}

/** Только читающие запросы можно выполнять повторно.
 *  EXPLAIN ANALYZE на INSERT действительно вставляет строки, а замер повторил бы
 *  вставку пять раз — «показать план» тихо менял бы данные студента. */
function readOnly(sql) {
  return /^\s*(select|with|table|values)\b/i.test(sql);
}

function quoteIdent(name) {
  return '"' + String(name).replace(/"/g, '""') + '"';
}

// --- Учёт на сервере ---------------------------------------------------------

// Серверу уходит только факт: запуск запроса и класс ошибки. Ни SQL, ни текст
// ошибки не передаются — в них попадают и данные, которые студент придумал сам.
async function report(payload) {
  const root = $("trainer");
  const url = root && root.dataset.logUrl;
  if (!url) return; // гость — не логируем
  try {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-CSRFToken": root.dataset.csrf },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (data.achievement) setStatus("Достижение: «" + data.achievement + "»", "ok");
  } catch {
    // молча: аналитика не должна мешать работе тренажёра
  }
}

// --- Загрузка движка ---------------------------------------------------------

// PGlite скачивает 16 МБ и о ходе загрузки не сообщает. На быстрой машине это
// незаметно, в аудитории с общим каналом — секунд восемь пустой строки
// «загрузка…». Поэтому файлы скачиваются здесь, со шкалой, и передаются движку
// готовыми (см. `preload`), а не оставляются ему на самостоятельную загрузку.
const HEAVY = [
  ["pglite.wasm", 9851],
  ["pglite.data", 6146],
];

async function readWithProgress(file, onChunk) {
  const res = await fetch(new URL(`../vendor/pglite/${file}`, import.meta.url));
  if (!res.ok) throw new Error(`${file}: ${res.status}`);
  const reader = res.body.getReader();
  const parts = [];
  for (;;) {
    const chunk = await reader.read();
    if (chunk.done) break;
    parts.push(chunk.value);
    onChunk(chunk.value.length);
  }
  return new Blob(parts);
}

/**
 * Скачивает движок со шкалой и отдаёт его уже разобранным.
 *
 * Скачанное обязательно передаётся в PGlite: иначе он тянет те же файлы второй
 * раз, и шкала, задуманная как утешение на время загрузки, сама удваивает её —
 * почти десять лишних мегабайт. Имена `pgliteWasmModule` и `fsBundle` — из
 * самого PGlite; при обновлении библиотеки их надо сверить. Если не совпадут,
 * поломки не будет: движок просто скачает файлы сам, как и раньше.
 */
async function preload(onProgress) {
  const total = HEAVY.reduce((sum, [, kb]) => sum + kb, 0);
  let done = 0;
  const tick = (bytes) => {
    done += bytes / 1024;
    onProgress(Math.min(99, (done / total) * 100));
  };

  try {
    const [wasm, data] = await Promise.all([
      readWithProgress("pglite.wasm", tick),
      readWithProgress("pglite.data", tick),
    ]);
    onProgress(100);
    return {
      pgliteWasmModule: await WebAssembly.compile(await wasm.arrayBuffer()),
      fsBundle: data,
    };
  } catch {
    onProgress(100);
    return {}; // не вышло — движок скачает файлы сам
  }
}

function setProgress(percent) {
  const bar = $("boot-bar");
  if (bar) bar.style.width = percent.toFixed(0) + "%";
}

// --- База --------------------------------------------------------------------

async function currentDataset() {
  try {
    const res = await db.query("SELECT dataset FROM dataedu.meta LIMIT 1");
    return res.rows.length ? res.rows[0].dataset : null;
  } catch {
    return null; // схемы ещё нет — база пустая
  }
}

async function seed(key) {
  await db.exec(WIPE);
  // У пустого набора данных нет — выполнять пустую строку нельзя.
  if (DATASETS[key].sql.trim()) await db.exec(DATASETS[key].sql);
  await db.exec(META);
  await db.exec("DELETE FROM dataedu.meta;");
  await db.query("INSERT INTO dataedu.meta (dataset) VALUES ($1)", [key]);
  // Без статистики планировщик считает любую таблицу крошечной, и план на
  // раздутых данных получается неправдоподобным.
  await db.exec("ANALYZE;");
  dataset = key;
  try {
    localStorage.setItem("trainer-dataset", key);
  } catch {
    // приватный режим — просто не запомним выбор
  }
}

async function openDb(artifacts) {
  try {
    return await PGlite.create({ dataDir: STORE, ...artifacts });
  } catch {
    // Хранилище недоступно (приватный режим, кончилась квота) — работаем в
    // памяти. Тренажёр важнее сохранности учебной песочницы.
    return await PGlite.create({ ...artifacts });
  }
}

// --- Схема -------------------------------------------------------------------

// Расположение таблиц на диаграмме — на каждый набор данных своё: разложив
// «Магазин», студент не должен обнаружить эту же раскладку натянутой на
// «Библиотеку», где и таблицы другие.
function layoutKey() {
  return `trainer-er-${dataset}`;
}

function savedLayout() {
  try {
    return JSON.parse(localStorage.getItem(layoutKey()) || "{}");
  } catch {
    return {}; // приватный режим или испорченная запись — раскладываем заново
  }
}

function saveLayout(positions) {
  try {
    localStorage.setItem(layoutKey(), JSON.stringify(positions));
  } catch {
    // не сохранилось — расположение проживёт до перезагрузки, и только
  }
}

async function refreshSchema() {
  const body = $("schema").querySelector(".schema-body");
  try {
    schema = await readSchema(db);
    if (schemaView === "list") {
      body.innerHTML = renderList(schema, DATASETS[dataset] && DATASETS[dataset].emptyHint);
      return;
    }
    body.innerHTML = renderDiagram(schema, savedLayout());
    bindDiagram(body, saveLayout);
  } catch {
    body.textContent = "Не удалось прочитать схему.";
  }
}

function toggleSchemaView() {
  schemaView = schemaView === "list" ? "diagram" : "list";
  $("schema-view").textContent = schemaView === "list" ? "Диаграмма" : "Списком";
  $("schema").classList.toggle("is-diagram", schemaView === "diagram");
  refreshSchema();
}

// --- История -----------------------------------------------------------------

function remember(sql) {
  queries = [sql, ...queries.filter((q) => q !== sql)].slice(0, HISTORY_LIMIT);
  historyPos = -1;
  renderHistory();
}

function renderHistory() {
  const box = $("history");
  const list = $("history-list");
  box.hidden = queries.length === 0;
  list.innerHTML = queries
    .map(
      (q, i) =>
        `<li><button type="button" class="history-item mono" data-i="${i}">${esc(q)}</button></li>`,
    )
    .join("");
}

// --- Вывод -------------------------------------------------------------------

function showError(message) {
  const { code, hint } = classify(message);
  $("output").innerHTML =
    `<div class="trainer-error mono">${esc(message)}</div>` +
    (hint ? `<div class="diag-hint">${esc(hint)}</div>` : "");
  lastResult = null;
  report({ event: "error", error: code });
}

function renderResult(res, elapsed) {
  const out = $("output");
  lastResult = null;
  if (!res) {
    out.innerHTML = "";
    return;
  }
  const timing = `<span class="trainer-timing">${ms(elapsed)} мс</span>`;

  if (!res.fields || res.fields.length === 0) {
    const n = res.affectedRows;
    out.innerHTML = `<div class="trainer-note">Выполнено${
      n != null ? ` · строк затронуто: ${n}` : ""
    } ${timing}</div>`;
    return;
  }

  const cols = res.fields.map((f) => f.name);
  const shown = res.rows.slice(0, RENDER_LIMIT);
  lastResult = { cols, rows: res.rows };

  let html = '<div class="trainer-table-wrap"><table class="trainer-table"><thead><tr>';
  html += cols.map((c) => `<th>${esc(c)}</th>`).join("");
  html += "</tr></thead><tbody>";
  for (const row of shown) {
    html += "<tr>" + cols.map((c) => `<td>${esc(fmt(row[c]))}</td>`).join("") + "</tr>";
  }
  html += "</tbody></table></div>";
  html += `<div class="trainer-note">${rowsLabel(res.rows.length)} ${timing}`;
  if (res.rows.length > RENDER_LIMIT) html += ` · показаны первые ${RENDER_LIMIT}`;
  html += ' · <button type="button" class="link-button" id="csv">выгрузить CSV</button>';
  html += "</div>";
  out.innerHTML = html;
}

// --- Выполнение --------------------------------------------------------------

function busy(state) {
  for (const id of ["run", "explain", "measure", "reset"]) $(id).disabled = state;
}

async function execute() {
  const sql = $("sql").value.trim();
  if (!sql || !db) return;
  busy(true);
  try {
    const started = performance.now();
    const results = await db.exec(sql);
    const elapsed = performance.now() - started;
    const withRows = [...results].reverse().find((r) => r.fields && r.fields.length);
    renderResult(withRows || results[results.length - 1], elapsed);
    remember(sql);
    await refreshSchema();
    report({ event: "run" });
  } catch (e) {
    showError(e && e.message ? e.message : String(e));
  } finally {
    busy(false);
  }
}

async function planFor(sql) {
  // ANALYZE выполняет запрос по-настоящему — иначе в плане не будет фактического
  // числа строк, а именно расхождение оценки с фактом объясняет, почему запрос
  // медленный. Для изменяющих запросов ANALYZE не годится: план обошёлся бы
  // студенту лишними вставленными строками.
  const analyze = readOnly(sql);
  const options = analyze ? "ANALYZE, BUFFERS, FORMAT JSON" : "FORMAT JSON";
  const res = await db.query(`EXPLAIN (${options}) ${sql}`);
  return { plan: parsePlan(res.rows), analyzed: analyze };
}

async function explain() {
  const sql = $("sql").value.trim();
  if (!sql || !db) return;
  busy(true);
  try {
    const { plan, analyzed } = await planFor(sql);
    $("output").innerHTML =
      renderPlan(plan) +
      (analyzed
        ? ""
        : "<div class='diag-hint'>Запрос изменяет данные, поэтому план построен без " +
          "ANALYZE: фактического времени в нём нет. Выполнять запрос ради замера " +
          "тренажёр не станет — это изменило бы вашу базу.</div>");
    remember(sql);
  } catch (e) {
    showError(e && e.message ? e.message : String(e));
  } finally {
    busy(false);
  }
}

// --- Замер: что даёт индекс --------------------------------------------------

async function listIndexes() {
  const res = await db.query(
    "SELECT indexname FROM pg_indexes WHERE schemaname = 'public' ORDER BY indexname",
  );
  return res.rows.map((r) => r.indexname);
}

async function rowCounts(names) {
  const out = new Map();
  for (const name of new Set(names.filter(Boolean))) {
    try {
      const res = await db.query(`SELECT count(*) AS n FROM ${quoteIdent(name)}`);
      out.set(name, Number(res.rows[0].n));
    } catch {
      // таблицы могло не стать между планом и подсчётом — не беда
    }
  }
  return out;
}

/** «в 2,5 раза», «в 200 раз» — при дробном числе форма всегда «раза». */
function times(ratio) {
  if (ratio < 10) return `в ${ratio.toFixed(1).replace(".", ",")} раза`;
  const whole = Math.round(ratio);
  return `в ${whole} ${pluralRu(whole, "раз", "раза", "раз")}`;
}

function scanSummary(scans) {
  if (!scans.length) return "просмотров таблиц нет";
  return scans
    .map((s) => `${s.type}${s.relation ? " по " + s.relation : ""}${s.index ? ` (${s.index})` : ""}`)
    .join(", ");
}

function renderMeasure(now, before, counts) {
  let html = "<div class='measure'>";
  html += `<div class="measure-now"><b>${ms(now.median)} мс</b> — медиана ${MEASURE_RUNS} прогонов`;
  html += `<span class="measure-wall"> · ${ms(now.wall)} мс вместе с обменом с браузером</span></div>`;
  html += `<div class="measure-plan mono">${esc(scanSummary(now.scans))}</div>`;

  if (before) {
    // Пол в сотую миллисекунды: запрос по индексу к трём строкам укладывается в
    // ноль, и отношение выродилось бы в бесконечность.
    const ratio = Math.max(before.median, 0.01) / Math.max(now.median, 0.01);
    const faster = ratio >= 1.15;
    const slower = ratio <= 0.87;
    const added = now.indexes.filter((i) => !before.indexes.includes(i));
    const dropped = before.indexes.filter((i) => !now.indexes.includes(i));

    html += `<div class="measure-delta ${faster ? "ok" : slower ? "warn" : ""}">`;
    html += `Было ${ms(before.median)} мс → стало ${ms(now.median)} мс`;
    if (faster) html += ` — быстрее ${times(ratio)}`;
    else if (slower) html += ` — медленнее ${times(1 / ratio)}`;
    else html += " — разница в пределах разброса";
    html += "</div>";

    if (added.length) {
      html += `<div class="measure-note">Появился индекс: ${esc(added.join(", "))}.</div>`;
    }
    if (dropped.length) {
      html += `<div class="measure-note">Индекс удалён: ${esc(dropped.join(", "))}.</div>`;
    }
    const wasSeq = before.scans.some((s) => s.type === "Seq Scan");
    const nowIndex = now.scans.some((s) => /Index/.test(s.type));
    if (wasSeq && nowIndex) {
      html +=
        "<div class='measure-note ok'>Планировщик сменил последовательный просмотр на " +
        "поиск по индексу — ровно то, ради чего индекс и создавался.</div>";
    }
    if (added.length && !faster) {
      html +=
        "<div class='measure-note'>Индекс есть, а быстрее не стало. Обычные причины: " +
        "строк слишком мало, условие не совпадает с индексируемым выражением, или " +
        "запрос всё равно читает почти всю таблицу.</div>";
    }
  } else {
    html +=
      "<div class='measure-note'>Это первый замер. Создайте индекс и нажмите " +
      "«Замерить» ещё раз — покажу разницу.</div>";
  }

  const small = [...counts].filter(([, n]) => n < SMALL_TABLE);
  if (small.length && DATASETS[dataset] && DATASETS[dataset].bulk) {
    html +=
      `<div class="measure-note">В таблице ${esc(small[0][0])} всего ${small[0][1]} строк. ` +
      "На таком объёме индекс не нужен, и планировщик его не возьмёт — он прав. " +
      '<button type="button" class="link-button" id="bulk">Добавить 200 000 строк</button></div>';
  }

  html += "</div>";
  return html;
}

async function measure() {
  const sql = $("sql").value.trim();
  if (!sql || !db) return;
  if (!readOnly(sql)) {
    $("output").innerHTML =
      "<div class='diag-hint'>Замерять можно только читающие запросы: повторный прогон " +
      "INSERT или UPDATE изменил бы данные пять раз подряд.</div>";
    return;
  }
  busy(true);
  setStatus(`Замер: ${MEASURE_RUNS} прогонов…`);
  try {
    await db.query(sql); // прогрев: первый прогон читает мимо кеша буферов

    // Меряется время самой базы (Execution Time из плана), а не время до ответа
    // в JavaScript. Обмен с WebAssembly стоит около полутора десятков
    // миллисекунд независимо от запроса, и на таком фоне выигрыш от индекса
    // выглядит двукратным там, где на деле он десятикратный: постоянное
    // слагаемое одинаково подмешано и в «до», и в «после». Общее время рядом
    // остаётся — студент ждёт именно его.
    const runs = [];
    for (let i = 0; i < MEASURE_RUNS; i++) {
      const started = performance.now();
      const { plan } = await planFor(sql);
      runs.push({ exec: plan["Execution Time"] || 0, wall: performance.now() - started, plan });
    }
    runs.sort((a, b) => a.exec - b.exec);

    const middle = runs[Math.floor(MEASURE_RUNS / 2)];
    const scans = scanNodes(middle.plan);
    const now = {
      median: middle.exec,
      wall: middle.wall,
      scans,
      indexes: await listIndexes(),
    };
    const key = normalize(sql);
    const before = measured.get(key);
    measured.set(key, now);

    const counts = await rowCounts(scans.map((s) => s.relation));
    $("output").innerHTML = renderMeasure(now, before, counts);
    setStatus("Готово — выполняйте запросы", "ok");
    remember(sql);
  } catch (e) {
    showError(e && e.message ? e.message : String(e));
    setStatus("Готово — выполняйте запросы", "ok");
  } finally {
    busy(false);
  }
}

// --- Выгрузка и ссылка -------------------------------------------------------

function toCsv({ cols, rows }) {
  const cell = (v) => {
    const s = v === null || v === undefined ? "" : fmt(v);
    return /[";\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
  };
  // Разделитель — точка с запятой, и файл начинается с BOM: русский Excel читает
  // запятую как десятичный знак, а без BOM показывает кириллицу кракозябрами.
  const lines = [cols.map(cell).join(";")];
  for (const row of rows) lines.push(cols.map((c) => cell(row[c])).join(";"));
  return "﻿" + lines.join("\r\n");
}

function downloadCsv() {
  if (!lastResult) return;
  saveFile("result.csv", toCsv(lastResult), "text/csv;charset=utf-8");
}

function saveFile(name, text, type) {
  const link = document.createElement("a");
  link.href = URL.createObjectURL(new Blob([text], { type }));
  link.download = name;
  link.click();
  setTimeout(() => URL.revokeObjectURL(link.href), 1000);
}

async function downloadDump() {
  if (!db) return;
  $("dump").disabled = true;
  setStatus("Собираю скрипт…");
  try {
    const { sql, tables, rows, truncated } = await dumpDatabase(db);
    if (!tables) {
      setStatus("Таблиц нет — выгружать нечего", "err");
      return;
    }
    saveFile(`dataedu-${dataset}.sql`, sql, "application/sql;charset=utf-8");
    setStatus(
      `Выгружено: ${tables} ${pluralRu(tables, "таблица", "таблицы", "таблиц")}, ${rowsLabel(rows)}` +
        (truncated.length ? " (часть данных усечена)" : ""),
      "ok",
    );
  } catch (e) {
    setStatus("Не удалось выгрузить: " + (e && e.message ? e.message : e), "err");
  } finally {
    $("dump").disabled = false;
  }
}

/** Запрос в адресной строке: преподаватель отвечает ссылкой, а не пересказом. */
async function shareLink() {
  const sql = $("sql").value.trim();
  if (!sql) return;
  const url = new URL(location.href);
  url.hash = `d=${dataset}&q=${encodeURIComponent(sql)}`;
  window.history.replaceState(null, "", url.toString());
  try {
    await navigator.clipboard.writeText(url.toString());
    setStatus("Ссылка на запрос скопирована", "ok");
  } catch {
    // Буфер обмена требует разрешения и защищённого соединения — но ссылка уже
    // в адресной строке, скопировать её можно руками.
    setStatus("Ссылка в адресной строке — скопируйте её", "ok");
  }
}

function readHash() {
  const hash = location.hash.replace(/^#/, "");
  if (!hash) return {};
  const params = new URLSearchParams(hash);
  return { sql: params.get("q"), dataset: params.get("d") };
}

// --- Запуск ------------------------------------------------------------------

function chooseDataset() {
  const fromHash = readHash().dataset;
  if (fromHash && DATASETS[fromHash]) return fromHash;
  try {
    const saved = localStorage.getItem("trainer-dataset");
    if (saved && DATASETS[saved]) return saved;
  } catch {
    // приватный режим
  }
  return DEFAULT_DATASET;
}

function fillDatasetSelect() {
  const select = $("dataset");
  select.innerHTML = Object.entries(DATASETS)
    .map(([key, d]) => `<option value="${key}">${esc(d.title)} — ${esc(d.note)}</option>`)
    .join("");
  select.value = dataset;
}

async function switchDataset(key) {
  busy(true);
  setStatus("Меняю набор данных…");
  await seed(key);
  $("output").innerHTML = "";
  measured.clear();
  await refreshSchema();
  // Пустое поле на пустой базе не подсказывает ничего. Заготовка ставится
  // только если студент ещё ничего не написал — затирать его текст нельзя.
  const starter = DATASETS[key].starter;
  if (starter && !$("sql").value.trim()) $("sql").value = starter;
  setStatus(`Набор «${DATASETS[key].title}» готов`, "ok");
  busy(false);
}

async function reset() {
  busy(true);
  setStatus("Сброс базы…");
  await seed(dataset);
  $("output").innerHTML = "";
  measured.clear();
  await refreshSchema();
  setStatus("База сброшена — готово", "ok");
  busy(false);
}

async function init() {
  const wanted = chooseDataset();
  try {
    setStatus("Загружаю PostgreSQL (16 МБ)…");
    const artifacts = await preload(setProgress);
    setStatus("Запускаю сервер…");

    db = await openDb(artifacts);
    const existing = await currentDataset();
    if (existing === wanted) {
      dataset = existing;
      restored = true;
    } else {
      await seed(wanted);
    }

    fillDatasetSelect();
    await refreshSchema();

    const { sql } = readHash();
    if (sql) $("sql").value = sql;

    $("boot").hidden = true;
    setStatus(
      restored ? "База восстановлена — выполняйте запросы" : "Готово — выполняйте запросы",
      "ok",
    );
    busy(false);
  } catch (e) {
    $("boot").hidden = true;
    setStatus("Не удалось загрузить PGlite: " + (e && e.message ? e.message : e), "err");
  }
}

// --- События -----------------------------------------------------------------

$("run").addEventListener("click", execute);
$("explain").addEventListener("click", explain);
$("measure").addEventListener("click", measure);
$("reset").addEventListener("click", reset);
$("share").addEventListener("click", shareLink);
$("schema-view").addEventListener("click", toggleSchemaView);
$("dump").addEventListener("click", downloadDump);
$("dataset").addEventListener("change", (e) => switchDataset(e.target.value));

$("schema").addEventListener("click", (e) => {
  if (e.target.id !== "er-reset") return;
  try {
    localStorage.removeItem(layoutKey());
  } catch {
    // нечего удалять — раскладка и так только в разметке
  }
  refreshSchema();
});

$("output").addEventListener("click", (e) => {
  if (e.target.id === "csv") downloadCsv();
  if (e.target.id === "bulk") {
    $("sql").value = DATASETS[dataset].bulk;
    $("sql").focus();
    setStatus("Выполните вставку, затем ANALYZE; и снова «Замерить»", "ok");
  }
});

$("history-list").addEventListener("click", (e) => {
  const item = e.target.closest(".history-item");
  if (!item) return;
  $("sql").value = queries[Number(item.dataset.i)];
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
    if (!queries.length) return;
    e.preventDefault();
    historyPos =
      e.key === "ArrowUp"
        ? Math.min(historyPos + 1, queries.length - 1)
        : Math.max(historyPos - 1, -1);
    $("sql").value = historyPos === -1 ? "" : queries[historyPos];
  }
});

init();
