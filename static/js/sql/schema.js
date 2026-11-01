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

const esc = (v) => String(v).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);

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

export function renderList(schema, hint) {
  if (!schema.tables.length) {
    // В пустом режиме совет «сбросьте базу» бессмыслен — сброс вернёт ту же
    // пустоту. Там подсказывать надо первый шаг, а не выход из положения.
    return `<div class="schema-empty">${esc(hint || "Таблиц нет. Создайте их или нажмите «Сбросить базу».")}</div>`;
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
// Таблицы стоят колонками слева направо: справочники слева, журналы справа. Раньше
// ярусы шли сверху вниз, и на широком экране диаграмма занимала узкую полосу
// посередине, а чтобы вместить её по высоте, текст приходилось ужимать до нечитаемого.
//
// Связи рисуются ортогонально: выход из обращённой к соседу стороны, вертикальная
// дорожка в промежутке, заход в столбец-ключ. Если коробки перетащили так, что
// промежутка между ними нет, линия огибает их снаружи — вход с той же стороны, что и
// выход, иначе она наматывалась бы на коробку.
//
// Таблицы перетаскиваются. Автоматическая раскладка угадывает не всегда, а разбор
// схемы на занятии — это как раз перекладывание таблиц. Расположение запоминается
// отдельно для каждого набора данных.

const CHAR = 7.9; // ширина знака в 13px моноширинном начертании, с запасом
const ROW = 22;
const HEAD = 32;
const PAD_X = 14;
const MARK_W = 26; // колонка под метку PK/FK у правого края коробки
const GAP_X = 72;
const GAP_Y = 28;
const STUB = 16; // отвод от края коробки до вертикальной дорожки
const LANE = 14; // зазор между дорожкой и самой дальней коробкой
const MARGIN = 24; // запас холста, чтобы было куда перетаскивать
const COLUMN_MAX = 4; // больше таблиц в колонку не ставим: она ушла бы за экран

// Поля слева и справа под вертикальные дорожки. Без них связь от самой левой
// таблицы уводила дорожку в отрицательные координаты, и линия обрезалась краем
// холста — обрыв выглядел как несуществующая связь. Перетаскивание ограничено
// теми же полями, иначе таблица заняла бы место дорожки.
const PAD = STUB + LANE + 8;

// Длинные имена типов из information_schema ничего не добавляют, зато раздвигают
// коробку почти вдвое — а тип показывается мелкой подсказкой рядом со столбцом.
const SHORT_TYPES = {
  "character varying": "varchar",
  "timestamp without time zone": "timestamp",
  "timestamp with time zone": "timestamptz",
  "time without time zone": "time",
  "double precision": "double",
};

function shortType(type) {
  return SHORT_TYPES[type] || type;
}

function box(table) {
  const widest = Math.max(
    table.name.length + 4,
    ...table.columns.map((c) => c.name.length + 2 + shortType(c.type).length),
  );
  return {
    table,
    w: Math.max(180, Math.round(widest * CHAR) + PAD_X * 2 + MARK_W),
    h: HEAD + table.columns.length * ROW + 10,
    x: 0,
    y: 0,
  };
}

/**
 * Раскладка колонками: таблица стоит правее всех, на кого ссылается.
 * Циклы (таблица, ссылающаяся сама на себя, или взаимные ссылки) ограничены
 * глубиной, иначе обход не закончится.
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

  // Высокая колонка делится на несколько: восемь таблиц без связей иначе вытянулись
  // бы столбиком, и уместить их на экране можно было бы только мелким шрифтом.
  const columns = [];
  for (const tier of tiers) {
    if (!tier) continue;
    tier.sort((a, b) => a.table.name.localeCompare(b.table.name));
    for (let i = 0; i < tier.length; i += COLUMN_MAX) columns.push(tier.slice(i, i + COLUMN_MAX));
  }

  const heightOf = (column) => column.reduce((s, b) => s + b.h, 0) + GAP_Y * (column.length - 1);
  const height = Math.max(...columns.map(heightOf));

  // Колонки центрируются по высоте: иначе диаграмма клинится к верхнему краю.
  let x = 0;
  for (const column of columns) {
    const width = Math.max(...column.map((b) => b.w));
    let y = (height - heightOf(column)) / 2 + 10;
    for (const b of column) {
      b.x = x + (width - b.w) / 2;
      b.y = y;
      y += b.h + GAP_Y;
    }
    x += width + GAP_X;
  }

  return { boxes, width: x - GAP_X + 20, height: height + 20 };
}

/** Смещение строки столбца от верха коробки. */
function columnOffset(table, name) {
  const i = table.columns.findIndex((c) => c.name === name);
  return HEAD + (i < 0 ? 0 : i) * ROW + ROW / 2 + 2;
}

/**
 * Ортогональный путь со скруглёнными углами: отвод вбок, вертикальная дорожка,
 * заход к цели. Радиус ужимается, если поворот короче него, — иначе дуга вылезает
 * за собственный отрезок и получается петля.
 *
 * `leave` и `enter` — направление движения по горизонтали на первом и последнем
 * отрезках: совпадают, когда линия идёт через промежуток, и различаются, когда
 * она огибает коробки снаружи.
 */
function orthPath(x1, y1, x2, y2, lane, leave, enter) {
  const vy = Math.sign(y2 - y1) || 1;
  const r = Math.min(9, Math.abs(y2 - y1) / 2, Math.abs(lane - x1), Math.abs(lane - x2));
  if (!(r > 1)) return `M ${x1} ${y1} H ${lane} V ${y2} H ${x2}`;
  return (
    `M ${x1} ${y1} H ${lane - leave * r} ` +
    `Q ${lane} ${y1} ${lane} ${y1 + vy * r} V ${y2 - vy * r} ` +
    `Q ${lane} ${y2} ${lane + enter * r} ${y2} H ${x2}`
  );
}

/**
 * Геометрия одной связи по текущему положению коробок.
 * `order` разводит линии, идущие через один промежуток: иначе они слились бы в одну
 * дорожку, и понять, какая откуда идёт, было бы нельзя.
 */
function routeLink(from, to, fromOffset, toOffset, order = 0) {
  const y1 = from.y + fromOffset;
  const y2 = to.y + toOffset;
  const shift = ((order % 3) - 1) * 6;
  const roomy = 2 * STUB;

  if (from.x - (to.x + to.w) >= roomy) {
    const x1 = from.x;
    const x2 = to.x + to.w;
    return { d: orthPath(x1, y1, x2, y2, (x1 + x2) / 2 + shift, -1, -1), x1, y1, x2, y2 };
  }
  if (to.x - (from.x + from.w) >= roomy) {
    const x1 = from.x + from.w;
    const x2 = to.x;
    return { d: orthPath(x1, y1, x2, y2, (x1 + x2) / 2 + shift, 1, 1), x1, y1, x2, y2 };
  }

  // Промежутка нет — обходим снаружи с той стороны, где обход короче для обеих.
  const right = Math.max(from.x + from.w, to.x + to.w);
  const left = Math.min(from.x, to.x);
  const costRight = right - (from.x + from.w) + (right - (to.x + to.w));
  const costLeft = from.x - left + (to.x - left);
  const dir = costRight <= costLeft ? 1 : -1;

  const x1 = dir > 0 ? from.x + from.w : from.x;
  const x2 = dir > 0 ? to.x + to.w : to.x;
  const lane = dir > 0 ? Math.max(x1, x2) + STUB + LANE : Math.min(x1, x2) - STUB - LANE;
  return { d: orthPath(x1, y1, x2, y2, lane, dir, -dir), x1, y1, x2, y2 };
}

function edgeMarkup(link, i, from, to, fromOffset, toOffset, extraClass = "") {
  const geom = routeLink(from, to, fromOffset, toOffset, i);
  return (
    `<g class="er-edge${extraClass}" data-i="${i}" data-src="${esc(link.src)}" data-dst="${esc(link.dst)}" ` +
    `data-sc="${esc(link.srcCol)}" data-dc="${esc(link.dstCol)}" ` +
    `data-fo="${fromOffset}" data-to="${toOffset}">` +
    `<title>${esc(link.src)}.${esc(link.srcCol)} → ${esc(link.dst)}.${esc(link.dstCol)}</title>` +
    `<path class="er-link" d="${geom.d}" />` +
    `<circle class="er-dot" cx="${geom.x1}" cy="${geom.y1}" r="3.5" />` +
    `<circle class="er-dot er-dot-one" cx="${geom.x2}" cy="${geom.y2}" r="3.5" />` +
    "</g>"
  );
}

/**
 * @param {object} schema результат readSchema
 * @param {object} saved сохранённое расположение таблиц
 * @param {{note?: boolean}} options `note: false` — без подписи под диаграммой: на
 *        экране выполнения запроса она только отнимала бы место у самого рисунка
 */
export function renderDiagram(schema, saved, { note = true } = {}) {
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
    edges += edgeMarkup(
      link,
      i,
      from,
      to,
      columnOffset(from.table, link.srcCol),
      columnOffset(to.table, link.dstCol),
    );
  });

  let nodes = "";
  for (const b of boxes.values()) {
    nodes +=
      `<g class="er-table" data-name="${esc(b.table.name)}" data-x="${b.x}" data-y="${b.y}" ` +
      `data-w="${b.w}" data-h="${b.h}" transform="translate(${b.x} ${b.y})">`;
    nodes += `<rect class="er-box" x="0" y="0" width="${b.w}" height="${b.h}" rx="6" />`;
    nodes += `<rect class="er-head" x="0" y="0" width="${b.w}" height="${HEAD}" rx="6" />`;
    nodes += `<text class="er-title" x="${PAD_X}" y="21">${esc(b.table.name)}</text>`;
    b.table.columns.forEach((c) => {
      const offset = columnOffset(b.table, c.name);
      const y = offset + 4.5;
      const mark = b.table.pk.has(c.name) ? "PK" : b.table.fk.has(c.name) ? "FK" : "";
      nodes +=
        `<text class="er-col${mark ? " er-key" : ""}" data-col="${esc(c.name)}" data-off="${offset}" ` +
        `x="${PAD_X}" y="${y}">${esc(c.name)}</text>`;
      nodes += `<text class="er-type" x="${b.w - PAD_X - MARK_W}" y="${y}">${esc(shortType(c.type))}</text>`;
      if (mark) nodes += `<text class="er-mark" x="${b.w - PAD_X}" y="${y}">${mark}</text>`;
    });
    nodes += "</g>";
  }

  const links = schema.links.length;
  const svg =
    `<div class="er-scroll"><svg class="er" data-pad="${PAD}" ` +
    `viewBox="${-PAD} 0 ${canvasW + PAD * 2} ${canvasH}" ` +
    `width="${canvasW + PAD * 2}" height="${canvasH}" role="img" ` +
    `aria-label="Диаграмма схемы: ${schema.tables.length} таблиц, ${links} связей">` +
    edges +
    nodes +
    "</svg></div>";
  if (!note) return svg;
  return (
    svg +
    `<div class="trainer-note">Таблиц: ${schema.tables.length} · связей по внешним ключам: ${links}. ` +
    "Линия идёт от ссылающегося столбца к ключу, на который он ссылается: залитая " +
    "точка — сторона «многие», полая — «один». Таблицы можно перетаскивать, а нажатие " +
    'на таблицу показывает её связи. <button type="button" class="link-button" id="er-reset">Разложить заново</button></div>'
  );
}

