from django.shortcuts import render
from .models import Need, Goal, Step, Iteration, Delivery
from .serializers import NeedSerializer, StepSerializer, IterationSerializer, DeliverySerializer, GoalGetSerializer, GoalPostPutSerializer
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
# Create your views here.


@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def need_list_view(request, format=None):

    if request.method == 'GET':
        needs = Need.objects.filter(user=request.user)
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
@permission_classes([permissions.IsAuthenticated])
def need_detail_view(request, pk, format=None):
    try:
        need = Need.objects.get(pk=pk)
    except Need.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.user != need.user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = NeedSerializer(need)
        return Response(serializer.data)

    if request.method == 'PUT':  # study
        data = JSONParser().parse(request)
        serializer = NeedSerializer(need, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        need.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def goal_list_view(request, format=None):

    if request.method == 'GET':
        goals = Goal.objects.filter(need__user=request.user)
        serializer = GoalGetSerializer(goals, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = GoalPostPutSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def goal_list_by_need_view(request, need, format=None):

    if request.method == 'GET':
        goals = Goal.objects.filter(need__user=request.user).filter(need=need)
        serializer = GoalGetSerializer(goals, many=True)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def goal_detail_view(request, pk, format=None):
    try:
        goal = Goal.objects.get(pk=pk)
    except Goal.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if goal.need.user != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = GoalGetSerializer(goal)
        return Response(serializer.data)
    if request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = GoalPostPutSerializer(goal, data=data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        goal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def step_list_view(request, format=None):
    if request.method == 'GET':
        steps = Step.objects.filter(goal__need__user=request.user)
        serializer = StepSerializer(steps, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = StepSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def step_list_by_goal_view(request, goal,  format=None):
    if request.method == 'GET':
        steps = Step.objects.filter(
            goal__need__user=request.user).filter(goal=goal)
        serializer = StepSerializer(steps, many=True)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def step_detail_view(request, pk, format=None):
    try:
        step = Step.objects.get(pk=pk)
    except Step.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if step.goal.need.user != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)

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
@permission_classes([permissions.IsAuthenticated])
def iteration_list_view(request, format=None):
    if request.method == 'GET':
        iterations = Iteration.objects.filter(owner=request.user)
        serializer = IterationSerializer(iterations, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = IterationSerializer(data=data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(response.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def iteration_detail_view(request, pk, format=None):
    try:
        iteration = Iteration.objects.get(pk=pk)
    except Iteration.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if iteration.owner != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)
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


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def iteration_get_active_view(request, format=None):
    try:
        iteration = Iteration.objects.get(completed=False)
    except Iteration.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = IterationSerializer(iteration)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def delivery_list_view(request, format=None):
    if request.method == 'GET':
        deliveries = Delivery.objects.filter(
            step__goal__need__user=request.user)
        serializer = DeliverySerializer(deliveries, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = DeliverySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def delivery_list_by_step_view(request, step, format=None):
    if request.method == 'GET':
        deliveries = Delivery.objects.filter(
            step__goal__need__user=request.user).filter(step=step)
        serializer = DeliverySerializer(deliveries, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def delivery_list_by_goal_view(request, goal, format=None):
    if request.method == 'GET':
        deliveries = Delivery.objects.filter(
            step__goal__need__user=request.user).filter(step__goal=goal)
        serializer = DeliverySerializer(deliveries, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def delivery_list_by_iteration_view(request, iteration, format=None):
    if request.method == 'GET':
        deliveries = Delivery.objects.filter(
            step__goal__need__user=request.user).filter(iteration=iteration)
        serializer = DeliverySerializer(deliveries, many=True)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delivery_detail_view(request, pk, format=None):
    try:
        delivery = Delivery.objects.get(pk=pk)
    except Delivery.DoesNotExist:
        return Response(status=404)

    if delivery.step.goal.need.user != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)
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


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def wizard_view(request, format=None):
    if request.method == 'POST':
        needs = Need.objects.filter(user=request.user)
        if(needs.count() == 0):
            Need.objects.create(
                name='Health', description='need1 description', user=request.user)
            Need.objects.create(
                name='Finance', description='need2 description', user=request.user)
            Need.objects.create(
                name='Professional', description='need3 description', user=request.user)
            Need.objects.create(
                name='Mind', description='need4 description', user=request.user)
            Need.objects.create(
                name='Others', description='need5 description', user=request.user)

            return Response(status=200)
        return Response(status=404)
