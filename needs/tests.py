from django.test import TestCase
from needs.models import Need, Goal, Step
from django.contrib.auth.models import User
import datetime

# Create your tests here.

class NeedBasicModelTests(TestCase):
	
	def setUp(self):
		self.user1 = User.objects.create_user('root1','email2@exemple.com','root')
		self.user2 = User.objects.create_user('root2','email2@exemple.com','root')
		self.user3 = User.objects.create_user('root3','email2@exemple.com','root')

		Need.objects.create(name='mind', description='a need we have', user=self.user1)
		Need.objects.create(name='body', description='a need we have', user=self.user2)
		Need.objects.create(name='financial', description='a need we have', user=self.user3)

	def test_need_create(self):
		self.assertEqual(Need.objects.all().count(), 3)
		Need.objects.create(name='another', description='a need we have',user = self.user1)
		self.assertEqual(Need.objects.all().count(), 4)

	def test_need_get(self):
		need = Need.objects.get(name='body')
		self.assertEqual(need.description, 'a need we have')
		self.assertEqual(need.user, self.user2)

	def test_need_create_values(self):
		need = Need.objects.create(name='another', description='a need we have', user = self.user2)
		need2 = Need.objects.get(name=need.name)
		self.assertEqual(need.name, need2.name)
		self.assertEqual(need.description, need2.description)
		self.assertEqual(need.user, need2.user)

	def test_need_update_values(self):
		need = Need.objects.get(name='mind')
		need.name = 'new mind'
		need.description = 'new description'
		need.user = self.user3
		need.save()

		need2 = Need.objects.get(id=need.id)
		self.assertEqual(need.name, 'new mind')
		self.assertEqual(need.description, 'new description')
		self.assertEqual(need.user, self.user3)

	def test_need_deletion(self):
		self.assertEqual(Need.objects.all().count(), 3)
		need = Need.objects.get(name='body')
		need.delete()
		self.assertEqual(Need.objects.all().count(), 2)

	def test_user_needs_relation(self):

		count = self.user1.need_set.all().count()
		self.assertEqual(count, 1)
		Need.objects.create(name='mind', description='a need we have', user=self.user1)
		count = self.user1.need_set.all().count()
		self.assertEqual(count, 2)

class StepModelTest(TestCase):
	def test_step_creation(self):
		Step.objects.create(name='first step', description='i like it', completed=False)


class GoalModelTest(TestCase):

	def setUp(self):
		self.user1 = User.objects.create_user('root1','email2@exemple.com','root')
		# self.user2 = User.objects.create_user('root2','email2@exemple.com','root')
		# self.user3 = User.objects.create_user('root3','email2@exemple.com','root')

		Need.objects.create(name='mind', description='a need we have', user=self.user1)
		Need.objects.create(name='body', description='a need we have', user=self.user1)
		Need.objects.create(name='financial', description='a need we have', user=self.user1)

		Goal.objects.create(name="teste")

	def test_goal_create(self):
		date = datetime.date.today()
		Goal.objects.create(name="teste2", description='description teste', endDate=date)
		goal = Goal.objects.get(name='teste2')
		self.assertEqual(goal.name, 'teste2')
		self.assertEqual(goal.description, 'description teste')
		self.assertEqual(goal.endDate, date)
