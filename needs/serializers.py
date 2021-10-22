from rest_framework import serializers
from .models import Need, Goal, Step, Iteration, Delivery


class NeedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Need
        fields = ['id', 'name', 'description', 'iconName', 'iconColor']


class GoalGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id', 'name', 'description', 'endDate', 'need']
        depth = 1

class GoalPostPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id', 'name', 'description', 'endDate', 'need']


class StepSerializer(serializers.ModelSerializer):

    percentageCompleted = serializers.SerializerMethodField('get_percentage_completed')
    class Meta:
        model = Step
        fields = ['id', 'name', 'description', 'completed', 'goal','percentageCompleted']

    def get_percentage_completed(self, obj):
        count = Delivery.objects.filter(step = obj.id)
        count_completed = count.filter(completed=True)
        if(count.count() == 0):
            return "0%"
        percentage = count_completed.count() /count.count() * 100
        return str(percentage)+ "%"


class IterationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Iteration
        fields = ['id', 'number', 'completed', 'date']


class DeliverySerializer(serializers.ModelSerializer):

    class Meta:
        model = Delivery
        fields = ['id', 'name', 'description',
                  'step', 'iteration', 'completed']
