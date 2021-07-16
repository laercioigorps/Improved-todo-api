from django.shortcuts import render
from .models import Need
from .serializers import NeedSerializer, GoalSerializer
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser

# Create your views here.

def need_list_view(request):

	if request.method == 'GET':
		needs = Need.objects.all()
		serializer = NeedSerializer(needs, many=True) 
		return JsonResponse(serializer.data, safe=False)
	if request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = NeedSerializer(data=data)
		if(serializer.is_valid()):
			serializer.save(user=request.user)
			return JsonResponse(serializer.data, status=201)
		else:
			return JsonResponse(serializer.errors, status=400)

def need_detail_view(request, pk):
	try:
		need = Need.objects.get(pk=pk)
	except Need.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = NeedSerializer(need)
		return JsonResponse(serializer.data)

	if request.method == 'PUT': #study
		data = JSONParser().parse(request)
		serializer = NeedSerializer(need, data = data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data)
		return JsonResponse(serializer.errors, status=400)
	if request.method == 'DELETE':
		need.delete()
		return HttpResponse(status=204)


def goal_list_view(request):

	# if request.method == 'GET':
	# 	needs = Need.objects.all()
	# 	serializer = NeedSerializer(needs, many= True)
	# 	return JsonResponse(serializer.data, safe=False)

	if request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = GoalSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data)
		return JsonResponse(serializer.errors)


