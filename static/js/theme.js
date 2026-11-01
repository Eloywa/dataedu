// Выбор темы: светлая, ламповая, тёмная или как в системе.
//
// Само применение темы происходит раньше — встроенным скриптом в <head>, до
// первой отрисовки. Здесь только то, что можно сделать после загрузки страницы:
// список тем, сохранение выбора и подпись для скринридера.
//
// Пока человек ничего не выбрал, атрибута `data-theme` нет, и тема следует системной
// настройке (`prefers-color-scheme` в CSS). Выбор конкретной темы фиксирует её — и с этого
// момента системная настройка не учитывается, пока не выбран пункт «Как в системе». Поэтому
// при загрузке атрибут здесь не ставится: иначе первый же заход навсегда закреплял бы ту
// тему, что стояла в системе.
//
// Скрипт обёрнут в самовызывающуюся функцию: обычные <script> делят одну
// глобальную область, и одноимённые объявления в разных файлах гасят друг друга
// с ошибкой «Identifier has already been declared» — вместе со всем остальным
// кодом файла. Так каждый файл держит свои имена при себе.

(function () {
  const KEY = "dataedu-theme";
  const SYSTEM = "system";
  const root = document.documentElement;
  const toggle = document.getElementById("theme-toggle");
  const list = document.getElementById("theme-list");
  if (!toggle || !list) return;

  const options = [...list.querySelectorAll("[data-theme-choice]")];

  function currentOption() {
    const theme = root.getAttribute("data-theme") || SYSTEM;
    return options.find((option) => option.dataset.themeChoice === theme) || options[0];
  }

  // Подпись называет текущую тему: иначе скринридер читает «тема оформления», не сообщая,
  // какая она сейчас.
  function describe() {
    const current = currentOption();
    const label = `Тема: ${current.textContent.trim().toLowerCase()}`;
    toggle.title = label;
    const text = toggle.querySelector(".visually-hidden");
    if (text) text.textContent = label;
    for (const option of options) {
      option.setAttribute("aria-checked", option === current ? "true" : "false");
    }
  }

  function choose(theme) {
    if (theme === SYSTEM) root.removeAttribute("data-theme");
    else root.setAttribute("data-theme", theme);
    try {
      if (theme === SYSTEM) localStorage.removeItem(KEY);
      else localStorage.setItem(KEY, theme);
    } catch {
      // Приватный режим или запрет на хранение: тема продержится до перезагрузки.
    }
    describe();
  }

  function isOpen() {
    return !list.hidden;
  }

  function open() {
    list.hidden = false;
    toggle.setAttribute("aria-expanded", "true");
    currentOption().focus();
  }

  function close({ returnFocus = false } = {}) {
    list.hidden = true;
    toggle.setAttribute("aria-expanded", "false");
    if (returnFocus) toggle.focus();
  }

  toggle.addEventListener("click", () => {
    if (isOpen()) close();
    else open();
  });

  toggle.addEventListener("keydown", (event) => {
    if (event.key === "ArrowDown" && !isOpen()) {
      event.preventDefault();
      open();
    }
  });

  list.addEventListener("click", (event) => {
    const option = event.target.closest("[data-theme-choice]");
    if (!option) return;
    choose(option.dataset.themeChoice);
    close({ returnFocus: true });
  });

  // Управление как у обычного меню: без него с клавиатуры до тем было бы не добраться,
  // ведь у пунктов `tabindex="-1"`.
  list.addEventListener("keydown", (event) => {
    const index = options.indexOf(document.activeElement);
    const last = options.length - 1;
    const targets = {
      ArrowDown: index === last ? 0 : index + 1,
      ArrowUp: index <= 0 ? last : index - 1,
      Home: 0,
      End: last,
    };
    if (event.key in targets) {
      event.preventDefault();
      options[targets[event.key]].focus();
    } else if (event.key === "Escape") {
      event.preventDefault();
      close({ returnFocus: true });
    } else if (event.key === "Tab") {
      close();
    }
  });

  document.addEventListener("click", (event) => {
    if (isOpen() && !event.target.closest(".theme-menu")) close();
  });

  describe();
})();
