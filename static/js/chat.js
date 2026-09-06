// Живой тред переписки и бейдж непрочитанных.
//
// Доставка сделана опросом, а не SSE: синхронный Django держал бы на каждое открытое
// соединение отдельный поток и отдельное подключение к базе (подробнее — в докстринге
// messaging/views.py). Опрос раз в несколько секунд для учебной переписки ощущается
// так же, а стоит одного обычного GET.
//
// Скрипт — надстройка. Без него страница работает: форма отправляется обычным POST
// с редиректом обратно, тред приходит отрисованным с сервера.

const THREAD_INTERVAL = 5000;
const BADGE_INTERVAL = 30000;

// Пауза, когда вкладка скрыта: опрашивать фоновую вкладку незачем — при возврате
// данные всё равно обновятся сразу.
function hidden() {
  return document.visibilityState === "hidden";
}

function timeLabel(iso) {
  const d = new Date(iso);
  const pad = (n) => String(n).padStart(2, "0");
  return `${pad(d.getDate())}.${pad(d.getMonth() + 1)} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

function renderMessage(m) {
  const li = document.createElement("li");
  li.className = "chat-msg" + (m.mine ? " is-mine" : "");
  li.dataset.id = m.id;

  // textContent, а не innerHTML: тело сообщения пишет пользователь, и разметка
  // из него в документ попадать не должна.
  const bubble = document.createElement("div");
  bubble.className = "chat-bubble";
  bubble.textContent = m.body;

  const time = document.createElement("time");
  time.className = "chat-time mono";
  time.dateTime = m.at;
  time.textContent = timeLabel(m.at);

  li.append(bubble, time);
  return li;
}

function startThread(root) {
  const log = root.querySelector("#chat-log");
  const url = root.dataset.threadUrl;
  const peer = root.dataset.peer;
  const course = root.dataset.course;
  if (!log || !url || !peer || !course) return;

  const atBottom = () => log.scrollHeight - log.scrollTop - log.clientHeight < 40;
  const toBottom = () => {
    log.scrollTop = log.scrollHeight;
  };
  toBottom();

  async function poll() {
    if (hidden()) return;
    let data;
    try {
      const res = await fetch(`${url}?peer=${encodeURIComponent(peer)}&course=${encodeURIComponent(course)}`, {
        headers: { Accept: "application/json" },
      });
      if (!res.ok) return;
      data = await res.json();
    } catch {
      // Сеть моргнула — просто ждём следующего круга, ошибку показывать незачем.
      return;
    }
    if (!data.ok) return;

    const known = new Set([...log.querySelectorAll(".chat-msg")].map((el) => el.dataset.id));
    const fresh = data.messages.filter((m) => !known.has(m.id));
    if (!fresh.length) return;

    // Прокрутку двигаем только если человек и так был внизу: иначе он читает
    // старое сообщение, и рывок вниз собьёт чтение.
    const wasAtBottom = atBottom();
    const empty = log.querySelector("#chat-empty");
    if (empty) empty.remove();
    fresh.forEach((m) => log.append(renderMessage(m)));
    if (wasAtBottom) toBottom();
  }

  setInterval(poll, THREAD_INTERVAL);
  document.addEventListener("visibilitychange", () => {
    if (!hidden()) poll();
  });
}

function startBadge(badge) {
  const url = badge.dataset.unreadUrl;
  if (!url) return;

  async function poll() {
    if (hidden()) return;
    try {
      const res = await fetch(url, { headers: { Accept: "application/json" } });
      if (!res.ok) return;
      const { unread } = await res.json();
      badge.textContent = unread > 99 ? "99+" : String(unread);
      badge.hidden = !unread;
    } catch {
      // молча
    }
  }

  setInterval(poll, BADGE_INTERVAL);
}

const thread = document.getElementById("chat");
if (thread) startThread(thread);

const badge = document.getElementById("unread-badge");
if (badge) startBadge(badge);
