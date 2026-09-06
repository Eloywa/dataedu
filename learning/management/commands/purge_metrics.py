"""Удаление устаревших событий ленты активности.

Ограничение срока хранения — требование минимизации: держать учебную телеметрию
бессрочно незачем. Для аналитики и отчётов хватает текущего учебного года, а всё
сверх того лишь увеличивает объём обрабатываемых данных.

Срок задаётся `METRICS_RETENTION_DAYS` (по умолчанию 400 дней — учебный год с запасом).
Удаляются только события `activities`; учебные результаты (прогресс, попытки, решения)
не трогаются — они нужны, пока существует учётная запись.

Команду имеет смысл поставить в планировщик (раз в сутки). Перед реальным удалением
удобно посмотреть объём: `manage.py purge_metrics --dry-run`.
"""

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from learning.models import Activity


class Command(BaseCommand):
    help = "Удалить события ленты активности старше METRICS_RETENTION_DAYS"

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=None,
            help="переопределить срок хранения (по умолчанию METRICS_RETENTION_DAYS)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="только показать, сколько будет удалено",
        )

    def handle(self, *args, **options):
        days = options["days"] or settings.METRICS_RETENTION_DAYS
        cutoff = timezone.now() - timezone.timedelta(days=days)
        stale = Activity.objects.filter(created_at__lt=cutoff)
        count = stale.count()

        self.stdout.write(f"Срок хранения: {days} дней (события до {cutoff:%d.%m.%Y}).")

        if count == 0:
            self.stdout.write(self.style.SUCCESS("Устаревших событий нет."))
            return

        if options["dry_run"]:
            self.stdout.write(
                self.style.WARNING(f"Будет удалено событий: {count} (пробный запуск).")
            )
            return

        stale.delete()
        self.stdout.write(self.style.SUCCESS(f"Удалено событий: {count}."))
