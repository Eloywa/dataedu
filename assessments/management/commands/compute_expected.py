"""Предрасчёт эталонного результата SQL-заданий.

Эталонный запрос преподавателя (setup_sql + expected_sql) выполняется в одноразовой
временной схеме на сервере и сразу откатывается. Исполняется ТОЛЬКО доверенный SQL
заданий (не студенческий). Результат сохраняется в Assignment.expected_result.
"""

import psycopg
from django.conf import settings
from django.core.management.base import BaseCommand

from assessments.grading import jsonable
from assessments.models import Assignment


def _conn_params():
    db = settings.DATABASES["default"]
    return dict(
        host=db["HOST"], port=db["PORT"], user=db["USER"], password=db["PASSWORD"], dbname=db["NAME"]
    )


def _statements(sql):
    return [s.strip() for s in (sql or "").split(";") if s.strip()]


class Command(BaseCommand):
    help = "Посчитать эталонный результат (expected_result) для SQL-заданий с setup_sql."

    def handle(self, *args, **options):
        qs = (
            Assignment.objects.filter(type="sql")
            .exclude(expected_sql__isnull=True)
            .exclude(expected_sql="")
            .exclude(setup_sql__isnull=True)
            .exclude(setup_sql="")
        )
        conn = psycopg.connect(**_conn_params())  # autocommit=False
        done, failed = 0, 0
        for a in qs:
            cur = conn.cursor()
            try:
                cur.execute("DROP SCHEMA IF EXISTS tmp_chk CASCADE; CREATE SCHEMA tmp_chk;")
                cur.execute("SET search_path TO tmp_chk, public;")
                for stmt in _statements(a.setup_sql):
                    cur.execute(stmt)
                cur.execute(a.expected_sql)
                cols = [d.name for d in cur.description] if cur.description else []
                rows = [list(r) for r in cur.fetchall()] if cur.description else []
                a.expected_result = {"columns": cols, "rows": jsonable(rows)}
                a.save(update_fields=["expected_result"])
                done += 1
                self.stdout.write(f"  ✓ {a.title}: {len(rows)} строк, {len(cols)} столбцов")
            except Exception as e:  # noqa: BLE001 — показываем причину и идём дальше
                failed += 1
                self.stdout.write(self.style.WARNING(f"  ✗ {a.title}: {e}"))
            finally:
                conn.rollback()  # откат: временная схема и search_path исчезают
        conn.close()
        self.stdout.write(self.style.SUCCESS(f"Эталон посчитан: {done}, ошибок: {failed}."))
