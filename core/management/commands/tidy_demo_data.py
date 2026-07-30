"""Приведение демо-данных в порядок перед скриншотами и апробацией.

Команда идемпотентна: её можно запускать повторно.

Две задачи, обе — следствие переливки данных из Next-версии:

1. **Обезличивание учётной записи автора.** В перелитых данных остался аккаунт с
   настоящими ФИО и институциональным адресом. Роль у него административная, поэтому он
   легко попадает в скриншот админки для диссертации. Данные принадлежат самому автору,
   но публиковать в тексте работы адрес и ФИО незачем — заменяем на псевдоним
   (см. §17.14 архитектурного документа: платформа не хранит персональных данных).
   Пароль не трогаем — доступ сохраняется, меняется только логин.

2. **Ремонт legacy-заданий.** Из Next-версии приехали SQL-задания без заготовки данных
   (`setup_sql`), поэтому эталон для них посчитать нельзя и автопроверка не работает:
   - «Выбрать всех студентов» — дописываем заготовку, эталон считается штатно;
   - «Создать таблицу студентов» — это DDL: сравнение результата к нему неприменимо
     (запрос студента не возвращает строк). Переводим в тип `ddl` — такие задания идут
     на проверку преподавателя, а не в автопроверку.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from assessments.admin import rows_cols_summary
from assessments.expected import ExpectedError, compute_and_save
from assessments.models import Assignment

# Логин автора → псевдоним. Пароль и права сохраняются.
AUTHOR_OLD_USERNAME = "achertovikov"
AUTHOR_NEW_USERNAME = "author"
AUTHOR_DISPLAY_NAME = "Автор платформы"

# Заготовка для «Выбрать всех студентов»: столбцы те же, что в описании парного
# задания «Создать таблицу студентов» (id, full_name, group_name).
SELECT_ALL_SETUP = """
CREATE TABLE students (
  id         serial PRIMARY KEY,
  full_name  text NOT NULL,
  group_name text
);
INSERT INTO students (full_name, group_name) VALUES
  ('Анна Соколова',    'ПИ-101'),
  ('Дмитрий Соколов',  'ПИ-101'),
  ('Мария Иванова',    'ПИ-102'),
  ('Павел Кузнецов',   'ПИ-102'),
  ('Ольга Попова',     'МО-201');
""".strip()


class Command(BaseCommand):
    help = "Обезличить учётную запись автора и починить legacy-задания из Next-версии."

    def handle(self, *args, **options):
        with transaction.atomic():
            self._pseudonymize_author()
            self._fix_select_all()
            self._fix_ddl_task()

    def _pseudonymize_author(self):
        from accounts.models import User

        if User.objects.filter(username=AUTHOR_NEW_USERNAME).exists():
            self.stdout.write(f"Логин «{AUTHOR_NEW_USERNAME}» уже есть — обезличивание пропущено.")
            return
        user = User.objects.filter(username=AUTHOR_OLD_USERNAME).first()
        if user is None:
            self.stdout.write("Учётная запись автора не найдена — обезличивание не требуется.")
            return

        user.username = AUTHOR_NEW_USERNAME
        user.display_name = AUTHOR_DISPLAY_NAME
        user.email = None  # адрес платформе не нужен
        user.save(update_fields=["username", "display_name", "email"])
        self.stdout.write(
            self.style.SUCCESS(
                f"Учётная запись обезличена: логин теперь «{AUTHOR_NEW_USERNAME}», "
                f"имя «{AUTHOR_DISPLAY_NAME}», email очищен. Пароль не менялся."
            )
        )

    def _fix_select_all(self):
        a = Assignment.objects.filter(title="Выбрать всех студентов", type="sql").first()
        if a is None:
            self.stdout.write("Задание «Выбрать всех студентов» не найдено.")
            return
        if a.expected_result and (a.setup_sql or "").strip():
            self.stdout.write("«Выбрать всех студентов»: эталон уже на месте.")
            return

        a.setup_sql = SELECT_ALL_SETUP
        a.save(update_fields=["setup_sql"])
        try:
            result = compute_and_save(a)
            self.stdout.write(
                self.style.SUCCESS(
                    "«Выбрать всех студентов»: заготовка дописана, эталон посчитан ("
                    + rows_cols_summary(len(result["rows"]), len(result["columns"]))
                    + ")."
                )
            )
        except ExpectedError as e:
            self.stdout.write(self.style.ERROR(f"«Выбрать всех студентов»: {e}"))

    def _fix_ddl_task(self):
        a = Assignment.objects.filter(title="Создать таблицу студентов").first()
        if a is None:
            self.stdout.write("Задание «Создать таблицу студентов» не найдено.")
            return
        if a.type == "ddl":
            self.stdout.write("«Создать таблицу студентов»: уже помечено как DDL.")
            return

        a.type = "ddl"
        a.save(update_fields=["type"])
        self.stdout.write(
            self.style.SUCCESS(
                "«Создать таблицу студентов» → тип «ddl»: сравнение результата к DDL "
                "неприменимо, задание идёт на проверку преподавателя."
            )
        )
