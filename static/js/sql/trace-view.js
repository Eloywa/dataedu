// Экран «Как выполняется»: проигрыватель шагов поверх ER-диаграммы.
//
// Шаги собирает trace.js, здесь только показ. Смысл в том, что запрос, диаграмма и
// строки стоят рядом и меняются вместе: на каждом шаге видно, какая часть текста
// запроса сейчас работает, какие таблицы и столбцы она трогает и что стало со строками.
//
// Управление — и кнопками, и стрелками на клавиатуре, а по таблице на диаграмме можно
// нажать, чтобы перейти к шагу, где она читается. Автовоспроизведение запускает только
// сам человек: шаги, сменяющиеся без спроса, читать невозможно.

import { bindDiagram, fitDiagram, highlightDiagram, renderDiagram } from "./schema.js";
import { pluralRu, rowsLabel } from "../plural.js";

const PLAY_DELAY = 3000;

const esc = (v) => String(v).replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" })[c]);

/** Текст запроса с выделенными частями. Отрезки идут по порядку и не пересекаются. */
function markedSql(sql, marks) {
  const sorted = [...marks].sort((a, b) => a[0] - b[0]);
  let out = "";
  let last = 0;
  for (const [start, end] of sorted) {
    if (start < last) continue;
    const piece = sql.slice(start, end);
    const body = piece.trimEnd(); // пробелы перед следующей частью не подсвечиваем
    out += `${esc(sql.slice(last, start))}<mark class="trace-mark">${esc(body)}</mark>`;
    out += esc(piece.slice(body.length));
    last = end;
  }
  return out + esc(sql.slice(last));
}

function sampleTable(sample, usedColumns) {
  let html = '<div class="trainer-table-wrap"><table class="trainer-table trace-table"><thead><tr>';
  if (sample.marked) html += '<th class="trace-state"><span class="visually-hidden">Прошла ли строка условие</span></th>';
  html += sample.columns
    .map((c) => `<th${usedColumns.has(c) ? ' class="is-used"' : ""}>${esc(c)}</th>`)
    .join("");
  html += "</tr></thead><tbody>";

  for (const row of sample.rows) {
    const state = row.state ? ` class="is-${row.state}"` : "";
    html += `<tr${state}>`;
    if (sample.marked) {
      const passed = row.state === "kept";
      html +=
        `<td class="trace-state" title="${passed ? "подошла" : "отброшена"}">${passed ? "✓" : "✗"}` +
        `<span class="visually-hidden">${passed ? " подошла" : " отброшена"}</span></td>`;
    }
    html += row.cells.map((cell) => `<td>${esc(cell)}</td>`).join("");
    html += "</tr>";
  }
  html += "</tbody></table></div>";

  if (sample.marked) {
    html += '<p class="trainer-note">Показано начало таблицы: ✓ — строка подошла, ✗ — отброшена.</p>';
  } else if (sample.total > sample.rows.length) {
    html += `<p class="trainer-note">Показаны первые ${sample.rows.length} из ${rowsLabel(sample.total)}.</p>`;
  }
  return html;
}

function flowHtml(step) {
  const unit = (n) => pluralRu(n, "строка", "строки", "строк");
  if (step.rowsIn == null) {
    return `<p class="trace-flow"><b>${step.rowsOut}</b> ${unit(step.rowsOut)}</p>`;
  }
  const before = step.inputs
    ? step.inputs.map((n) => `<b>${n}</b>`).join(' <span class="trace-plus">+</span> ')
    : `<b>${step.rowsIn}</b> ${unit(step.rowsIn)}`;
  return (
    `<p class="trace-flow">${before}` +
    `<span class="trace-arrow" aria-hidden="true">→</span>` +
    `<span class="visually-hidden">, стало </span><b>${step.rowsOut}</b> ${unit(step.rowsOut)}</p>`
  );
}

function detailHtml(step) {
  const used = new Set((step.columns || []).map((c) => c.column));
  let html = `<h2 class="trace-title">${esc(step.title)}</h2>`;
  html += `<p class="trace-text">${esc(step.text)}</p>`;
  html += flowHtml(step);
  if (step.note) html += `<p class="trace-note">${esc(step.note)}</p>`;
  if (step.sample && step.sample.rows.length) html += sampleTable(step.sample, used);
  return html;
}

/**
 * Показать шаги в контейнере.
 * @param {Element} host куда
 * @param {object} trace результат buildTrace
 * @param {{schema: object, saved: object, onMove: Function, maxHeight: () => number}} options
 * @returns {{destroy: () => void}}
 */
