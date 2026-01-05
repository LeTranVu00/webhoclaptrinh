from django.core.management.base import BaseCommand
from courses.models import DailyTask
from courses.templatetags.vn_filters import resource_url, resource_embed


class Command(BaseCommand):
    help = 'List DailyTask.resources and normalized URLs (for debugging)'

    def handle(self, *args, **options):
        qs = DailyTask.objects.all()
        self.stdout.write(f"Total DailyTask: {qs.count()}")
        for dt in qs:
            raw = dt.resources or ''
            url = resource_url(raw)
            embed = resource_embed(raw)
            self.stdout.write(f"id={dt.id} raw={raw!r} -> url={url!r} embed={embed!r}")
