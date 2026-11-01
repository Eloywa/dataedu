// Поле ввода SQL: номера строк, подсветка и строка быстрых символов.
//
// Редактор остаётся обычной <textarea>. Готовый компонент вроде CodeMirror сюда
// не поставить: платформа не делает внешних запросов, а вшивать в репозиторий
// ещё полтора мегабайта ради подсветки — дорого (см. static/vendor/README.md).
// Поэтому подсветка рисуется подложкой: под прозрачным текстом поля лежит <pre>
// с теми же символами, разобранными на части. Совпадение держится на том, что у
// слоёв одинаковые шрифт, кегль, интерлиньяж и отступы, — правила лежат рядом в
// app.css и помечены комментарием.
//
// Перенос строк выключен (`wrap="off"`, `white-space: pre`): при переносе слой
// подсветки и поле считают строки по-разному, и подложка уезжает. Длинный запрос
// прокручивается внутри своего блока — страница вбок не едет (бриф §4).

// Слова PostgreSQL, которые подсвечиваем. Список намеренно короткий: это
// учебный тренажёр, и всё, что встречается в курсе, здесь есть. Незнакомое
// слово просто останется обычным текстом — хуже от этого не будет.
const KEYWORDS = [
  "select", "from", "where", "group", "by", "having", "order", "limit", "offset",
  "join", "inner", "left", "right", "full", "outer", "cross", "on", "using",
  "insert", "into", "values", "update", "set", "delete", "truncate",
  "create", "table", "view", "index", "schema", "database", "drop", "alter",
  "add", "column", "constraint", "primary", "foreign", "key", "references",
  "unique", "check", "default", "not", "null", "and", "or", "in", "between",
  "like", "ilike", "is", "as", "distinct", "case", "when", "then", "else", "end",
  "union", "all", "except", "intersect", "with", "recursive", "returning",
  "begin", "commit", "rollback", "savepoint", "explain", "analyze", "vacuum",
  "asc", "desc", "count", "sum", "avg", "min", "max", "coalesce", "cast",
  "over", "partition", "row_number", "rank", "dense_rank", "lag", "lead",
  "integer", "int", "bigint", "text", "varchar", "boolean", "date", "timestamp",
  "numeric", "serial", "true", "false",
];
const KEYWORD_SET = new Set(KEYWORDS);

// Символы, которых нет на экранной клавиатуре телефона или до которых нужно
// два-три нажатия (бриф §5). Порядок — по частоте в учебных запросах.
const SYMBOLS = [
  "'", '"', "=", ";", ">", "<", "*", "(", ")", ",", ".", "%",
  "AND", "OR", "NOT", "NULL",
];

function esc(text) {
  return text.replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" })[c]);
}

/** Разбор запроса на части. Одним проходом регулярного выражения: строки и
 *  комментарии должны выигрывать у всего остального, иначе `-- from` подсветится
 *  как ключевое слово посреди комментария. */
function highlight(sql) {
  const pattern = /(--[^\n]*|\/\*[\s\S]*?\*\/)|('(?:[^']|'')*')|(\b\d+(?:\.\d+)?\b)|([A-Za-z_][A-Za-z_0-9]*)/g;
  let out = "";
  let last = 0;
  let match;

  while ((match = pattern.exec(sql)) !== null) {
    out += esc(sql.slice(last, match.index));
    const [text, comment, string, number, word] = match;
    if (comment) {
      out += '<span class="tok-comment">' + esc(text) + "</span>";
    } else if (string) {
      out += '<span class="tok-string">' + esc(text) + "</span>";
    } else if (number) {
      out += '<span class="tok-number">' + esc(text) + "</span>";
    } else if (word && KEYWORD_SET.has(word.toLowerCase())) {
      out += '<span class="tok-key">' + esc(text) + "</span>";
    } else {
      out += esc(text);
    }
    last = match.index + text.length;
  }
  out += esc(sql.slice(last));
  // Пустая последняя строка иначе схлопывается, и подложка уезжает вверх на
  // строку относительно поля.
  return out + "\n";
}

/** Номера строк. Отдельным столбцом, а не фоном поля: фон рисует одинаковые
 *  полоски, а номер нужен настоящий — по нему студент находит строку в тексте
 *  ошибки PostgreSQL. */
function gutterHtml(sql) {
  const lines = sql.split("\n").length;
  let out = "";
  for (let i = 1; i <= lines; i += 1) out += i + "\n";
  return out;
}

function insertAtCaret(field, text) {
  const start = field.selectionStart;
  const end = field.selectionEnd;
  field.value = field.value.slice(0, start) + text + field.value.slice(end);
  const caret = start + text.length;
  field.setSelectionRange(caret, caret);
  field.dispatchEvent(new Event("input", { bubbles: true }));
}

/**
 * Обвязать <textarea> номерами строк, подсветкой и строкой символов.
 * Возвращает { refresh } — обновить подложку, когда значение меняют из кода.
 */
export function setupEditor(field, { symbolsHost } = {}) {
  if (!field) return { refresh() {} };

  field.setAttribute("wrap", "off");

  const shell = document.createElement("div");
  shell.className = "editor";
  field.parentNode.insertBefore(shell, field);

  const gutter = document.createElement("pre");
  gutter.className = "editor-gutter";
  gutter.setAttribute("aria-hidden", "true");

  const layer = document.createElement("pre");
  layer.className = "editor-layer";
  layer.setAttribute("aria-hidden", "true");
  const code = document.createElement("code");
  layer.append(code);

  shell.append(gutter, layer, field);

  function refresh() {
    const value = field.value;
    code.innerHTML = highlight(value);
    gutter.textContent = gutterHtml(value);
    sync();
  }

  function sync() {
    layer.scrollTop = field.scrollTop;
    layer.scrollLeft = field.scrollLeft;
    gutter.scrollTop = field.scrollTop;
  }

  field.addEventListener("input", refresh);
  field.addEventListener("scroll", sync);

  // Tab внутри запроса — отступ, а не уход на следующую кнопку. Выход по Esc:
  // иначе с клавиатуры из поля не выбраться (бриф §7 — полное управление с
  // клавиатуры).
  field.addEventListener("keydown", (event) => {
    if (event.key === "Tab" && !event.shiftKey && !field.dataset.escaped) {
      event.preventDefault();
      insertAtCaret(field, "  ");
    }
    if (event.key === "Escape") {
      field.dataset.escaped = "1";
    }
  });
  field.addEventListener("blur", () => delete field.dataset.escaped);

  if (symbolsHost) {
    for (const symbol of SYMBOLS) {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "symbol-key";
      button.textContent = symbol;
      // Вставка не должна уводить фокус: на телефоне иначе закрывается
      // клавиатура, и после каждого символа её приходится открывать заново.
      button.addEventListener("mousedown", (event) => event.preventDefault());
      button.addEventListener("click", () => {
        const text = symbol.length > 1 ? " " + symbol + " " : symbol;
        insertAtCaret(field, text);
        field.focus();
      });
      symbolsHost.append(button);
    }
  }

  refresh();
  return { refresh };
}
