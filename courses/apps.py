from django.apps import AppConfig


class CoursesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'courses'
    def ready(self):
        # Import signal handlers to ensure they're registered
        try:
            from . import signals  # noqa: F401
        except Exception:
            pass
