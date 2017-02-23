from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from models import *
from serializers import *

# Create your views here.

def subscription(request):
    #print 'request', request
    return render(request, 'resources/subscriptions.html')

# List all Resources in the tree (common attributes)
# resource_tree/
class ResouceTree(APIView):

    def get(self, request):
        resources = Resource.objects.all()
        serializer = ResourceSerializer(resources, many=True)
        return Response(serializer.data)

    def post(self):
        pass

class GatewayStatsView(APIView):

    def get(self, request, format=None):
        print 'GET request received:', #request.data
        resources = GatewayStats.objects.all()
        serializer = GatewayStatsSerializer(resources, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print 'POST request received:', #request.data
        serializer = GatewayStatsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GatewayRxView(APIView):

    def get(self, request, format=None):
        print 'GET request received:', #request.data
        resources = GatewayRx.objects.all()
        serializer = GatewayRxSerializer(resources, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print 'POST request received:', #request.data
        serializer = GatewayRxSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class Status(APIView):
#
#     def get(self, request, format=None):
#         resources = CONTENTINSTANCE.objects.all().order_by('creationTime')
#         # Filtering only the last content instances
#         parents = []
#         last_content = []
#         for r in resources:
#             if r.parent not in parents:
#                 parents.append(r.parent)
#                 last_content.append(r)
#             else:
#                 continue
#
#         serializer = StatusSerializer(last_content, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         print 'request', request.data
#         serializer = StatusSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View to display get or post data
# class MyView(View):
#     def get(self, request, *args, **kwargs):
#         return HttpResponse('This is GET request')
#
#     def post(self, request, *args, **kwargs):
#         return HttpResponse('This is POST request')



