from django.core.management.base import BaseCommand
from courses.models import DailyTask
from courses.templatetags.vn_filters import resource_url
import csv
import os


class Command(BaseCommand):
    help = 'Fix DailyTask.resources using safe heuristics and back up original values'

    def handle(self, *args, **options):
        qs = DailyTask.objects.all()
        total = qs.count()
        self.stdout.write(f'Total DailyTask: {total}')
        backup_path = os.path.join(os.getcwd(), 'dailytask_resources_backup.csv')
        with open(backup_path, 'w', newline='', encoding='utf-8') as bf:
            writer = csv.writer(bf)
            writer.writerow(['id', 'weekly_schedule_id', 'raw_resources', 'new_resources', 'description_before'])
            for dt in qs:
                raw = dt.resources or ''
                normalized = resource_url(raw)
                new = None
                desc_before = dt.description or ''

                if not raw:
                    new = ''
                    writer.writerow([dt.id, dt.weekly_schedule_id, raw, new, desc_before])
                    continue

                if normalized:
                    # resource_url already returned something usable
                    if normalized != raw:
                        new = normalized
                        dt.resources = new
                        dt.save()
                    else:
                        new = raw
                    writer.writerow([dt.id, dt.weekly_schedule_id, raw, new, desc_before])
                    continue

                # normalized is empty -> apply heuristics
                s = raw.strip()
                if s.isdigit():
                    # map numeric tokens to an external placeholder pattern
                    new = f'https://example.com/resource/{s}'
                    dt.resources = new
                    dt.save()
                elif s.isalnum() and len(s) == 11:
                    new = f'https://youtu.be/{s}'
                    dt.resources = new
                    dt.save()
                else:
                    # Unknown token: clear resources and append admin note to description
                    new = ''
                    note = f"\n\n[NOTE] Original resources token: {raw} — please update in Admin."
                    if note.strip() not in desc_before:
                        dt.description = (desc_before or '') + note
                        dt.save()

                writer.writerow([dt.id, dt.weekly_schedule_id, raw, new, desc_before])

        self.stdout.write(self.style.SUCCESS(f'Backup written to {backup_path}'))
        self.stdout.write(self.style.SUCCESS('Resource fix pass completed.'))
