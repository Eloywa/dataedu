"""Теория урока: разметка в HTML и оглавление по её заголовкам.

Оглавление («Содержание урока» из §3.3 брифа) не хранится отдельным полем и не
размечается руками. Оно собирается из тех же заголовков, что уже стоят в тексте
урока: иначе список и текст разойдутся при первой же правке теории, а заметить
это можно будет только открыв урок.

Якоря делает расширение `toc` самого markdown — оно же проставляет `id` на
заголовки, так что ссылка и цель всегда появляются парой.
"""

import markdown as md
from django.utils.safestring import mark_safe
from markdown.extensions.toc import slugify_unicode

# Заголовки уроков русские, а стандартный slugify выбрасывает всё, кроме латиницы,
# и превращает «Чем база отличается от документа Word» в `_1`. Такие якоря ничего
# не говорят ни в адресной строке, ни в разметке; `slugify_unicode` сохраняет
# кириллицу.
EXTENSIONS = ["extra", "sane_lists", "toc"]
CONFIG = {"toc": {"toc_depth": "2-3", "permalink": False, "slugify": slugify_unicode}}


def render_theory(text):
    """HTML теории и плоское оглавление: [{"id", "name", "level"}].

    Уровни оставлены плоским списком с полем `level`, а не вложенными списками:
    в боковой колонке подзаголовок отличается только отступом, и разбирать в
    шаблоне дерево ради этого незачем.
    """
    converter = md.Markdown(extensions=EXTENSIONS, extension_configs=CONFIG)
    html = converter.convert(text or "")

    toc = []
    for token in converter.toc_tokens:
        toc.append({"id": token["id"], "name": token["name"], "level": token["level"]})
        for child in token.get("children", []):
            toc.append({"id": child["id"], "name": child["name"], "level": child["level"]})

    # Оглавление из одного пункта — это не оглавление: единственный заголовок и так
    # виден на экране, а колонка рядом с текстом занимала бы место впустую.
    if len(toc) < 2:
        toc = []

    # Содержимое авторское: уроки пишет преподаватель в админке, произвольного
    # пользовательского ввода здесь нет (то же основание, что у `md_to_html`).
    return mark_safe(html), toc
