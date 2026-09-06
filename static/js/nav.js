// Мобильное меню шапки.
//
// Скрипт включает сворачивание, а не показ: до его загрузки навигация видна и
// работает (см. комментарий в base.html). Поэтому первым делом ставится класс
// js-nav на <html> — к нему привязано правило скрытия в app.css. Если файл
// не загрузился или JS отключён, класса нет, правило не срабатывает, меню просто
// переносится на вторую строку.
//
// Ширина порога (860px) продублирована здесь и в CSS сознательно: matchMedia не
// умеет читать медиазапросы из таблицы стилей, а вводить CSS-переменную ради
// одного числа — лишний слой. Значения помечены в обоих файлах.
//
// Скрипт обёрнут в самовызывающуюся функцию: обычные <script> делят одну
// глобальную область, и одноимённые объявления в разных файлах гасят друг друга
// с ошибкой «Identifier has already been declared» — вместе со всем остальным
// кодом файла. Так каждый файл держит свои имена при себе.

(function () {
  const BREAKPOINT = "(max-width: 860px)";

  const toggle = document.getElementById("nav-toggle");
  const nav = document.getElementById("site-nav");

  if (toggle && nav) {
    document.documentElement.classList.add("js-nav");
    toggle.hidden = false;

    const mobile = window.matchMedia(BREAKPOINT);

    function setOpen(open) {
      nav.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    }

    toggle.addEventListener("click", () => {
      setOpen(!nav.classList.contains("is-open"));
    });

    // Esc закрывает и возвращает фокус на кнопку: иначе фокус остаётся внутри
    // скрытого меню, и следующий Tab уводит «в никуда».
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && nav.classList.contains("is-open")) {
        setOpen(false);
        toggle.focus();
      }
    });

    // Клик мимо меню закрывает его. Проверка на mobile.matches нужна, чтобы на
    // десктопе, где меню и так раскрыто, клики по странице не трогали состояние.
    document.addEventListener("click", (e) => {
      if (!mobile.matches || !nav.classList.contains("is-open")) return;
      if (nav.contains(e.target) || toggle.contains(e.target)) return;
      setOpen(false);
    });

    // При переходе на широкий экран состояние сбрасывается: раскладка десктопа
    // показывает меню сама, а оставшийся aria-expanded="true" на скрытой кнопке
    // означал бы для скринридера раскрытый список, которого нет.
    mobile.addEventListener("change", (e) => {
      if (!e.matches) setOpen(false);
    });
  }
})();