/**
 * Включает перетаскивание таблиц и выбор таблицы нажатием.
 *
 * Геометрия читается из самой разметки (data-атрибуты у групп и связей), а не
 * держится отдельным состоянием: панель схемы перерисовывается после каждого
 * запроса, и любое состояние рядом с ней разошлось бы с разметкой.
 *
 * @param {Element} root контейнер с диаграммой
 * @param {(positions: object) => void} onMove вызывается по окончании переноса
 * @param {(name: string) => void} [onSelect] нажатие на таблицу без переноса
 */
export function bindDiagram(root, onMove, onSelect) {
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
      const geom = routeLink(
        rectOf(from),
        rectOf(to),
        +edge.dataset.fo,
        +edge.dataset.to,
        +edge.dataset.i,
      );
      edge.querySelector(".er-link").setAttribute("d", geom.d);
      const dots = edge.querySelectorAll("circle");
      dots[0].setAttribute("cx", geom.x1);
      dots[0].setAttribute("cy", geom.y1);
      dots[1].setAttribute("cx", geom.x2);
      dots[1].setAttribute("cy", geom.y2);
    });
  }

  // Экранные пиксели → координаты viewBox: диаграмма масштабируется под ширину
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
    // Дрожание руки при нажатии — ещё не перенос: иначе выбор таблицы срабатывал бы
    // через раз, а расположение перезаписывалось бы на ровном месте.
    if (!drag.moved && Math.hypot(x - +g.dataset.x, y - +g.dataset.y) < 3) return;
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
    if (!drag.moved && onSelect && event.type === "pointerup") onSelect(drag.g.dataset.name);
    drag = null;
  }

  svg.addEventListener("pointerup", finish);
  svg.addEventListener("pointercancel", finish);
}

