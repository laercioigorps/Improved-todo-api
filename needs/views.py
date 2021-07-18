from django.shortcuts import render
from .models import Need, Goal, Step, Iteration, Delivery
from .serializers import NeedSerializer, GoalSerializer, StepSerializer, IterationSerializer, DeliverySerializer
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


@api_view(['GET', 'POST'])
def need_list_view(request, format=None):

	if request.method == 'GET':
		needs = Need.objects.all()
		serializer = NeedSerializer(needs, many=True) 
		return Response(serializer.data)
	if request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = NeedSerializer(data=data)
		if(serializer.is_valid()):
			serializer.save(user=request.user)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def need_detail_view(request, pk):
	try:
		need = Need.objects.get(pk=pk)
	except Need.DoesNotExist:
		return HttpResponse(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = NeedSerializer(need)
		return Response(serializer.data)

	if request.method == 'PUT': #study
		data = JSONParser().parse(request)
		serializer = NeedSerializer(need, data = data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	if request.method == 'DELETE':
		need.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def goal_list_view(request):

	if request.method == 'GET':
		needs = Need.objects.all()
		serializer = NeedSerializer(needs, many= True)
		return Response(serializer.data)

	if request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = GoalSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def goal_detail_view(request, pk):
	try:
		goal = Goal.objects.get(pk=pk)
	except Goal.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = GoalSerializer(goal)
		return Response(serializer.data)
	if request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = GoalSerializer(goal, data=data)
		if(serializer.is_valid()):
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	if request.method == 'DELETE':
		goal.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def step_list_view(request):
	if request.method == 'GET':
		steps = Step.objects.all()
		serializer = StepSerializer(steps, many=True)
		return Response(serializer.data)

	if request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = StepSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT', 'DELETE'])
def step_detail_view(request, pk, format=None):
	try:
		step = Step.objects.get(pk=pk)
	except Step.DoesNotExist:
		return HttpResponse(status=status.HTTP_404_NOT_FOUND)
	if request.method == 'GET':
		serializer = StepSerializer(step)
		return Response(serializer.data)
	if request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = StepSerializer(step, data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	if request.method == 'DELETE':
		step.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def iteration_list_view(request, format=None):
	if request.method == 'GET':
		iterations = Iteration.objects.all()
		serializer = IterationSerializer(iterations, many=True)
		return Response(serializer.data)
	if request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = IterationSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(response.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def iteration_detail_view(request, pk, format=None):
	try:
		iteration = Iteration.objects.get(pk=pk)
	except Iteration.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = IterationSerializer(iteration)
		return Response(serializer.data)
	if request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = IterationSerializer(iteration, data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	if request.method == 'DELETE':
		iteration.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def delivery_list_view(request, format=None):
	if request.method == 'GET':
		deliveries = Delivery.objects.all()
		serializer = DeliverySerializer(deliveries, many=True)
		return Response(serializer.data)
	if request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = DeliverySerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def delivery_detail_view(request, pk, format=None):
	try:
		delivery = Delivery.objects.get(pk=pk)
	except Delivery.DoesNotExist:
		return Response(status=404)

	if request.method == 'GET':
		serializer = DeliverySerializer(delivery)
		return Response(serializer.data)
	if request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = DeliverySerializer(delivery, data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	if request.method == 'DELETE':
		delivery.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


