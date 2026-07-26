from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        from django.contrib.auth.signals import user_logged_in
        from django.utils import timezone

        def update_last_seen(sender, user, request, **kwargs):
            type(user).objects.filter(pk=user.pk).update(last_seen_at=timezone.now())
            # Событие входа + серия «Неделя без пропусков» (не должно ломать вход).
            try:
                from gamification.services import record_login

                record_login(user)
            except Exception:
                pass

        user_logged_in.connect(update_last_seen, dispatch_uid="accounts_last_seen")