// --- Подсветка и масштаб ------------------------------------------------------

function sameLink(link, edge) {
  const forward =
    link.srcTable === edge.src &&
    link.srcCol === edge.sc &&
    link.dstTable === edge.dst &&
    link.dstCol === edge.dc;
  const backward =
    link.srcTable === edge.dst &&
    link.srcCol === edge.dc &&
    link.dstTable === edge.src &&
    link.dstCol === edge.sc;
  return forward || backward;
}

/**
 * Выделяет на диаграмме часть схемы. Остальное приглушается — но остаётся на месте:
 * по неподвижной картинке видно, какая именно её часть работает на этом шаге.
 *
 * Соединение может идти и мимо внешнего ключа: такой линии на диаграмме нет, поэтому
 * она дорисовывается пунктиром на время шага.
 *
 * @param {Element} root контейнер с диаграммой
 * @param {{tables?: string[], active?: string[],
 *          columns?: {table: string, column: string}[],
 *          links?: {srcTable: string, srcCol: string, dstTable: string, dstCol: string}[]}|null} spec
 *        null снимает выделение
 */
export function highlightDiagram(root, spec) {
  const svg = root.querySelector("svg.er");
  if (!svg) return;

  svg.querySelectorAll(".er-virtual").forEach((el) => el.remove());
  svg.classList.toggle("is-tracing", Boolean(spec));

  const active = new Set(spec?.active || []);
  const used = new Set([...(spec?.tables || []), ...active]);
  const columns = new Set((spec?.columns || []).map((c) => `${c.table}.${c.column}`));

  const groups = new Map();
  svg.querySelectorAll("g.er-table").forEach((g) => {
    const name = g.dataset.name;
    groups.set(name, g);
    g.classList.toggle("is-used", used.has(name));
    g.classList.toggle("is-active", active.has(name));
    g.querySelectorAll(".er-col").forEach((text) => {
      text.classList.toggle("is-used", columns.has(`${name}.${text.dataset.col}`));
    });
  });

  const wanted = spec?.links || [];
  const drawn = new Set();
  svg.querySelectorAll("g.er-edge").forEach((edge) => {
    const hit = wanted.findIndex((link) => sameLink(link, edge.dataset));
    edge.classList.toggle("is-active", hit >= 0);
    if (hit >= 0) drawn.add(hit);
  });

  const offsetOf = (g, name) => {
    const text = [...g.querySelectorAll(".er-col")].find((t) => t.dataset.col === name);
    return text ? +text.dataset.off : HEAD;
  };
  const rectOf = (g) => ({ x: +g.dataset.x, y: +g.dataset.y, w: +g.dataset.w, h: +g.dataset.h });

  wanted.forEach((link, i) => {
    if (drawn.has(i)) return;
    const from = groups.get(link.srcTable);
    const to = groups.get(link.dstTable);
    if (!from || !to || from === to) return;
    const markup = edgeMarkup(
      { src: link.srcTable, srcCol: link.srcCol, dst: link.dstTable, dstCol: link.dstCol },
      i,
      rectOf(from),
      rectOf(to),
      offsetOf(from, link.srcCol),
      offsetOf(to, link.dstCol),
      " er-virtual is-active",
    );
    // Перед таблицами: линия не должна ложиться поверх текста.
    svg.querySelector("g.er-table").insertAdjacentHTML("beforebegin", markup);
  });
}

