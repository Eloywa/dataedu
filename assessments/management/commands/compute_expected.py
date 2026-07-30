"""Пакетный предрасчёт эталонных результатов SQL-заданий.

Сама логика расчёта живёт в `assessments/expected.py` — тем же кодом пользуется кнопка
«Посчитать эталон» в админке. Команда остаётся для пакетного прогона (например, после
`seed_practice` или переливки данных).
"""

import psycopg
from django.core.management.base import BaseCommand

from assessments.expected import ExpectedError, _conn_params, compute_and_save
from assessments.models import Assignment


class Command(BaseCommand):
    help = "Посчитать эталонный результат (expected_result) для SQL-заданий с setup_sql."

    def add_arguments(self, parser):
        parser.add_argument(
            "--only-missing",
            action="store_true",
            help="считать только там, где эталона ещё нет",
        )

    def handle(self, *args, **options):
        qs = (
            Assignment.objects.filter(type="sql")
            .exclude(expected_sql__isnull=True)
            .exclude(expected_sql="")
            .exclude(setup_sql__isnull=True)
            .exclude(setup_sql="")
        )
        if options["only_missing"]:
            qs = qs.filter(expected_result__isnull=True)

        if not qs.exists():
            self.stdout.write("Заданий для расчёта не найдено.")
            return

        # Одно соединение на весь прогон: каждая задача откатывается отдельно.
        conn = psycopg.connect(**_conn_params())
        done, failed = 0, 0
        try:
            for a in qs:
                try:
                    result = compute_and_save(a, conn=conn)
                    done += 1
                    self.stdout.write(
                        f"  ✓ {a.title}: {len(result['rows'])} строк, "
                        f"{len(result['columns'])} столбцов"
                    )
                except ExpectedError as e:
                    failed += 1
                    self.stdout.write(self.style.WARNING(f"  ✗ {a.title}: {e}"))
        finally:
            conn.close()

        style = self.style.SUCCESS if not failed else self.style.WARNING
        self.stdout.write(style(f"Эталон посчитан: {done}, ошибок: {failed}."))
