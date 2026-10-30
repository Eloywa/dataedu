// Выдвижная программа курса на странице урока.
//
// На широком экране дерево модулей стоит слева постоянно и никакого скрипта не
// требует. На экранах уже 1024 px оно превращается в панель, которая выезжает по
// кнопке (бриф §4): постоянная колонка на телефоне съела бы весь экран, ради
// которого урок и открывают.
//
// Скрипт включает сворачивание, а не показ — тот же порядок, что в nav.js: до
// его загрузки дерево видно и работает как обычный список ссылок. Класс js-lesson
// на <html> ставится первым делом, к нему привязаны правила скрытия в app.css.
// Не загрузился файл или выключен JS — класса нет, правила не срабатывают,
// программа курса просто лежит над текстом урока.
//
// Порог (1023px) продублирован здесь и в CSS сознательно: matchMedia не читает
// медиазапросы из таблицы стилей, а заводить переменную ради одного числа —
// лишний слой. Значение помечено в обоих файлах.
//
// Файл обёрнут в самовызывающуюся функцию: обычные <script> делят одну глобальную
// область, и одноимённые объявления в разных файлах гасят друг друга.

(function () {
  const NARROW = "(max-width: 1023px)";

  const toggle = document.getElementById("course-tree-toggle");
  const tree = document.getElementById("course-tree");
  const backdrop = document.getElementById("course-tree-backdrop");
  const close = document.getElementById("course-tree-close");

  if (!toggle || !tree) {
    return;
  }

  document.documentElement.classList.add("js-lesson");
  toggle.hidden = false;
  if (close) {
    close.hidden = false;
  }

  const narrow = window.matchMedia(NARROW);

  function setOpen(open) {
    tree.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    if (backdrop) {
      backdrop.hidden = !open;
    }
    // Фон не прокручивается, пока панель открыта: иначе касание мимо панели
    // уводит страницу, а не закрывает её.
    document.body.classList.toggle("is-drawer-open", open);
  }

  function isOpen() {
    return tree.classList.contains("is-open");
  }

  toggle.addEventListener("click", () => {
    const open = !isOpen();
    setOpen(open);
    if (open) {
      // Фокус уходит в панель: человеку с клавиатуры иначе пришлось бы
      // протабулировать всю страницу, чтобы добраться до списка уроков.
      const first = tree.querySelector("a, button");
      if (first) {
        first.focus();
      }
    }
  });

  if (close) {
    close.addEventListener("click", () => {
      setOpen(false);
      toggle.focus();
    });
  }

  if (backdrop) {
    backdrop.addEventListener("click", () => {
      setOpen(false);
      toggle.focus();
    });
  }

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && isOpen()) {
      setOpen(false);
      toggle.focus();
    }
  });

  // Переход по ссылке внутри панели — это уход на другой урок, и панель должна
  // закрыться сама: иначе на новой странице она на миг мелькает открытой.
  tree.addEventListener("click", (event) => {
    if (event.target.closest("a") && narrow.matches) {
      setOpen(false);
    }
  });

  // Экран расширили до десктопного — панель больше не панель, а колонка:
  // состояние «открыта» нужно снять, иначе останутся подложка и блокировка
  // прокрутки.
  narrow.addEventListener("change", (event) => {
    if (!event.matches) {
      setOpen(false);
    }
  });
})();
