// Расчёт эталона задания в браузере преподавателя.
//
// Зачем не на сервере. Серверный расчёт (assessments/expected.py) исполняет SQL
// в PostgreSQL, а в профиле разработки база файловая — и кнопка «Посчитать эталон»
// там просто падает с ошибкой подключения. Но дело не только в удобстве: студент
// выполняет свой запрос в PGlite, и эталон, посчитанный другим движком, может с
// ним разойтись на мелочах — форматировании numeric, порядке столбцов у `SELECT *`,
// точности round(). Здесь эталон считает **тот же движок**, что и у студента.
//
// Модель доверия не меняется: считает преподаватель, он же эталон и задаёт.
// Студенту этот код недоступен — страница живёт в админке.
//
// Ещё одно отличие от серверной кнопки: расчёт идёт по тому, что сейчас в полях
// формы, а не по сохранённому. Можно набросать задачу и сразу посмотреть, что
// вернёт эталонный запрос, не сохраняя черновик.

import { PGlite } from "../vendor/pglite/index.js";

(function () {
  const root = document.getElementById("expected-tool");
  if (!root) return;

  const saveUrl = root.dataset.saveUrl;
  const csrf = root.dataset.csrf;
  const out = document.getElementById("expected-out");
  const button = document.getElementById("expected-run");

  const field = (name) => document.getElementById("id_" + name);
  const esc = (v) =>
    String(v).replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" })[c]);
  const fmt = (v) => (v === null || v === undefined ? "NULL" : typeof v === "object" ? JSON.stringify(v) : String(v));

  function say(html, kind) {
    out.innerHTML = `<div class="expected-msg ${kind || ""}">${html}</div>`;
  }

  function table(columns, rows) {
    let html = "<table class='expected-table'><thead><tr>";
    html += columns.map((c) => `<th>${esc(c)}</th>`).join("") + "</tr></thead><tbody>";
    for (const row of rows.slice(0, 30)) {
      html += "<tr>" + row.map((v) => `<td>${esc(fmt(v))}</td>`).join("") + "</tr>";
    }
    html += "</tbody></table>";
    if (rows.length > 30) html += `<p>… и ещё ${rows.length - 30}</p>`;
    return html;
  }

  async function compute() {
    const setup = (field("setup_sql")?.value || "").trim();
    const expected = (field("expected_sql")?.value || "").trim();

    if (!setup) return say("Не заполнена заготовка данных (setup_sql).", "err");
    if (!expected) return say("Не заполнен эталонный запрос (expected_sql).", "err");

    button.disabled = true;
    say("Запускаю PostgreSQL в браузере…");
    try {
      // Каждый расчёт — на чистой базе: остатки предыдущего прогона исказили бы эталон.
      const db = await PGlite.create();
      await db.exec(setup);

      const results = await db.exec(expected);
      const res = [...results].reverse().find((r) => r.fields && r.fields.length);
      if (!res) {
        return say(
          "Эталонный запрос не вернул таблицу. Для задания с автопроверкой нужен SELECT.",
          "err",
        );
      }

      const columns = res.fields.map((f) => f.name);
      const rows = res.rows.map((r) => columns.map((c) => r[c]));

      const resp = await fetch(saveUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRFToken": csrf },
        body: JSON.stringify({ columns, rows }),
      });
      const data = await resp.json();
      if (!resp.ok || !data.ok) {
        return say(esc(data.error || "Не удалось сохранить эталон."), "err");
      }

      out.innerHTML =
        `<div class="expected-msg ok">Эталон посчитан и сохранён: ${esc(data.summary)}.</div>` +
        table(columns, rows) +
        "<p>Проверьте таблицу глазами: именно с ней будут сравниваться ответы студентов.</p>";
    } catch (e) {
      say("SQL не выполнился: " + esc(e && e.message ? e.message : String(e)), "err");
    } finally {
      button.disabled = false;
    }
  }

  button.addEventListener("click", compute);
})();
