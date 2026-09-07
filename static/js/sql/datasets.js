// Учебные наборы данных для песочницы.
//
// Наборов три, и это не разнообразие ради разнообразия. На одном наборе студент
// запоминает не приём, а конкретные имена: «соединение — это students и groups».
// Тот же JOIN на магазине и библиотеке заставляет увидеть за именами отношение
// «многие к одному».
//
// «Университет» совпадает с заготовкой практических заданий (seed_practice):
// студент решает задачи на тех же данных, на которых экспериментировал.
//
// У каждого набора есть `bulk` — вставка, раздувающая его до двухсот тысяч строк.
// Без неё разговор об индексах беспредметен: на двенадцати строках планировщик
// индекс не возьмёт, и правильно сделает.

export const DATASETS = {
  university: {
    title: "Университет",
    note: "группы, студенты, оценки",
    sql: `
CREATE TABLE groups (
  id      integer PRIMARY KEY,
  name    text NOT NULL,
  curator text
);
INSERT INTO groups (id, name, curator) VALUES
  (1, 'ПИ-101', 'Иванов И. И.'),
  (2, 'ПИ-102', 'Петрова О. И.'),
  (3, 'МО-201', 'Сидоров С. С.');

CREATE TABLE students (
  id        integer PRIMARY KEY,
  full_name text NOT NULL,
  group_id  integer REFERENCES groups(id),
  xp        integer NOT NULL DEFAULT 0
);
INSERT INTO students (id, full_name, group_id, xp) VALUES
  (1,  'Анна Соколова',     1, 320),
  (2,  'Дмитрий Соколов',   1, 180),
  (3,  'Мария Иванова',     1, 240),
  (4,  'Павел Кузнецов',    2, 90),
  (5,  'Ольга Попова',      2, 410),
  (6,  'Артём Михайлов',    2, 0),
  (7,  'Полина Захарова',   2, 150),
  (8,  'Денис Григорьев',   3, 200),
  (9,  'Виктория Иванова',  3, 365),
  (10, 'Глеб Тимофеев',     3, 130),
  (11, 'Егор Новиков',      1, 275),
  (12, 'Софья Морозова',    3, 55);

CREATE TABLE marks (
  id         serial PRIMARY KEY,
  student_id integer NOT NULL REFERENCES students(id),
  subject    text NOT NULL,
  mark       integer NOT NULL CHECK (mark BETWEEN 2 AND 5),
  taken_on   date NOT NULL
);
INSERT INTO marks (student_id, subject, mark, taken_on) VALUES
  (1, 'Базы данных', 5, '2026-01-15'), (1, 'Математика', 4, '2026-01-20'),
  (2, 'Базы данных', 3, '2026-01-15'), (2, 'Математика', 3, '2026-01-20'),
  (3, 'Базы данных', 4, '2026-01-15'), (3, 'Математика', 5, '2026-01-20'),
  (4, 'Базы данных', 3, '2026-01-16'), (5, 'Базы данных', 5, '2026-01-16'),
  (5, 'Математика', 5, '2026-01-21'), (6, 'Базы данных', 2, '2026-01-16'),
  (7, 'Базы данных', 4, '2026-01-16'), (8, 'Базы данных', 4, '2026-01-17'),
  (9, 'Базы данных', 5, '2026-01-17'), (9, 'Математика', 4, '2026-01-21'),
  (10, 'Базы данных', 3, '2026-01-17'), (11, 'Базы данных', 4, '2026-01-15'),
  (12, 'Базы данных', 3, '2026-01-17');
`,
    bulk: `INSERT INTO students (id, full_name, group_id, xp)
SELECT g, 'Студент №' || g, 1 + (g % 3), (g * 37) % 500
FROM generate_series(100, 200000) AS g;`,
  },

  shop: {
    title: "Магазин",
    note: "покупатели, товары, заказы",
    sql: `
CREATE TABLE customers (
  id   integer PRIMARY KEY,
  name text NOT NULL,
  city text NOT NULL
);
INSERT INTO customers (id, name, city) VALUES
  (1, 'Анна Соколова',  'Москва'),
  (2, 'Пётр Волков',    'Казань'),
  (3, 'Ирина Лебедева', 'Москва'),
  (4, 'Сергей Орлов',   'Новосибирск'),
  (5, 'Мария Зайцева',  'Казань');

CREATE TABLE products (
  id       integer PRIMARY KEY,
  title    text NOT NULL,
  category text NOT NULL,
  price    numeric(10, 2) NOT NULL
);
INSERT INTO products (id, title, category, price) VALUES
  (1, 'Клавиатура',  'Периферия',  3200.00),
  (2, 'Мышь',        'Периферия',  1450.00),
  (3, 'Монитор 24',  'Мониторы',  14900.00),
  (4, 'Монитор 27',  'Мониторы',  23500.00),
  (5, 'Кабель HDMI', 'Кабели',      590.00),
  (6, 'Наушники',    'Аудио',      6700.00);

CREATE TABLE orders (
  id          integer PRIMARY KEY,
  customer_id integer NOT NULL REFERENCES customers(id),
  placed_on   date NOT NULL,
  status      text NOT NULL
);
INSERT INTO orders (id, customer_id, placed_on, status) VALUES
  (1, 1, '2026-02-01', 'доставлен'),
  (2, 2, '2026-02-03', 'доставлен'),
  (3, 1, '2026-02-11', 'в пути'),
  (4, 3, '2026-02-12', 'отменён'),
  (5, 4, '2026-02-15', 'доставлен'),
  (6, 5, '2026-02-18', 'в пути');

CREATE TABLE order_items (
  order_id   integer NOT NULL REFERENCES orders(id),
  product_id integer NOT NULL REFERENCES products(id),
  quantity   integer NOT NULL CHECK (quantity > 0),
  PRIMARY KEY (order_id, product_id)
);
INSERT INTO order_items (order_id, product_id, quantity) VALUES
  (1, 1, 1), (1, 2, 1), (1, 5, 2),
  (2, 3, 1),
  (3, 6, 1), (3, 2, 2),
  (4, 4, 1),
  (5, 3, 2), (5, 5, 1),
  (6, 1, 1), (6, 6, 1);
`,
    bulk: `INSERT INTO orders (id, customer_id, placed_on, status)
SELECT g, 1 + (g % 5), DATE '2026-01-01' + (g % 365),
       CASE g % 3 WHEN 0 THEN 'доставлен' WHEN 1 THEN 'в пути' ELSE 'отменён' END
FROM generate_series(100, 200000) AS g;`,
  },

  library: {
    title: "Библиотека",
    note: "авторы, книги, выдачи",
    sql: `
CREATE TABLE authors (
  id      integer PRIMARY KEY,
  name    text NOT NULL,
  country text
);
INSERT INTO authors (id, name, country) VALUES
  (1, 'Кнут Д. Э.',       'США'),
  (2, 'Дейт К. Дж.',      'Великобритания'),
  (3, 'Гарсиа-Молина Г.', 'США'),
  (4, 'Кормен Т.',        'США');

CREATE TABLE books (
  id        integer PRIMARY KEY,
  title     text NOT NULL,
  author_id integer REFERENCES authors(id),
  year      integer,
  copies    integer NOT NULL DEFAULT 1
);
INSERT INTO books (id, title, author_id, year, copies) VALUES
  (1, 'Искусство программирования',      1, 1968, 2),
  (2, 'Введение в системы баз данных',   2, 1975, 5),
  (3, 'Системы баз данных. Полный курс', 3, 2002, 3),
  (4, 'Алгоритмы: построение и анализ',  4, 1990, 4),
  (5, 'Конкретная математика',           1, 1989, 1);

CREATE TABLE readers (
  id        integer PRIMARY KEY,
  full_name text NOT NULL,
  card_no   text NOT NULL UNIQUE,
  faculty   text
);
INSERT INTO readers (id, full_name, card_no, faculty) VALUES
  (1, 'Анна Соколова',  'Ч-0001', 'Информатика'),
  (2, 'Пётр Волков',    'Ч-0002', 'Информатика'),
  (3, 'Ирина Лебедева', 'Ч-0003', 'Математика'),
  (4, 'Сергей Орлов',   'Ч-0004', 'Физика');

CREATE TABLE loans (
  id          serial PRIMARY KEY,
  book_id     integer NOT NULL REFERENCES books(id),
  reader_id   integer NOT NULL REFERENCES readers(id),
  taken_on    date NOT NULL,
  returned_on date
);
INSERT INTO loans (book_id, reader_id, taken_on, returned_on) VALUES
  (2, 1, '2026-01-10', '2026-01-28'),
  (3, 1, '2026-02-01', NULL),
  (2, 2, '2026-01-12', '2026-02-02'),
  (4, 3, '2026-01-20', NULL),
  (1, 4, '2026-02-05', NULL),
  (2, 3, '2026-02-07', '2026-02-19'),
  (5, 2, '2026-02-10', NULL);
`,
    bulk: `INSERT INTO loans (book_id, reader_id, taken_on, returned_on)
SELECT 1 + (g % 5), 1 + (g % 4), DATE '2025-01-01' + (g % 500),
       CASE WHEN g % 3 = 0 THEN NULL ELSE DATE '2025-01-20' + (g % 500) END
FROM generate_series(1, 200000) AS g;`,
  },
};

export const DEFAULT_DATASET = "university";

/** Полный сброс схемы: короче и надёжнее, чем DROP TABLE в правильном порядке. */
export const WIPE = "DROP SCHEMA public CASCADE; CREATE SCHEMA public;";