export function mountTrace(host, trace, { schema, saved, onMove, maxHeight }) {
  const { steps } = trace;
  const peak = Math.max(1, ...steps.map((s) => s.rowsOut || 0));
  let index = 0;
  let timer = null;

  host.innerHTML =
    '<div class="trace">' +
    `<pre class="trace-sql mono"></pre>` +
    '<div class="trace-controls">' +
    '<button type="button" class="btn btn-ghost btn-small" data-go="first">В начало</button>' +
    '<button type="button" class="btn btn-ghost btn-small" data-go="prev">← Назад</button>' +
    '<button type="button" class="btn btn-primary btn-small" data-go="play">Воспроизвести</button>' +
    '<button type="button" class="btn btn-ghost btn-small" data-go="next">Далее →</button>' +
    '<span class="trace-counter" role="status"></span>' +
    "</div>" +
    '<ol class="trace-steps">' +
    steps
      .map(
        (step, i) =>
          `<li><button type="button" class="trace-chip" data-step="${i}">` +
          `<span class="trace-chip-name">${esc(step.chip || step.title)}</span>` +
          `<span class="trace-chip-rows">${rowsLabel(step.rowsOut || 0)}</span>` +
          `<span class="trace-chip-bar"><i style="width:${Math.max(3, ((step.rowsOut || 0) / peak) * 100).toFixed(0)}%"></i></span>` +
          "</button></li>",
      )
      .join("") +
    "</ol>" +
    '<div class="trace-body">' +
    `<div class="trace-map">${renderDiagram(schema, saved, { note: false })}</div>` +
    '<div class="trace-detail" aria-live="polite"></div>' +
    "</div>" +
    `<p class="trainer-note">Планирование ${trace.planningMs.toFixed(1)} мс, выполнение ${trace.executionMs.toFixed(1)} мс. ` +
    "Всё показанное здесь — настоящий план этого запроса, база при этом не изменилась.</p>" +
    "</div>";

  const root = host.querySelector(".trace");
  const sqlBox = root.querySelector(".trace-sql");
  const counter = root.querySelector(".trace-counter");
  const detail = root.querySelector(".trace-detail");
  const map = root.querySelector(".trace-map");
  const chips = [...root.querySelectorAll(".trace-chip")];
  const playButton = root.querySelector('[data-go="play"]');

  function show(i) {
    index = Math.max(0, Math.min(i, steps.length - 1));
    const step = steps[index];

    sqlBox.innerHTML = markedSql(trace.sql, step.marks || []);
    counter.textContent = `Шаг ${index + 1} из ${steps.length}`;
    detail.innerHTML = detailHtml(step);

    chips.forEach((chip, n) => {
      chip.classList.toggle("is-active", n === index);
      chip.classList.toggle("is-done", n < index);
      if (n === index) chip.setAttribute("aria-current", "step");
      else chip.removeAttribute("aria-current");
    });
    // Только по горизонтали: `scrollIntoView` подвинул бы всю страницу.
    const chip = chips[index];
    const strip = chip.closest(".trace-steps");
    strip.scrollLeft = chip.offsetLeft - strip.offsetLeft - strip.clientWidth / 2 + chip.clientWidth / 2;

    highlightDiagram(map, {
      tables: step.tables,
      active: step.active,
      columns: step.columns,
      links: step.links,
    });

    // На телефоне диаграмма шире экрана: подводим к ней таблицу, с которой идёт работа,
    // иначе выделение могло оказаться за краем.
    const table = map.querySelector("g.er-table.is-active");
    const scroller = map.querySelector(".er-scroll");
    if (table && scroller && scroller.scrollWidth > scroller.clientWidth) {
      const box = table.getBoundingClientRect();
      const frame = scroller.getBoundingClientRect();
      scroller.scrollLeft += box.left + box.width / 2 - (frame.left + frame.width / 2);
    }

    root.querySelector('[data-go="prev"]').disabled = index === 0;
    root.querySelector('[data-go="first"]').disabled = index === 0;
    root.querySelector('[data-go="next"]').disabled = index === steps.length - 1;
  }

  function stop() {
    if (timer) clearInterval(timer);
    timer = null;
    playButton.textContent = "Воспроизвести";
  }

  function play() {
    if (timer) {
      stop();
      return;
    }
    if (index === steps.length - 1) show(0);
    playButton.textContent = "Пауза";
    timer = setInterval(() => {
      if (index >= steps.length - 1) stop();
      else show(index + 1);
    }, PLAY_DELAY);
  }

  root.addEventListener("click", (event) => {
    const button = event.target.closest("button");
    if (!button) return;
    if (button.dataset.step !== undefined) {
      stop();
      show(Number(button.dataset.step));
      return;
    }
    const go = button.dataset.go;
    if (go === "play") return play();
    if (!go) return;
    stop();
    if (go === "first") show(0);
    if (go === "prev") show(index - 1);
    if (go === "next") show(index + 1);
  });

  root.addEventListener("keydown", (event) => {
    if (event.key === "ArrowLeft") {
      event.preventDefault();
      stop();
      show(index - 1);
    } else if (event.key === "ArrowRight") {
      event.preventDefault();
      stop();
      show(index + 1);
    }
  });

  bindDiagram(map, onMove, (name) => {
    const found = steps.findIndex((step) => (step.active || []).includes(name));
    if (found >= 0) {
      stop();
      show(found);
    }
  });

  // Вписывается заново только при смене ширины: сама подгонка меняет высоту контейнера,
  // и реакция на любое изменение размера зациклилась бы.
  let width = 0;
  const fit = () => {
    if (map.clientWidth === width) return;
    width = map.clientWidth;
    fitDiagram(map, { maxHeight: maxHeight() });
  };
  const observer = new ResizeObserver(fit);
  observer.observe(map);
  fit();
  show(0);

  return {
    destroy() {
      stop();
      observer.disconnect();
    },
  };
}