/** Задать масштаб диаграммы. Единица — размер, под который подобран шрифт. */
export function scaleDiagram(root, scale) {
  const svg = root.querySelector("svg.er");
  if (!svg) return;
  svg.style.width = `${Math.round(+svg.getAttribute("width") * scale)}px`;
  svg.style.height = `${Math.round(+svg.getAttribute("height") * scale)}px`;
}

/**
 * Вписать диаграмму в контейнер целиком и вернуть получившийся масштаб.
 * Снизу масштаб ограничен: мельче текст не читается, и полезнее дать прокрутку.
 */
export function fitDiagram(root, { maxHeight = Infinity, minScale = 0.55, maxScale = 1.6 } = {}) {
  const svg = root.querySelector("svg.er");
  const scroller = root.querySelector(".er-scroll");
  if (!svg || !scroller) return 1;
  // Запас в пару пикселей: `clientWidth` округлён, и при дробной ширине контейнера
  // вписанная вплотную диаграмма вылезала бы на доли пикселя, включая полосу прокрутки.
  const available = scroller.clientWidth - 2;
  if (available <= 0) return 1;
  const scale = Math.max(
    minScale,
    Math.min(maxScale, available / +svg.getAttribute("width"), maxHeight / +svg.getAttribute("height")),
  );
  scaleDiagram(root, scale);
  return scale;
}
