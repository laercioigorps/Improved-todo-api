from django.test import TestCase
from needs.models import Need, Goal, Step, Iteration, Delivery
from django.contrib.auth.models import User
import datetime

# Create your tests here.


class NeedBasicModelTests(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            'root1', 'email2@exemple.com', 'root')
        self.user2 = User.objects.create_user(
            'root2', 'email2@exemple.com', 'root')
        self.user3 = User.objects.create_user(
            'root3', 'email2@exemple.com', 'root')

        Need.objects.create(
            name='mind', description='a need we have', user=self.user1)
        Need.objects.create(
            name='body', description='a need we have', user=self.user2)
        Need.objects.create(
            name='financial', description='a need we have', user=self.user3)

    def test_need_create(self):
        self.assertEqual(Need.objects.all().count(), 3)
        Need.objects.create(
            name='another', description='a need we have', user=self.user1)
        self.assertEqual(Need.objects.all().count(), 4)

    def test_need_get(self):
        need = Need.objects.get(name='body')
        self.assertEqual(need.description, 'a need we have')
        self.assertEqual(need.user, self.user2)

    def test_need_create_values(self):
        need = Need.objects.create(
            name='another', description='a need we have', user=self.user2)
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
        Need.objects.create(
            name='mind', description='a need we have', user=self.user1)
        count = self.user1.need_set.all().count()
        self.assertEqual(count, 2)


class StepModelTest(TestCase):

    def setUp(self):

        self.user1 = User.objects.create_user(
            'root3', 'email2@exemple.com', 'root')

        self.need1 = Need.objects.create(
            name='mind', description='a need we have', user=self.user1)

        self.goal1 = Goal.objects.create(
            name='goal1', endDate=datetime.date.today(), need=self.need1)

        self.step1 = Step.objects.create(name='first step', description='I like it',
                                         completed=False, goal=self.goal1)
        self.step2 = Step.objects.create(name='second step', description='I kind of like it',
                                         completed=False, goal=self.goal1)
        self.step3 = Step.objects.create(name='third step', description='I dont know if I like it',
                                         completed=False, goal=self.goal1)

    def test_step_creation(self):
        count = Step.objects.all().count()
        self.assertEqual(count, 3)
        Step.objects.create(name='first step', description='I like it will pass',
                            completed=False, goal=self.goal1)
        count = Step.objects.all().count()
        self.assertEqual(count, 4)

    def test_need_retrieve_and_update(self):
        step = Step.objects.get(name='first step')
        step.name = 'firstNameUpdate'
        step.description = 'firstDescriptionUpdate'
        step.completed = True
        step.save()

        stepUpdated = Step.objects.get(name='firstNameUpdate')

        self.assertEqual(stepUpdated.name, 'firstNameUpdate')
        self.assertEqual(stepUpdated.description, 'firstDescriptionUpdate')
        self.assertIs(stepUpdated.completed, True)

    def test_step_deletion(self):
        count = Step.objects.all().count()
        self.assertEqual(count, 3)
        step = Step.objects.get(name='first step')
        step.delete()
        count = Step.objects.all().count()
        self.assertEqual(count, 2)


class GoalModelTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            'root1', 'email2@exemple.com', 'root')
        # self.user2 = User.objects.create_user('root2','email2@exemple.com','root')
        # self.user3 = User.objects.create_user('root3','email2@exemple.com','root')

        self.need1 = Need.objects.create(
            name='mind', description='a need we have', user=self.user1)
        self.need2 = Need.objects.create(
            name='body', description='a need we have', user=self.user1)
        self.need3 = Need.objects.create(
            name='financial', description='a need we have', user=self.user1)

        Goal.objects.create(name="teste", need=self.need1)
        Goal.objects.create(name="goal2", need=self.need1)
        Goal.objects.create(name="goal3", need=self.need2)

    def test_goal_create(self):
        count = Goal.objects.all().count()
        self.assertEqual(count, 3)
        date = datetime.date.today()
        Goal.objects.create(
            name="teste2", description='description teste', endDate=date, need=self.need3)
        goal = Goal.objects.get(name='teste2')
        count = Goal.objects.all().count()
        self.assertEqual(count, 4)
        self.assertEqual(goal.name, 'teste2')
        self.assertEqual(goal.description, 'description teste')
        self.assertEqual(goal.endDate, date)

    def test_goal_create_with_50_char_length_name(self):
        count = Goal.objects.all().count()
        self.assertEqual(count, 3)
        date = datetime.date.today()
        Goal.objects.create(
            name="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", description='description teste', endDate=date, need=self.need3)
        goal = Goal.objects.get(id=4)
        count = Goal.objects.all().count()
        self.assertEqual(count, 4)
        self.assertEqual(goal.name, 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        self.assertEqual(goal.description, 'description teste')
        self.assertEqual(goal.endDate, date)

    def test_goal_update(self):
        goal = Goal.objects.get(name='goal3')
        goal.name = 'goal3Edited'
        goal.description = 'a edited need we have'
        goal.save()
        editedGoal = Goal.objects.get(name='goal3Edited')
        self.assertEqual(editedGoal.description, 'a edited need we have')

    def test_goal_delete(self):
        goal = Goal.objects.get(name='goal3')
        self.assertEqual(Goal.objects.all().count(), 3)
        goal.delete()
        self.assertEqual(Goal.objects.all().count(), 2)


class IterationModelTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            'root1', 'email2@exemple.com', 'root')
        # self.user2 = User.objects.create_user('root2','email2@exemple.com','root')
        # self.user3 = User.objects.create_user('root3','email2@exemple.com','root')

        self.need1 = Need.objects.create(
            name='mind', description='a need we have', user=self.user1)
        self.need2 = Need.objects.create(
            name='body', description='a need we have', user=self.user1)
        self.need3 = Need.objects.create(
            name='financial', description='a need we have', user=self.user1)

        self.goal1 = Goal.objects.create(name="teste", need=self.need1)
        self.goal2 = Goal.objects.create(name="goal2", need=self.need1)
        self.goal3 = Goal.objects.create(name="goal3", need=self.need2)

        self.iteration1 = Iteration.objects.create(number=1, completed=False,
                                                   date=datetime.date.today(), owner=self.user1)

    def test_Iteration_creation(self):
        count = Iteration.objects.all().count()
        self.assertEqual(count, 1)
        Iteration.objects.create(number=2, completed=False,
                                 date=datetime.date.today(), owner=self.user1)
        count = Iteration.objects.all().count()
        self.assertEqual(count, 2)

    def test_iteration_date(self):
        iteration = Iteration.objects.get(id=self.iteration1.id)
        today = datetime.date.today()
        self.assertEqual(iteration.date, today)


class DelivelyModelTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            'root1', 'email2@exemple.com', 'root')
        # self.user2 = User.objects.create_user('root2','email2@exemple.com','root')
        # self.user3 = User.objects.create_user('root3','email2@exemple.com','root')

        self.need1 = Need.objects.create(
            name='mind', description='a need we have', user=self.user1)
        self.need2 = Need.objects.create(
            name='body', description='a need we have', user=self.user1)
        self.need3 = Need.objects.create(
            name='financial', description='a need we have', user=self.user1)

        self.goal1 = Goal.objects.create(name="teste", need=self.need1)
        self.goal2 = Goal.objects.create(name="goal2", need=self.need1)
        self.goal3 = Goal.objects.create(name="goal3", need=self.need2)

        self.iteration1 = Iteration.objects.create(number=1, completed=False,
                                                   date=datetime.date.today(), owner=self.user1)

        self.step1 = Step.objects.create(name='first step', description='I like it',
                                         completed=False, goal=self.goal1)
        self.step2 = Step.objects.create(name='second step', description='I kind of like it',
                                         completed=False, goal=self.goal1)
        self.step3 = Step.objects.create(name='third step', description='I dont know if I like it',
                                         completed=False, goal=self.goal1)

        self.delivery1 = Delivery.objects.create(name='delivery1', description='delivery1',
                                                 step=self.step1, iteration=self.iteration1, completed=False)
        self.delivery2 = Delivery.objects.create(name='delivery2', description='delivery2',
                                                 step=self.step1, iteration=self.iteration1, completed=False)
        self.delivery3 = Delivery.objects.create(name='delivery3', description='delivery1',
                                                 step=self.step2, iteration=self.iteration1, completed=False)

    def test_delivery_creation(self):
        count = Delivery.objects.all().count()
        self.assertEqual(count, 3)
        delivery4 = Delivery.objects.create(name='delivery4', description='delivery4',
                                            step=self.step1, iteration=self.iteration1, completed=False)
        count = Delivery.objects.all().count()
        self.assertEqual(count, 4)

    def test_delivery_creation_without_iteration(self):
        count = Delivery.objects.all().count()
        self.assertEqual(count, 3)
        delivery4 = Delivery.objects.create(name='delivery4', description='delivery4',
                                            step=self.step1, completed=False)
        count = Delivery.objects.all().count()
        self.assertEqual(count, 4)


class IconTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            'root1', 'email2@exemple.com', 'root')
        # self.user2 = User.objects.create_user('root2','email2@exemple.com','root')
        # self.user3 = User.objects.create_user('root3','email2@exemple.com','root')

        self.need1 = Need.objects.create(
            name='mind', description='a need we have', user=self.user1)
        self.need2 = Need.objects.create(
            name='body', description='a need we have', user=self.user1)
        self.need3 = Need.objects.create(
            name='financial', description='a need we have', user=self.user1)

    def test_needs_created(self):
        count = Need.objects.all().count()
        self.assertEquals(count, 3)

    def test_create_need_with_icon(self):
        count = Need.objects.all().count()
        self.assertEquals(count, 3)

        need4 = Need.objects.create(
            name='financial', description='a need we have', user=self.user1, iconName="far fa-heart", iconColor="bg-red-500")

        count = Need.objects.all().count()
        self.assertEquals(count, 4)

        self.assertEquals(need4.iconName, "far fa-heart")
        self.assertEquals(need4.iconColor, "bg-red-500")

    def test_set_need_icon(self):
        self.assertEquals(self.need1.iconName, None)
        self.assertEquals(self.need1.iconColor, None)

        self.need1.iconName = "far fa-heart"
        self.need1.icon_color = "bg-red-500"

        self.assertEquals(self.need1.iconName, "far fa-heart")
        self.assertEquals(self.need1.icon_color, "bg-red-500")
