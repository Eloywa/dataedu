# Обложки курсов

Снимки лежат в репозитории и отдаются с того же сервера, что и остальная
статика. Ссылаться на чужой хостинг нельзя: платформа не делает ни одного
внешнего запроса (см. раздел «Автономность» в корневом README и тест
`core.tests.test_accessibility.AutonomyTests`).

Источник — [Unsplash](https://unsplash.com). [Лицензия
Unsplash](https://unsplash.com/license) разрешает скачивать, изменять и
использовать снимки бесплатно, в том числе в коммерческих целях, и не требует
разрешения автора. Указание авторства не обязательно, но ведётся здесь: работа
дипломная, и происхождение каждого чужого материала должно быть прослеживаемо.

Запрещено лицензией и здесь не делается: продажа самих снимков без изменений и
создание сервиса, повторяющего Unsplash.

## Что откуда

| Файл | Курс | Автор | Оригинал |
|---|---|---|---|
| `sql-s-nulya.jpg` | SQL с нуля | Afonso Azevedo Neves | [rNxfMnfnenE](https://unsplash.com/photos/rNxfMnfnenE) |
| `databases-for-teachers.jpg` | Базы данных для будущих педагогов | Dom Fou | [YRMWVcdyhmI](https://unsplash.com/photos/YRMWVcdyhmI) |
| `postgresql-praktika.jpg` | PostgreSQL на практике | Nam Anh | [QJbyG6O0ick](https://unsplash.com/photos/QJbyG6O0ick) |
| `proektirovanie-er.jpg` | Проектирование ER | Sven Mieke | [fteR0e2BzKo](https://unsplash.com/photos/fteR0e2BzKo) |
| `normalizaciya.jpg` | Нормализация | Jan Antonin Kolar | [lRoX0shwjUQ](https://unsplash.com/photos/lRoX0shwjUQ) |
| `indeksy-proizvoditelnost.jpg` | Индексы и производительность | Lance Chang | [h3pVxOIpnzk](https://unsplash.com/photos/h3pVxOIpnzk) |
| `okonnye-funkcii.jpg` | Оконные функции | Khara Woods | [3lKFHLCKark](https://unsplash.com/photos/3lKFHLCKark) |
| `tranzakcii-blokirovki.jpg` | Транзакции и блокировки | Brock Wegner | [3ROwc3JSjCk](https://unsplash.com/photos/3ROwc3JSjCk) |

## Как подобраны

Предметные метафоры, а не отвлечённые «кибер»-картинки: картотека для
нормализации, складские стеллажи для индексов, ряды окон на фасаде для оконных
функций, дверь хранилища для транзакций, слон для PostgreSQL. Светящиеся серверы
и синие сетки к теме курса не ближе прежнего градиента, а выглядят как заставка
из чужой презентации.

## Как обработаны

Кадрирование по центру до 16:9, ширина 900 пикселей (вдвое больше плашки на
карточке — под экраны с удвоенной плотностью), JPEG с качеством 80,
прогрессивный. Все восемь весят около 550 КБ.

Новый снимок ставится так же: положить файл `<slug>.jpg` в эту папку, добавить
slug в `PHOTOS` в `courses/cover.py` и строку в таблицу выше. Курс без снимка
получает рисованную обложку — градиент с иконкой, и это не считается недочётом.
