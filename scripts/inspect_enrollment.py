import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','mycourse.settings')
django.setup()
from courses.models import LearningPathEnrollment

EN_ID = 2
try:
    en = LearningPathEnrollment.objects.get(pk=EN_ID)
except Exception as e:
    print('Enrollment load error:', e)
    raise SystemExit(1)
print('Enrollment:', en.id, en.user.username if en.user else en.user, 'learning_path:', en.learning_path.id if en.learning_path else None, 'start_date:', en.start_date)
lp = en.learning_path
weeks = list(lp.weeks.all())
print('Total weeks on LP:', len(weeks))
for ws in weeks:
    print(' Week', ws.week_number, ws.title, '-> days count', ws.days.count())
    for d in ws.days.all():
        print('   Day', d.day_number, d.title, 'resources:', d.resources)
