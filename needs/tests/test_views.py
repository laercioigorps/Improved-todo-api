from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from needs.models import Need, Goal, Step, Iteration, Delivery
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

class StepViewTest(TestCase):

	def setUp(self):
		self.user1 = User.objects.create_user('root1','email2@exemple.com','root')

		self.need1 = Need.objects.create(name='need1', description='need1 description', user=self.user1)
		self.need2 = Need.objects.create(name='need2', description='need2 description', user=self.user1)

		self.goal1 = Goal.objects.create(name="goal1", need=self.need1)
		self.goal2 = Goal.objects.create(name="goal2", need=self.need1)

		self.step1 = Step.objects.create(name='step1', description='step1Description',
			completed=False,goal = self.goal1)
		self.step2 = Step.objects.create(name='step2', description='step2Description',
			completed=False,goal = self.goal1)
		self.step3 = Step.objects.create(name='step3', description='step3Description',
			completed=False,goal = self.goal1)

	def test_step_creation(self):
		count = Step.objects.all().count()
		self.assertEqual(count, 3)

		client = APIClient()
		client.login(username='root1', password='root')

		response = client.post('/step/',{
				'name' : 'newStep',
				'description' : 'newStepDescription',
				'completed' : True,
				'goal' : self.goal2.id,
			}, format='json')

		self.assertEqual(response.status_code, 200)
		count = Step.objects.all().count()
		self.assertEqual(count, 4)

	def test_step_list(self):
		client = APIClient()
		client.login(username='root1', password='root')

		response = client.get('/step/')
		self.assertEqual(response.status_code, 200)

	def test_step_retrieve(self):
		client = APIClient()
		client.login(username='root1', password='root')

		response = client.get('/step/1/')

		stream = io.BytesIO(response.content)
		data = JSONParser().parse(stream)

		self.assertEqual(data['name'], 'step1')
		self.assertEqual(data['description'], 'step1Description')
		self.assertEqual(data['completed'], False)
		self.assertEqual(data['goal'], self.goal1.id)

	def test_step_update(self):
		client = APIClient()
		client.login(username='root1', password='root')

		response = client.put('/step/1/', {
			'name' : 'step1Updated',
			'description' : 'step1DescriptionUpdated',
			'completed' : True,
			'goal' : self.goal2.id,
			}, format='json')
		
		self.assertEqual(response.status_code, 200)
		step = Step.objects.get(id=1)
		self.assertEqual(step.name, 'step1Updated')
		self.assertEqual(step.description, 'step1DescriptionUpdated')
		self.assertIs(step.completed, True)
		self.assertEqual(step.goal, self.goal2)

	def test_step_delete(self):
		count = Step.objects.all().count()
		self.assertEqual(count, 3)

		client = APIClient()
		client.login(username='root1', password='root')

		response = client.delete('/step/1/')
		self.assertEqual(response.status_code, 200)

		count = Step.objects.all().count()
		self.assertEqual(count, 2)

class IterationViewTest(TestCase):

	def setUp(self):
		self.user1 = User.objects.create_user('root1','email2@exemple.com','root')

		self.need1 = Need.objects.create(name='need1', description='need1 description', user=self.user1)
		self.need2 = Need.objects.create(name='need2', description='need2 description', user=self.user1)

		self.goal1 = Goal.objects.create(name="goal1", need=self.need1)
		self.goal2 = Goal.objects.create(name="goal2", need=self.need1)

		self.step1 = Step.objects.create(name='step1', description='step1Description',
			completed=False,goal = self.goal1)
		self.step2 = Step.objects.create(name='step2', description='step2Description',
			completed=False,goal = self.goal1)
		self.step3 = Step.objects.create(name='step3', description='step3Description',
			completed=False,goal = self.goal1)

		self.iteration1 = Iteration.objects.create(number=1, completed = False,
		date = datetime.date.today(), goal = self.goal1)
		self.iteration2 = Iteration.objects.create(number=2, completed = False,
		date = datetime.date.today(), goal = self.goal1)
		self.iteration3 = Iteration.objects.create(number=1, completed = True,
		date = datetime.date.today(), goal = self.goal2)

	def test_iteration_creation(self):
		count = Iteration.objects.all().count()
		self.assertEqual(count, 3)

		client = APIClient()
		client.login(username='root1', password='root')

		response =client.post('/iteration/', {
			'number' : 2,
			'completed' : True,
			'date' : datetime.date.today(),
			'goal': self.goal2.id,
			}, format='json')

		self.assertEqual(response.status_code, 200)
		count = Iteration.objects.all().count()
		self.assertEqual(count, 4)

	def test_iteration_list(self):
		client = APIClient()
		client.login(username='root1', password='root')
		response = client.get('/iteration/')

		self.assertEqual(response.status_code, 200)

	def test_iteration_update(self):
		count = Iteration.objects.all().count()
		self.assertEqual(count, 3)

		client = APIClient()
		client.login(username='root1', password='root')

		response = client.put('/iteration/1/', {
			'number' : 2,
			'completed' : True,
			'date' : datetime.date.today(),
			'goal': self.goal2.id,
			}, format='json')
		self.assertEqual(response.status_code, 200)
		count = Iteration.objects.all().count()
		self.assertEqual(count, 3)

		iteration = Iteration.objects.get(id=1)
		self.assertEqual(iteration.number, 2)
		self.assertIs(iteration.completed, True)
		self.assertEqual(iteration.date, datetime.date.today())
		self.assertEqual(iteration.goal, self.goal2)

	def test_iteration_retrieve(self):
		client = APIClient()
		client.login(username='root1', password='root')

		response = client.get('/iteration/1/')
		self.assertEqual(response.status_code, 200)

		stream = io.BytesIO(response.content)
		data = JSONParser().parse(stream)

		self.assertEqual(data['number'], 1)
		self.assertEqual(data['completed'], False)
		self.assertEqual(data['date'], datetime.date.today().strftime('%Y-%m-%d'))
		self.assertEqual(data['goal'], self.goal1.id)

	def test_iteration_delete(self):
		client = APIClient()
		client.login(username='root1', password='root')

		count = Iteration.objects.all().count()
		self.assertEqual(count, 3)

		response = client.delete('/iteration/1/')

		count = Iteration.objects.all().count()
		self.assertEqual(count, 2)


