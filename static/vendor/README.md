# static/vendor — сторонние файлы, размещённые локально

Здесь лежат внешние библиотеки и шрифты, **вшитые в репозиторий**. Правило простое:
готовая страница DataEdu не должна делать ни одного запроса за пределы своего домена.

Причины две, и обе важны:

1. **Работа без интернета.** Тренажёр и автопроверка построены на PGlite
   (PostgreSQL в WebAssembly). Пока библиотека грузилась с `cdn.jsdelivr.net`,
   отсутствие сети или блокировка CDN означали неработающий тренажёр — в том числе
   на защите.
2. **152-ФЗ.** Каждый запрос к зарубежному CDN передаёт туда IP-адрес и User-Agent
   пользователя. По позиции Роскомнадзора IP-адрес относится к персональным данным,
   то есть такой запрос — трансграничная передача (ст. 12 152-ФЗ) без правовых
   оснований. Локальное размещение снимает вопрос целиком.

Отсюда следует запрет: **не добавлять в шаблоны ссылки на внешние CDN, шрифтовые
сервисы, аналитику и карты.** Любая новая зависимость сначала попадает в этот каталог.

---

## pglite/ — PGlite 0.5.4 (Apache-2.0)

PostgreSQL в браузере. Из 25 МБ npm-пакета взят минимальный набор для ESM в браузере
(~17 МБ): движок, образ файловой системы и точка входа с чанками.

| Файл | Назначение |
|---|---|
| `pglite.wasm` (9.7 МБ) | скомпилированный PostgreSQL |
| `pglite.data` (6.1 МБ) | образ файловой системы Postgres |
| `index.js` (453 КБ) | точка входа ESM |
| `chunk-*.js` (7 файлов) | чанки сборки, импортируются `index.js` |
| `LICENSE` | Apache-2.0 |

Отброшены: `*.map` (source maps), `*.cjs` (сборка под Node), `contrib/*.tar.gz`
(расширения Postgres — платформа их не использует), `initdb.wasm`.

Раскладку менять нельзя: `index.js` обращается к `pglite.wasm` и `pglite.data`
по относительному пути.

### Обновление версии

```bash
npm pack @electric-sql/pglite            # скачает electric-sql-pglite-<версия>.tgz
tar xzf electric-sql-pglite-*.tgz
cp package/dist/index.js package/dist/pglite.wasm package/dist/pglite.data \
   package/dist/chunk-*.js package/LICENSE static/vendor/pglite/
```

После обновления проверить, что `index.js` не начал импортировать новые файлы:

```bash
grep -o 'from"\./[^"]*"' static/vendor/pglite/index.js | sort -u
```

Затем открыть `/trainer/` и `/practice/<id>/` и убедиться, что запрос выполняется.

---

## fonts/ — Geist, Space Grotesk, Manrope, IBM Plex Mono (SIL OFL 1.1)

22 файла `woff2` (~364 КБ) и `fonts.css` с правилами `@font-face`, снятыми с
Google Fonts вместе с `unicode-range` — поэтому браузер по-прежнему качает только
нужный субсет, а не весь набор.

Субсеты: `latin`, `latin-ext`, `cyrillic`, `cyrillic-ext`. `vietnamese` и `greek`
отброшены как ненужные.

Часть семейств (Geist, Space Grotesk, Manrope) — variable-шрифты: один файл
обслуживает все веса, поэтому имена файлов не содержат вес, и на один `woff2`
ссылается несколько правил `@font-face`. Это нормально.

**Зачем Manrope.** У Space Grotesk нет кириллицы, а весь интерфейс русскоязычный —
без компаньона русские заголовки уезжали в системный `sans-serif`. Стек
`"Space Grotesk", "Manrope", sans-serif` даёт поглифовый фолбэк: латиница
набирается Space Grotesk, кириллица — Manrope.

### Обновление

Забрать CSS с Google Fonts под браузерным User-Agent (иначе вернётся `ttf` вместо
`woff2`), скачать все `woff2` из ответа и переписать `url(...)` на локальные имена.
Ключевой момент: **имена файлов задавать по URL, а не по весу** — иначе для
variable-шрифтов правила разных весов будут ссылаться на несуществующие файлы.
Обязательная самопроверка после генерации:

```bash
python - <<'PY'
import re, pathlib
css = pathlib.Path("static/vendor/fonts/fonts.css").read_text(encoding="utf-8")
refs = set(re.findall(r"url\(([^)]+\.woff2)\)", css))
have = {p.name for p in pathlib.Path("static/vendor/fonts").glob("*.woff2")}
print("отсутствуют:", sorted(refs - have) or "нет")
print("лишние:", sorted(have - refs) or "нет")
PY
```

---

## Проверка, что внешних запросов не осталось

```bash
grep -rn "https\?://" templates/ static/css/ static/js/
```

Вывод должен быть пустым. Ссылки внутри `static/vendor/**` (комментарии, лицензии)
допустимы — это текст, а не запросы.
