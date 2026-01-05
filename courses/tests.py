from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Course, LearningPath, WeeklySchedule, DailyTask, LearningPathEnrollment
from datetime import date


class LearningPathScheduleTests(TestCase):
	def setUp(self):
		User = get_user_model()
		self.client = Client()
		# create users
		self.student = User.objects.create_user(username='student', password='pass')
		self.staff = User.objects.create_user(username='staff', password='pass', is_staff=True)

		# create course and learning path
		self.course = Course.objects.create(title='TTest Course', description='desc', price=0)
		self.lp = LearningPath.objects.create(course=self.course, total_weeks=2, hours_per_week=3)

		# weekly schedules and daily tasks
		w1 = WeeklySchedule.objects.create(learning_path=self.lp, week_number=1, title='W1', objectives='obj', total_hours=3)
		w2 = WeeklySchedule.objects.create(learning_path=self.lp, week_number=2, title='W2', objectives='obj2', total_hours=3)

		for i in range(1,4):
			DailyTask.objects.create(weekly_schedule=w1, day_number=i, title=f'D1-{i}', description='d', duration_minutes=30)
		for i in range(1,3):
			DailyTask.objects.create(weekly_schedule=w2, day_number=i, title=f'D2-{i}', description='d', duration_minutes=30)

	def test_enrollment_and_schedule_view(self):
		# create enrollment for student with start_date
		enroll = LearningPathEnrollment.objects.create(user=self.student, learning_path=self.lp, start_date=date.today())

		# login as student
		self.client.login(username='student', password='pass')

		url = reverse('my_schedule', args=[enroll.id])
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 200)
		self.assertContains(resp, self.course.title)

	def test_schedule_access_control(self):
		# create enrollment
		enroll = LearningPathEnrollment.objects.create(user=self.student, learning_path=self.lp, start_date=date.today())
		# another non-staff user should be forbidden
		other = get_user_model().objects.create_user(username='other', password='pass')
		self.client.login(username='other', password='pass')
		resp = self.client.get(reverse('my_schedule', args=[enroll.id]))
		self.assertEqual(resp.status_code, 403)

		# staff can view
		self.client.login(username='staff', password='pass')
		resp = self.client.get(reverse('my_schedule', args=[enroll.id]))
		self.assertEqual(resp.status_code, 200)