class DeliveryViewTest(TestCase):

	def setUp(self):
		self.user1 = User.objects.create_user('root1','email2@exemple.com','root')

		self.need1 = Need.objects.create(name='need1', description='need1 description', user=self.user1)
		self.need2 = Need.objects.create(name='need2', description='need2 description', user=self.user1)

		self.goal1 = Goal.objects.create(name="goal1", need=self.need1)
		self.goal2 = Goal.objects.create(name="goal2", need=self.need1)

		self.step1 = Step.objects.create(name='step1', description='step1Description',
			completed=False,goal = self.goal1)
		self.step2 = Step.objects.create(name='step2', description='step2Description',
			completed=False,goal = self.goal1)
		self.step3 = Step.objects.create(name='step3', description='step3Description',
			completed=False,goal = self.goal1)

		self.iteration1 = Iteration.objects.create(number=1, completed = False,
		date = datetime.date.today(), goal = self.goal1)
		self.iteration2 = Iteration.objects.create(number=2, completed = False,
		date = datetime.date.today(), goal = self.goal1)
		self.iteration3 = Iteration.objects.create(number=1, completed = True,
		date = datetime.date.today(), goal = self.goal2)

		self.delivery1 = Delivery.objects.create(name='delivery1', description='delivery1Description',
			step = self.step1, iteration = self.iteration1, completed= False)
		self.delivery2 = Delivery.objects.create(name='delivery2', description='delivery2Description',
			step = self.step1, iteration = self.iteration1, completed=False)
		self.delivery3 = Delivery.objects.create(name='delivery3', description='delivery1Description',
			step = self.step2, iteration = self.iteration1, completed=False)

	def test_delivery_list(self):
		client = APIClient()
		client.login(username='root1', password='root')
		response = client.get('/delivery/')

		self.assertEqual(response.status_code, 200)

	def test_delivery_creation(self):
		count = Delivery.objects.all().count()
		self.assertEqual(count, 3)

		client = APIClient()
		client.login(username='root1', password='root')

		response = client.post('/delivery/', {
			'name' : 'newIteration',
			'description' : 'newIterationDescription',
			'step' : self.step2.id,
			'iteration': self.iteration1.id,
			'completed': True,
			}, format='json')

		count = Delivery.objects.all().count()
		self.assertEqual(count, 4)

	def test_delivery_retrieve(self):
		client = APIClient()
		client.login(username='root1', password='root')

		response = client.get('/delivery/1/')
		self.assertEqual(response.status_code, 200)

		stream = io.BytesIO(response.content)
		data = JSONParser().parse(stream)

		self.assertEqual(data['name'], 'delivery1')
		self.assertEqual(data['description'], 'delivery1Description')
		self.assertEqual(data['step'], self.step1.id)
		self.assertEqual(data['iteration'], self.iteration1.id)
		self.assertEqual(data['completed'], False)

	def test_delivery_update(self):
		count = Delivery.objects.all().count()
		self.assertEqual(count, 3)

		client = APIClient()
		client.login(username='root1', password='root')

		response = client.put('/delivery/1/', {
			'name' : 'Iteration1Updated',
			'description' : 'Iteration1DescriptionUpdated',
			'step' : self.step2.id,
			'iteration': self.iteration1.id,
			'completed': True,
			}, format='json')


		self.assertEqual(response.status_code, 200)
		count = Iteration.objects.all().count()
		self.assertEqual(count, 3)

		delivery = Delivery.objects.get(id=1)
		self.assertEqual(delivery.name, 'Iteration1Updated')
		self.assertEqual(delivery.description, 'Iteration1DescriptionUpdated')
		self.assertEqual(delivery.step, self.step2)
		self.assertEqual(delivery.iteration, self.iteration1)
		self.assertIs(delivery.completed, True)

	def test_delivery_delete(self):
		count = Delivery.objects.all().count()
		self.assertEqual(count, 3)

		client = APIClient()
		client.login(username='root1', password='root')

		response = client.delete('/delivery/1/')

		self.assertEqual(response.status_code, 200)
		count = Delivery.objects.all().count()
		self.assertEqual(count, 2)




		

