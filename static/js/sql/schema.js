// Схема базы: список таблиц и ER-диаграмма.
//
// И то и другое читается из самой базы после каждого успешного запроса, а не
// вписано в шаблон. Раньше в разметке лежали две демонстрационные таблицы, и
// созданная студентом третья в списке не появлялась — панель врала ровно тогда,
// когда становилась нужна.
//
// Диаграмма нужна не для украшения. Курс начинается со связей между таблицами,
// а увидеть связь в тексте CREATE TABLE студент не может: REFERENCES — это одно
// слово в середине определения. На диаграмме то же самое — линия.

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
//
// Связи рисуются ортогонально: отвод вбок от строки столбца, вертикальная
// дорожка, заход в столбец-ключ. Первая версия соединяла точки кривой Безье и
// выбирала сторону по центрам коробок — при вертикальном расположении таблиц
// выход оказывался слева, а вход справа, и линия делала петлю вокруг коробки.
// Теперь сторона выбирается по тому, с какой стороны дорожка короче для обеих
// таблиц сразу, и вход всегда с той же стороны, что и выход: линия огибает
// коробки, а не наматывается на них.
//
// Таблицы перетаскиваются. Автоматическая раскладка по ярусам угадывает не
// всегда, а разбор схемы на занятии — это как раз перекладывание таблиц.
// Расположение запоминается отдельно для каждого набора данных.

const CHAR = 7.1; // ширина знака в 12px моноширинном начертании, с запасом
const ROW = 17;
const HEAD = 26;
const PAD_X = 14;
const GAP_X = 44;
const GAP_Y = 64;
const STUB = 16; // отвод от края коробки до вертикальной дорожки
const LANE = 14; // зазор между дорожкой и самой дальней коробкой
const MARGIN = 90; // запас холста, чтобы было куда перетаскивать

// Поля слева и справа под вертикальные дорожки. Без них связь от самой левой
// таблицы уводила дорожку в отрицательные координаты, и линия обрезалась краем
// холста — обрыв выглядел как несуществующая связь. Перетаскивание ограничено
// теми же полями, иначе таблица заняла бы место дорожки.
const PAD = STUB + LANE + 8;

