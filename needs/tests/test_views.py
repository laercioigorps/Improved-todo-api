from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from needs.models import Need, Goal
from needs.serializers import NeedSerializer
from rest_framework.parsers import JSONParser
import io
import datetime

class NeedViewTest(TestCase):

	def setUp(self):
		self.user1 = User.objects.create_user('root1','email1@exemple.com','root')
		self.user2 = User.objects.create_user('root2','email2@exemple.com','root')

		self.need1 = Need.objects.create(name='need1', description='need1 description', user=self.user1)
		self.need2 = Need.objects.create(name='need2', description='need2 description', user=self.user1)
		self.need3 = Need.objects.create(name='need3', description='need3 description', user=self.user1)

	def test_need_create(self):
		count = Need.objects.all().count()
		self.assertEqual(count, 3)

		client = APIClient()
		client.login(username='root1', password='root')
		response = client.post('/need/', 
			{
			'name': 'newNeed',
			'description' : 'newneedDescription',
			}, format='json')
		self.assertEqual(response.status_code , 201)

		count = Need.objects.all().count()
		self.assertEqual(count, 4)
		
		need = Need.objects.get(name='newNeed')
		self.assertEqual(need.description, 'newneedDescription')

	def test_need_retrieve(self):
		client = APIClient()
		client.login(username='root1', password='root')
		response = client.get('/need/2/')

		self.assertEqual(response.status_code, 200)

		stream = io.BytesIO(response.content)
		data = JSONParser().parse(stream)

		serializer = NeedSerializer(data = data)
		valid = serializer.is_valid()
		validated_data = serializer.validated_data
		self.assertIs(valid, True)
		self.assertEqual(validated_data['name'], 'need2')
		self.assertEqual(validated_data['description'], 'need2 description')

	def test_need_update(self):
		count = Need.objects.all().count()
		self.assertEqual(count, 3)

		client = APIClient()
		client.login(username='root1', password='root')
		response = client.put('/need/2/', 
			{
			'name': 'need2Updated',
			'description' : 'need2DescriptionUpdated',
			}, format='json')

		need = Need.objects.get(id=2)
		self.assertEqual(need.name, 'need2Updated')
		self.assertEqual(need.description, 'need2DescriptionUpdated')

		count = Need.objects.all().count()
		self.assertEqual(count, 3)

	def test_need_delete(self):
		count = Need.objects.all().count()
		self.assertEqual(count, 3)

		client = APIClient()
		client.login(username='root1', password='root')
		client.delete('/need/2/')

		count = Need.objects.all().count()
		self.assertEqual(count, 2)

class GoalViewTest(TestCase):

	def setUp(self):
		self.user1 = User.objects.create_user('root1','email1@exemple.com','root')
		self.user2 = User.objects.create_user('root2','email2@exemple.com','root')

		self.need1 = Need.objects.create(name='need1', description='need1 description', user=self.user1)
		self.need2 = Need.objects.create(name='need2', description='need2 description', user=self.user1)
		self.need3 = Need.objects.create(name='need3', description='need3 description', user=self.user1)

		self.today = datetime.date.today()
		self.goal1 = Goal.objects.create(name="goal1",description='goal1Description',
			endDate=self.today, need=self.need1)
		self.goal2 = Goal.objects.create(name="goal2",description='goal2Description',
			endDate=self.today, need=self.need1)
		self.goal3 = Goal.objects.create(name="goal3",description='goal3Description',
			endDate=self.today, need=self.need1)

	def test_goal_create(self):
		count = Goal.objects.all().count()
		self.assertEqual(count, 3)
		endDate = datetime.date.today()

		client = APIClient()
		client.login(username='root1', password='root')
		response = client.post('/goal/', {
			'name' : 'newGoal',
			'description' : 'newGoalDescription',
			'endDate' : endDate,
			'need' : self.need1.id,
			}, format='json')

		self.assertEqual(response.status_code, 200)

		count = Goal.objects.all().count()
		self.assertEqual(count, 4)

		goal = Goal.objects.get(id=4)
		self.assertEqual(goal.name, 'newGoal')
		self.assertEqual(goal.description, 'newGoalDescription')
		self.assertEqual(goal.endDate, endDate)
		self.assertEqual(goal.need, self.need1)

	def test_goal_retrieve(self):
		client = APIClient()
		client.login(username='root1', password='root')
		response = client.get('/goal/1/')

		stream = io.BytesIO(response.content)
		data = JSONParser().parse(stream)

		self.assertEqual(data['name'], 'goal1')
		self.assertEqual(data['description'], 'goal1Description')
		self.assertEqual(data['endDate'], self.today.strftime('%Y-%m-%d'))
		self.assertEqual(data['need'], self.need1.id)


	def test_goal_list(self):
		client = APIClient()
		client.login(username='root1', password='root')
		response = client.get('/goal/')

		self.assertEqual(response.status_code, 200)

	def test_goal_update(self):
		client = APIClient()
		client.login(username='root1', password='root')	
		client.put('/goal/1/', {
			'name':'newNameForGoal1',
			'description' : 'newDescriptionForGoal1',
			'endDate' : self.today,
			'need' : self.need2.id,
			}, format='json')

		goal = Goal.objects.get(id=1)
		self.assertEqual(goal.name, 'newNameForGoal1')
		self.assertEqual(goal.description, 'newDescriptionForGoal1')
		self.assertEqual(goal.endDate, self.today)
		self.assertEqual(goal.need, self.need2)


	def test_goal_delete(self):
		count = Goal.objects.all().count()
		self.assertEqual(count, 3)

		client = APIClient()
		client.login(username='root1', password='root')
		client.delete('/goal/1/')

		count = Goal.objects.all().count()
		self.assertEqual(count, 2)





		

