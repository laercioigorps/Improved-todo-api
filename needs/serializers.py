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

    class Meta:
        model = Step
        fields = ['id', 'name', 'description', 'completed', 'goal']


class IterationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Iteration
        fields = ['id', 'number', 'completed', 'date']


class DeliverySerializer(serializers.ModelSerializer):

    class Meta:
        model = Delivery
        fields = ['id', 'name', 'description',
                  'step', 'iteration', 'completed']