function box(table) {
  const lines = table.columns.map((c) => `${c.name}  ${c.type}`);
  const widest = Math.max(table.name.length + 4, ...lines.map((l) => l.length));
  return {
    table,
    w: Math.max(150, Math.round(widest * CHAR) + PAD_X * 2),
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

/** Смещение строки столбца от верха коробки. */
function columnOffset(table, name) {
  const i = table.columns.findIndex((c) => c.name === name);
  return HEAD + (i < 0 ? 0 : i) * ROW + ROW / 2 - 2;
}

/**
 * Ортогональный путь со скруглёнными углами: отвод вбок, вертикальная дорожка,
 * заход обратно. Радиус ужимается, если поворот короче него, — иначе дуга
 * вылезает за собственный отрезок, и получается та самая петля.
 */
function orthPath(x1, y1, x2, y2, lane, dir) {
  const vy = Math.sign(y2 - y1) || 1;
  const r = Math.min(9, Math.abs(y2 - y1) / 2, Math.abs(lane - x1), Math.abs(lane - x2));
  if (!(r > 1)) return `M ${x1} ${y1} H ${lane} V ${y2} H ${x2}`;
  return (
    `M ${x1} ${y1} H ${lane - dir * r} ` +
    `Q ${lane} ${y1} ${lane} ${y1 + vy * r} V ${y2 - vy * r} ` +
    `Q ${lane} ${y2} ${lane - dir * r} ${y2} H ${x2}`
  );
}

/** Геометрия одной связи по текущему положению коробок. */
function routeLink(from, to, fromOffset, toOffset) {
  const y1 = from.y + fromOffset;
  const y2 = to.y + toOffset;

  // С какой стороны обход дешевле для обеих коробок сразу.
  const right = Math.max(from.x + from.w, to.x + to.w);
  const left = Math.min(from.x, to.x);
  const costRight = right - (from.x + from.w) + (right - (to.x + to.w));
  const costLeft = from.x - left + (to.x - left);
  const dir = costRight <= costLeft ? 1 : -1;

  const x1 = dir > 0 ? from.x + from.w : from.x;
  const x2 = dir > 0 ? to.x + to.w : to.x;
  const lane = dir > 0 ? Math.max(x1, x2) + STUB + LANE : Math.min(x1, x2) - STUB - LANE;

  return { d: orthPath(x1, y1, x2, y2, lane, dir), x1, y1, x2, y2 };
}

export function renderDiagram(schema, saved) {
  if (!schema.tables.length) {
    return "<div class='schema-empty'>Таблиц нет — рисовать нечего.</div>";
  }
  const { boxes, width, height } = layout(schema);

  // Сохранённое положение перебивает автоматическое: если студент разложил
  // таблицы сам, следующий же запрос не должен смешать их обратно.
  for (const [name, pos] of Object.entries(saved || {})) {
    const b = boxes.get(name);
    if (b && Number.isFinite(pos.x) && Number.isFinite(pos.y)) {
      b.x = pos.x;
      b.y = pos.y;
    }
  }

  const placed = [...boxes.values()];
  const canvasW = Math.max(width, ...placed.map((b) => b.x + b.w)) + MARGIN;
  const canvasH = Math.max(height, ...placed.map((b) => b.y + b.h)) + MARGIN;

  let edges = "";
  schema.links.forEach((link, i) => {
    const from = boxes.get(link.src);
    const to = boxes.get(link.dst);
    if (!from || !to || from === to) return;
    const fromOffset = columnOffset(from.table, link.srcCol);
    const toOffset = columnOffset(to.table, link.dstCol);
    const geom = routeLink(from, to, fromOffset, toOffset);
    edges +=
      `<g class="er-edge" data-i="${i}" data-src="${esc(link.src)}" data-dst="${esc(link.dst)}" ` +
      `data-fo="${fromOffset}" data-to="${toOffset}">` +
      `<title>${esc(link.src)}.${esc(link.srcCol)} → ${esc(link.dst)}.${esc(link.dstCol)}</title>` +
      `<path class="er-link" d="${geom.d}" />` +
      `<circle class="er-dot" cx="${geom.x1}" cy="${geom.y1}" r="3.5" />` +
      `<circle class="er-dot er-dot-one" cx="${geom.x2}" cy="${geom.y2}" r="3.5" />` +
      "</g>";
  });

  let nodes = "";
  for (const b of boxes.values()) {
    nodes +=
      `<g class="er-table" data-name="${esc(b.table.name)}" data-x="${b.x}" data-y="${b.y}" ` +
      `data-w="${b.w}" data-h="${b.h}" transform="translate(${b.x} ${b.y})">`;
    nodes += `<rect class="er-box" x="0" y="0" width="${b.w}" height="${b.h}" rx="7" />`;
    nodes += `<rect class="er-head" x="0" y="0" width="${b.w}" height="${HEAD}" rx="7" />`;
    nodes += `<text class="er-title" x="${PAD_X}" y="17">${esc(b.table.name)}</text>`;
    b.table.columns.forEach((c, i) => {
      const y = HEAD + i * ROW + 12;
      const mark = b.table.pk.has(c.name) ? "PK" : b.table.fk.has(c.name) ? "FK" : "";
      nodes += `<text class="er-col${mark ? " er-key" : ""}" x="${PAD_X}" y="${y}">${esc(c.name)}</text>`;
      if (mark) nodes += `<text class="er-mark" x="${b.w - PAD_X}" y="${y}">${mark}</text>`;
    });
    nodes += "</g>";
  }

  const links = schema.links.length;
  return (
    `<div class="er-scroll"><svg class="er" data-pad="${PAD}" ` +
    `viewBox="${-PAD} 0 ${canvasW + PAD * 2} ${canvasH}" ` +
    `width="${canvasW + PAD * 2}" height="${canvasH}" role="img" ` +
    `aria-label="Диаграмма схемы: ${schema.tables.length} таблиц, ${links} связей">` +
    edges +
    nodes +
    "</svg></div>" +
    `<div class="trainer-note">Таблиц: ${schema.tables.length} · связей по внешним ключам: ${links}. ` +
    "Линия идёт от ссылающегося столбца к ключу, на который он ссылается: залитая " +
    "точка — сторона «многие», полая — «один». Таблицы можно перетаскивать." +
    ' <button type="button" class="link-button" id="er-reset">Разложить заново</button></div>'
  );
}

/**
 * Включает перетаскивание таблиц.
 *
 * Геометрия читается из самой разметки (data-атрибуты у групп и связей), а не
 * держится отдельным состоянием: панель схемы перерисовывается после каждого
 * запроса, и любое состояние рядом с ней разошлось бы с разметкой.
 *
 * @param {Element} root контейнер с диаграммой
 * @param {(positions: object) => void} onMove вызывается по окончании переноса
 */
export function bindDiagram(root, onMove) {
  const svg = root.querySelector("svg.er");
  if (!svg) return;

  const groups = new Map();
  svg.querySelectorAll("g.er-table").forEach((g) => groups.set(g.dataset.name, g));
  const rectOf = (g) => ({ x: +g.dataset.x, y: +g.dataset.y, w: +g.dataset.w, h: +g.dataset.h });

  function redraw(names) {
    svg.querySelectorAll("g.er-edge").forEach((edge) => {
      if (names && !names.has(edge.dataset.src) && !names.has(edge.dataset.dst)) return;
      const from = groups.get(edge.dataset.src);
      const to = groups.get(edge.dataset.dst);
      if (!from || !to) return;
      const geom = routeLink(rectOf(from), rectOf(to), +edge.dataset.fo, +edge.dataset.to);
      edge.querySelector(".er-link").setAttribute("d", geom.d);
      const dots = edge.querySelectorAll("circle");
      dots[0].setAttribute("cx", geom.x1);
      dots[0].setAttribute("cy", geom.y1);
      dots[1].setAttribute("cx", geom.x2);
      dots[1].setAttribute("cy", geom.y2);
    });
  }

  // Экранные пиксели → координаты viewBox: диаграмма ужимается под ширину
  // панели, и без пересчёта таблица уезжала бы не туда, куда ведут курсор.
  const point = svg.createSVGPoint();
  function toSvg(event) {
    point.x = event.clientX;
    point.y = event.clientY;
    return point.matrixTransform(svg.getScreenCTM().inverse());
  }

  const bounds = svg.viewBox.baseVal;
  const pad = +svg.dataset.pad || 0;
  const clamp = (v, lo, hi) => Math.max(lo, Math.min(v, hi));
  let drag = null;

  svg.addEventListener("pointerdown", (event) => {
    const g = event.target.closest("g.er-table");
    if (!g) return;
    event.preventDefault();
    const p = toSvg(event);
    drag = { g, dx: p.x - +g.dataset.x, dy: p.y - +g.dataset.y, moved: false };
    g.classList.add("is-dragging");
    // Порядок в разметке — это и порядок отрисовки: без переноса в конец
    // таблица уезжала бы под соседнюю, за которую её же и тянут.
    svg.appendChild(g);
    svg.setPointerCapture(event.pointerId);
  });

  svg.addEventListener("pointermove", (event) => {
    if (!drag) return;
    const p = toSvg(event);
    const g = drag.g;
    const x = clamp(p.x - drag.dx, bounds.x + pad, bounds.x + bounds.width - pad - +g.dataset.w);
    const y = clamp(p.y - drag.dy, 0, bounds.height - +g.dataset.h);
    g.dataset.x = x;
    g.dataset.y = y;
    g.setAttribute("transform", `translate(${x} ${y})`);
    drag.moved = true;
    redraw(new Set([g.dataset.name]));
  });

  function finish(event) {
    if (!drag) return;
    drag.g.classList.remove("is-dragging");
    if (svg.hasPointerCapture(event.pointerId)) svg.releasePointerCapture(event.pointerId);
    if (drag.moved && onMove) {
      const positions = {};
      for (const [name, g] of groups) positions[name] = { x: +g.dataset.x, y: +g.dataset.y };
      onMove(positions);
    }
    drag = null;
  }

  svg.addEventListener("pointerup", finish);
  svg.addEventListener("pointercancel", finish);
}
