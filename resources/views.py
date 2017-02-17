from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from models import *
from serializers import ResourceSerializer, StatusSerializer

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

class Status(APIView):

    def get(self, request):
        resources = CONTENTINSTANCE.objects.all().order_by('creationTime')
        # Filtering only the last content instances
        parents = []
        last_content = []
        for r in resources:
            if r.parent not in parents:
                parents.append(r.parent)
                last_content.append(r)
            else:
                continue

        serializer = StatusSerializer(last_content, many=True)
        return Response(serializer.data)

    def post(self):
        pass

# View to display get or post data
# class MyView(View):
#     def get(self, request, *args, **kwargs):
#         return HttpResponse('This is GET request')
#
#     def post(self, request, *args, **kwargs):
#         return HttpResponse('This is POST request')



