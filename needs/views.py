from django.shortcuts import render
from .models import Need, Goal, Step, Iteration, Delivery
from .serializers import NeedSerializer, StepSerializer, IterationSerializer, DeliverySerializer, GoalGetSerializer, GoalPostPutSerializer
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from datetime import date, timedelta
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
        iteration = Iteration.objects.filter(
            owner=request.user).get(completed=False)
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
                name='Health', description='need1 description', user=request.user, iconName="far fa-heart", iconColor="bg-red-500")
            Need.objects.create(
                name='Finance', description='need2 description', user=request.user, iconName="far fa-chart-bar", iconColor="bg-red-500")
            Need.objects.create(
                name='Professional', description='need3 description', user=request.user, iconName="fas fa-user-tie", iconColor="bg-red-500")
            Need.objects.create(
                name='Mind', description='need4 description', user=request.user, iconName="fas fa-code-branch", iconColor="bg-red-500")
            Need.objects.create(
                name='Others', description='need5 description', user=request.user, iconName="far fa-handshake", iconColor="bg-red-500")

            dateToBeUsed = date.today() + timedelta(days=5)
            Iteration.objects.create(
                number=0, completed=False, date=dateToBeUsed, owner=request.user)

            return Response(status=200)
        return Response(status=404)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def tutorial_setup_view(request, format=None):
    if request.method == 'POST':
        iteration = Iteration.objects.get(owner=request.user)
        need = Need.objects.filter(name='Others').get(user=request.user)
        goal = Goal.objects.create(
            name='tutorial', description="tutorial", endDate=None, need=need)

        step1 = Step.objects.create(
            name="Learn To Check", description="d", goal=goal, completed=False)
        step2 = Step.objects.create(
            name="Learn About The Goals", description="d", goal=goal, completed=False)
        step3 = Step.objects.create(
            name="Learn About The Steps", description="d", goal=goal, completed=False)
        step4 = Step.objects.create(
            name="Learn About The Iterations", description="d", goal=goal, completed=False)

        deliveries = []

        deliveries.append(Delivery(name="Welcome to IginApp", description="Be welcome, we'll try our best",
                          step=step1, iteration=iteration, completed=False))
        deliveries.append(Delivery(name="Mark a task as completed by checking the side box!", description="You can mark a task as completed by checking the side box!",
                          step=step1, iteration=iteration, completed=False))
        deliveries.append(Delivery(name="Check us when you complete the task", description="Check us when you complete the task",
                          step=step1, iteration=iteration, completed=False))

        deliveries.append(Delivery(name="Our Needs are Health, Mind,Financial,Professional and Others", description="that's right",
                          step=step2, iteration=iteration, completed=False))
        deliveries.append(Delivery(name="The App is based on Goals and Needs", description="The App is based on Goals and Needs",
                          step=step2, iteration=iteration, completed=False))
        deliveries.append(Delivery(name="Click the tutorial Goal on the side Goal box!", description="Click the tutorial Goal on the side Goal box!",
                          step=step2, iteration=iteration, completed=False))
        deliveries.append(Delivery(name="We need to complete some steps to complete the goal!", description="We need to complete some steps to complete the goal",
                          step=step2, iteration=iteration, completed=False))
        deliveries.append(Delivery(name="The second Step is Ok with this task!", description="Done",
                          step=step2, iteration=iteration, completed=False))

        deliveries.append(Delivery(name="Click the learn step step", description="Click the learn step step",
                          step=step3, iteration=iteration, completed=False))
        deliveries.append(Delivery(name="Each Step is composed of tasks!", description="Each Step is composed of tasks!",
                          step=step3, iteration=iteration, completed=False))
        deliveries.append(Delivery(name="To add a new task on a step click the 'add new' button", description="Hope you are doing good",
                          step=step3, iteration=iteration, completed=False))
        deliveries.append(Delivery(name="To define a task to be done click 'Add' on the side", description="Right now the task is going to show up in the to-do box",
                          step=step3, iteration=None, completed=False))
        deliveries.append(Delivery(name="You can remove a task from your todo list by clicking remove", description="You can remove a task from your to-do list by clicking 'remove'",
                          step=step3, iteration=None, completed=False))
        deliveries.append(Delivery(name="You can click the task name to edit!", description="You can click the task name to edit!",
                          step=step3, iteration=None, completed=False))

        Delivery.objects.bulk_create(deliveries)

        return Response(status=200)
    return Response(status=404)
