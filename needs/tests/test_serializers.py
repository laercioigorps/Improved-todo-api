from django.test import TestCase
from needs.models import Need, Goal, Step, Iteration, Delivery
from needs.serializers import NeedSerializer, GoalSerializer, StepSerializer, IterationSerializer
from django.contrib.auth.models import User
import datetime
import io
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


def get_json_data(serializerData):
	content = JSONRenderer().render(serializerData)
	stream = io.BytesIO(content)
	data = JSONParser().parse(stream)
	return data


class NeedSerializerTest(TestCase):

	def setUp(self):
		self.user1 = User.objects.create_user('root1','email2@exemple.com','root')

		self.need1 = Need.objects.create(name='need1', description='need1 description', user= self.user1)
		self.need2 = Need.objects.create(name='need2', description='need2 description', user= self.user1)
		self.need3 = Need.objects.create(name='need3', description='need3 description', user= self.user1)

	def test_need_creation(self):
		count = Need.objects.all().count()
		self.assertEqual(count, 3)

		need = Need(name='mind', description='a need we have' )
		needSerializer = NeedSerializer(need)
		data = get_json_data(needSerializer.data)

		serializer = NeedSerializer(data=data)
		serializer.is_valid()
		serializer.save(user=self.user1)

		count = Need.objects.all().count()
		self.assertEqual(count, 4)

		getNeed = Need.objects.get(name='mind')
		self.assertEqual(getNeed.user , self.user1)
		self.assertEqual(getNeed.description , 'a need we have')
		

	def test_need_update(self):
		count = Need.objects.all().count()
		self.assertEqual(count, 3)

		need = Need.objects.get(name='need1')
		need.name= 'need1Updated'
		need.description = 'need1DescriptionUpdated'

		needSerializer = NeedSerializer(need)

		data = get_json_data(needSerializer.data)

		serializer = NeedSerializer(need, data=data)

		serializer.is_valid()
		serializer.save()

		getNeed = Need.objects.get(id=need.id)
		self.assertEqual(getNeed.user , self.user1)
		self.assertEqual(getNeed.name , 'need1Updated')
		self.assertEqual(getNeed.description , 'need1DescriptionUpdated')
		self.assertEqual(getNeed.id , need.id)

		count = Need.objects.all().count()
		self.assertEqual(count, 3)

class GoalSerializerTest(TestCase):

	def setUp(self):
		self.user1 = User.objects.create_user('root1','email2@exemple.com','root')

		self.need1 = Need.objects.create(name='need1', description='need1 description', user=self.user1)
		self.need2 = Need.objects.create(name='need2', description='need2 description', user=self.user1)


		self.goal1 = Goal.objects.create(name="goal1", need=self.need1)
		self.goal2 = Goal.objects.create(name="goal2", need=self.need1)
		self.goal3 = Goal.objects.create(name="goal3", need=self.need2)

	def test_goal_create(self):
		count = Goal.objects.all().count()
		self.assertEqual(count, 3)

		goal = Goal(name="newGoal", description='new goal description',
		need=self.need1, endDate= datetime.date.today())

		goalSerializer = GoalSerializer(goal)
		data = get_json_data(goalSerializer.data)

		serializer = GoalSerializer(data=data)
		serializer.is_valid()
		serializer.save()

		count = Goal.objects.all().count()
		self.assertEqual(count, 4)

	def test_goal_update(self):
		goal = Goal.objects.get(id= self.goal1.id)
		goal.name = 'goal1Updated'
		goal.description = 'goal1DescriptionUpdated'
		nextWeekDate = datetime.date.today() + datetime.timedelta(days=7)
		goal.endDate = nextWeekDate

		goalSerializer = GoalSerializer(goal)
		data = get_json_data(goalSerializer.data)

		serializer = GoalSerializer(goal, data=data)
		serializer.is_valid()
		serializer.save()

		getGoal = Goal.objects.get(id=goal.id)
		self.assertEqual(goal.name, 'goal1Updated')
		self.assertEqual(goal.description, 'goal1DescriptionUpdated')
		self.assertEqual(goal.endDate, nextWeekDate)


class StepSerializerTest(TestCase):

	def setUp(self):
		self.user1 = User.objects.create_user('root1','email2@exemple.com','root')

		self.need1 = Need.objects.create(name='need1', description='need1 description', user=self.user1)
		self.need2 = Need.objects.create(name='need2', description='need2 description', user=self.user1)

		self.goal1 = Goal.objects.create(name="goal1", need=self.need1)
		self.goal2 = Goal.objects.create(name="goal2", need=self.need1)
		self.goal3 = Goal.objects.create(name="goal3", need=self.need2)

		self.step1 = Step.objects.create(name='step1', description='step1Description',
			completed=False,goal = self.goal1)
		self.step2 = Step.objects.create(name='step2', description='step2Description',
			completed=False,goal = self.goal1)
		self.step3 = Step.objects.create(name='step3', description='step3Description',
			completed=False,goal = self.goal1)

	def test_step_creation(self):
		count = Step.objects.all().count()
		self.assertEqual(count, 3)

		step = Step(name='newStep', description='step3NewDescription',
			completed=True,goal = self.goal2)
		stepSerializer = StepSerializer(step)
		data = get_json_data(stepSerializer.data)

		serializer = StepSerializer(data=data)
		serializer.is_valid()
		serializer.save()

		count = Step.objects.all().count()
		self.assertEqual(count, 4)

	def test_step_update(self):

		count = Step.objects.all().count()
		self.assertEqual(count, 3)

		step = Step.objects.get(id=self.step1.id)

		step.name = 'newStepName'
		step.description = 'newStepDescription'
		step.completed = True

		stepSerializer = StepSerializer(step)
		data = get_json_data(stepSerializer.data)

		serializer = StepSerializer(step, data=data)
		serializer.is_valid()
		serializer.save()

		count = Step.objects.all().count()
		self.assertEqual(count, 3)

		getStep = Step.objects.get(id=step.id)
		self.assertEqual(getStep.name , 'newStepName')
		self.assertEqual(getStep.description, 'newStepDescription')
		self.assertEqual(getStep.completed, True)

class IterationSerializerTest(TestCase):
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

		iteration = Iteration(number=2, completed=False,
		date=datetime.date.today(), goal=self.goal1)

		iterationSerializer = IterationSerializer(iteration)
		data = get_json_data(iterationSerializer.data)

		serializer = IterationSerializer(data=data)
		serializer.is_valid()
		serializer.save()

		count = Iteration.objects.all().count()
		self.assertEqual(count, 4)

	def test_iteration_update(self):

		iteration = Iteration.objects.get(id=self.iteration1.id)
		iteration.number = 2
		iteration.completed = True
		nextWeekDate = datetime.date.today() + datetime.timedelta(days=7)
		iteration.date = nextWeekDate
		iteration.goal = self.goal2

		iterationSerializer = IterationSerializer(iteration)
		data = get_json_data(iterationSerializer.data)

		serializer = IterationSerializer(iteration, data=data)
		serializer.is_valid()
		serializer.save()

		count = Iteration.objects.all().count()
		self.assertEqual(count, 3)

		getIteration = Iteration.objects.get(id=iteration.id)
		self.assertEqual(getIteration.number, 2)
		self.assertEqual(getIteration.completed, True)
		self.assertEqual(getIteration.date, nextWeekDate)
		self.assertEqual(getIteration.goal, self.goal2)










