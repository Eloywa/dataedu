// Выгрузка базы в SQL.
//
// Своя схема живёт в IndexedDB браузера — забрать её оттуда нельзя ни сдать
// преподавателю, ни перенести на другую машину. Здесь она собирается в обычный
// скрипт: `CREATE TABLE`, ограничения, индексы, данные. Файл выполняется в
// настоящем PostgreSQL, а не только в песочнице, — иначе курсовая работа
// оставалась бы внутри вкладки.
//
// Определения ограничений и индексов не восстанавливаются по частям, а берутся
// у самой базы (`pg_get_constraintdef`, `pg_indexes.indexdef`). Собирать текст
// ограничения из системных таблиц вручную — верный способ однажды потерять
// условие CHECK или порядок столбцов в составном ключе.

const CHUNK = 200; // строк в одном INSERT: длинные операторы тяжело читать
const ROW_LIMIT = 20000; // выше — файл перестаёт быть обозримым, а смысл теряется

function ident(name) {
  return '"' + String(name).replace(/"/g, '""') + '"';
}

function literal(value) {
  if (value === null || value === undefined) return "NULL";
  if (typeof value === "number") return Number.isFinite(value) ? String(value) : "NULL";
  if (typeof value === "boolean") return value ? "TRUE" : "FALSE";
  if (value instanceof Date) return `'${value.toISOString()}'`;
  // Значения numeric приходят из драйвера строкой, и в кавычках они и
  // остаются: PostgreSQL приведёт их к типу столбца сам, а превращать их в
  // число на стороне JavaScript значило бы терять точность на ровном месте.
  const text = typeof value === "object" ? JSON.stringify(value) : String(value);
  return "'" + text.replace(/'/g, "''") + "'";
}

/** Столбец с `nextval` в умолчании — это serial. Выводим его как serial, иначе
 *  скрипт ссылался бы на последовательность, которой в новой базе ещё нет. */
function serialType(type, def) {
  if (!def || !/^nextval\(/i.test(def)) return null;
  if (/^bigint$/i.test(type)) return "bigserial";
  if (/^smallint$/i.test(type)) return "smallserial";
  return "serial";
}

async function readColumns(db) {
  const res = await db.query(`
    SELECT cl.relname                            AS table_name,
           a.attname                             AS column_name,
           format_type(a.atttypid, a.atttypmod)  AS type,
           a.attnotnull                          AS not_null,
           pg_get_expr(d.adbin, d.adrelid)       AS default_expr
    FROM pg_attribute a
    JOIN pg_class cl ON cl.oid = a.attrelid
    JOIN pg_namespace n ON n.oid = cl.relnamespace
    LEFT JOIN pg_attrdef d ON d.adrelid = a.attrelid AND d.adnum = a.attnum
    WHERE n.nspname = 'public' AND cl.relkind = 'r' AND a.attnum > 0 AND NOT a.attisdropped
    ORDER BY cl.relname, a.attnum
  `);
  const tables = new Map();
  for (const r of res.rows) {
    if (!tables.has(r.table_name)) tables.set(r.table_name, []);
    tables.get(r.table_name).push(r);
  }
  return tables;
}

async function readConstraints(db) {
  const res = await db.query(`
    SELECT cl.relname AS table_name,
           c.conname   AS name,
           c.contype   AS kind,
           pg_get_constraintdef(c.oid) AS def
    FROM pg_constraint c
    JOIN pg_class cl ON cl.oid = c.conrelid
    JOIN pg_namespace n ON n.oid = cl.relnamespace
    WHERE n.nspname = 'public'
    ORDER BY cl.relname, c.contype DESC, c.conname
  `);
  return res.rows;
}

async function readIndexes(db) {
  const res = await db.query(`
    SELECT tablename AS table_name, indexname AS name, indexdef AS def
    FROM pg_indexes
    WHERE schemaname = 'public'
    ORDER BY tablename, indexname
  `);
  return res.rows;
}

function createTable(name, columns, inline) {
  const lines = columns.map((c) => {
    const serial = serialType(c.type, c.default_expr);
    let line = `  ${ident(c.column_name)} ${serial || c.type}`;
    if (!serial && c.default_expr) line += ` DEFAULT ${c.default_expr}`;
    if (c.not_null && !serial) line += " NOT NULL";
    return line;
  });
  // Первичный ключ и CHECK пишутся внутри CREATE TABLE — они относятся к самой
  // таблице. Внешние ключи выносятся отдельно, чтобы не зависеть от порядка.
  for (const c of inline) lines.push(`  CONSTRAINT ${ident(c.name)} ${c.def}`);
  return `CREATE TABLE ${ident(name)} (\n${lines.join(",\n")}\n);`;
}

async function dumpRows(db, name, columns) {
  const cols = columns.map((c) => c.column_name);
  const res = await db.query(`SELECT * FROM ${ident(name)} LIMIT ${ROW_LIMIT + 1}`);
  const rows = res.rows;
  if (!rows.length) return { sql: "", count: 0, truncated: false };

  const truncated = rows.length > ROW_LIMIT;
  const kept = truncated ? rows.slice(0, ROW_LIMIT) : rows;
  const head = `INSERT INTO ${ident(name)} (${cols.map(ident).join(", ")}) VALUES`;
  const parts = [];
  for (let i = 0; i < kept.length; i += CHUNK) {
    const values = kept
      .slice(i, i + CHUNK)
      .map((row) => "  (" + cols.map((c) => literal(row[c])).join(", ") + ")")
      .join(",\n");
    parts.push(`${head}\n${values};`);
  }
  return { sql: parts.join("\n"), count: kept.length, truncated };
}

/**
 * Собирает всю схему public в один скрипт.
 * @returns {Promise<{sql: string, tables: number, rows: number, truncated: string[]}>}
 */
export async function dumpDatabase(db) {
  const columns = await readColumns(db);
  const constraints = await readConstraints(db);
  const indexes = await readIndexes(db);

  const byTable = new Map();
  for (const c of constraints) {
    if (!byTable.has(c.table_name)) byTable.set(c.table_name, []);
    byTable.get(c.table_name).push(c);
  }
  const constraintNames = new Set(constraints.map((c) => c.name));

  const out = [
    "-- Выгружено из SQL-тренажёра DataEdu",
    `-- ${new Date().toLocaleString("ru-RU")}`,
    "--",
    "-- Скрипт рассчитан на пустую схему: выполняйте в новой базе.",
    "",
  ];
  let totalRows = 0;
  const truncated = [];
  const foreign = [];

  for (const [name, cols] of [...columns].sort((a, b) => a[0].localeCompare(b[0]))) {
    const own = byTable.get(name) || [];
    const inline = own.filter((c) => c.kind === "p" || c.kind === "c" || c.kind === "u");
    for (const c of own.filter((c) => c.kind === "f")) {
      foreign.push(`ALTER TABLE ${ident(name)} ADD CONSTRAINT ${ident(c.name)} ${c.def};`);
    }

    out.push(createTable(name, cols, inline), "");

    const data = await dumpRows(db, name, cols);
    totalRows += data.count;
    if (data.truncated) truncated.push(name);
    if (data.sql) out.push(data.sql, "");

    // Последовательность после вставки готовых значений остаётся на нуле, и
    // первая же вставка без явного идентификатора упирается в конфликт ключа.
    // Форма с третьим аргументом `false` задаёт «следующее значение — ровно
    // это»: у пустой таблицы иначе пропадал бы первый идентификатор.
    for (const c of cols) {
      if (serialType(c.type, c.default_expr)) {
        out.push(
          `SELECT setval(pg_get_serial_sequence('${name}', '${c.column_name}'), ` +
            `coalesce(max(${ident(c.column_name)}), 0) + 1, false) FROM ${ident(name)};`,
          "",
        );
      }
    }
  }

  if (foreign.length) {
    out.push("-- Внешние ключи — после всех таблиц, чтобы не зависеть от порядка.", ...foreign, "");
  }

  const extra = indexes.filter((i) => !constraintNames.has(i.name));
  if (extra.length) {
    out.push("-- Индексы", ...extra.map((i) => `${i.def};`), "");
  }

  if (truncated.length) {
    out.push(`-- Данные усечены до ${ROW_LIMIT} строк: ${truncated.join(", ")}`);
  }

  return { sql: out.join("\n"), tables: columns.size, rows: totalRows, truncated };
}
