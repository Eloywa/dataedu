// Переключатель светлой и тёмной темы.
//
// Само применение темы происходит раньше — встроенным скриптом в <head>, до
// первой отрисовки. Здесь только то, что можно сделать после загрузки страницы:
// обработчик нажатия, сохранение выбора и подпись для скринридера.
//
// Три состояния, а не два: пока человек не нажимал кнопку, атрибута `data-theme`
// нет, и тема следует системной настройке (`prefers-color-scheme` в CSS). Нажатие
// фиксирует выбор — и с этого момента системная настройка больше не учитывается.
//
// Скрипт обёрнут в самовызывающуюся функцию: обычные <script> делят одну
// глобальную область, и одноимённые объявления в разных файлах гасят друг друга
// с ошибкой «Identifier has already been declared» — вместе со всем остальным
// кодом файла. Так каждый файл держит свои имена при себе.

(function () {
  const KEY = "dataedu-theme";
  const root = document.documentElement;
  const toggle = document.getElementById("theme-toggle");

  function systemPrefersDark() {
    return window.matchMedia("(prefers-color-scheme: dark)").matches;
  }

  function currentTheme() {
    return root.getAttribute("data-theme") || (systemPrefersDark() ? "dark" : "light");
  }

  function describe(theme) {
    return theme === "dark" ? "Включить светлую тему" : "Включить тёмную тему";
  }

  function apply(theme) {
    root.setAttribute("data-theme", theme);
    try {
      localStorage.setItem(KEY, theme);
    } catch {
      // Приватный режим или запрет на хранение: тема продержится до перезагрузки.
    }
    if (toggle) {
      const label = describe(theme);
      toggle.title = label;
      // Подпись меняется вместе с темой, иначе скринридер читает «сменить тему»
      // без указания, на какую именно.
      const text = toggle.querySelector(".visually-hidden");
      if (text) text.textContent = label;
    }
  }

  if (toggle) {
    apply(currentTheme());
    toggle.addEventListener("click", () => {
      apply(currentTheme() === "dark" ? "light" : "dark");
    });
  }
})();
