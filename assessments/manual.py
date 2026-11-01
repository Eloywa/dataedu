"""Разбор работы, которую студент сдаёт на проверку преподавателю, — без БД и без HTTP.

Файл читается в текст и хранится в той же записи `Submission`, а не на диске. Сдают
здесь SQL-скрипт (его выгружает кнопка «Выгрузить SQL» в тренажёре), и текст в базе
закрывает сразу всё, что потребовал бы отдельный каталог файлов: преподаватель видит
работу прямо в очереди проверки, выгрузка своих данных её включает, а удаление
учётной записи удаляет и её — без файлов-сирот, которые остались бы на сервере вопреки
обещанию о настоящем удалении (см. правовой контур в ARCHITECTURE.md §5.1).
"""

from pathlib import PurePath

MAX_ANSWER_CHARS = 100_000
MAX_UPLOAD_BYTES = 1024 * 1024
UPLOAD_SUFFIXES = (".sql", ".txt")


def read_answer(raw_text, upload=None):
    """Текст работы из формы. Возвращает `(текст, ошибка)` — одно из двух None.

    Если приложен файл, он важнее поля: выбранный файл не появляется сам по себе, а
    вот в поле мог остаться прошлый черновик.
    """
    if upload is not None:
        text, error = _read_upload(upload)
        if error:
            return None, error
    else:
        text = raw_text or ""

    text = text.strip()
    if not text:
        return None, "Ответ пустой: впишите его в поле или приложите файл."
    # PostgreSQL не хранит нулевой байт в тексте, и запись упала бы с ошибкой сервера.
    # Встречается он в файлах, которые текстом только притворяются.
    if "\x00" in text:
        return None, "Файл не похож на текстовый: сохраните работу как .sql или .txt."
    if len(text) > MAX_ANSWER_CHARS:
        return None, f"Ответ длиннее {MAX_ANSWER_CHARS} символов."
    return text, None


def _read_upload(upload):
    if PurePath(upload.name or "").suffix.lower() not in UPLOAD_SUFFIXES:
        return None, "Подойдёт файл .sql или .txt."
    if upload.size > MAX_UPLOAD_BYTES:
        return None, "Файл больше 1 МБ."
    try:
        # utf-8-sig: Блокнот и Excel часто дописывают в начало файла метку порядка байт.
        return upload.read().decode("utf-8-sig"), None
    except UnicodeDecodeError:
        return None, "Файл не читается как текст в UTF-8: пересохраните его в этой кодировке."
