from rest_framework import serializers
from .models import Need, Goal, Step, Iteration


class NeedSerializer(serializers.ModelSerializer):

	class Meta:
		model = Need
		fields = ['id', 'name', 'description']

class GoalSerializer(serializers.ModelSerializer):

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
		fields = ['id', 'number', 'completed', 'date', 'goal']