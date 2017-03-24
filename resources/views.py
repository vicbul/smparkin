from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from models import *
from serializers import *
from django.db.models import Max, F
import rx_simulator
import time

# Create your views here.

def subscription(request):
    #print 'request', request
    return render(request, 'resources/subscriptions.html')

def simulator(request):
    try:
        rx_simulator.run()
        return HttpResponse('<h1>Simulated data sent.</h1>')
    except Exception as e:
        raise Http404("Some nasty error happened while running the simulator. It's all your fault!")




# List all Resources in the tree (common attributes)

class TestView(APIView):

    def get(self, request):
        resources = test1.objects.all()
        serializer = Test1Serializer(resources, many=True)
        return Response(serializer.data)

    def post(self):
        pass

# resource_tree/
class ResouceTree(APIView):

    def get(self, request):
        resources = Resource.objects.all()
        serializer = ResourceSerializer(resources, many=True)
        return Response(serializer.data)

    def post(self):
        pass

class AppView(APIView):

    def get(self, request, format=None):
        print 'GET request received:', #request.data
        resources = APP.objects.all()
        serializer = AppSerializer(resources, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print 'POST request received:', request.data['resourceID']
        # If there is no resourceID create it, else update it
        if not APP.objects.filter(resourceID = request.data['resourceID']):
            serializer = AppSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            existing_app = APP.objects.get(resourceID=request.data['resourceID'])
            print 'Updating',existing_app
            serializer = AppSerializer(existing_app, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # return Response(status=status.HTTP_409_CONFLICT)


class ContainerView(APIView):

    def get(self, request, format=None):
        print 'GET request received:', #request.data
        if request.GET.get('type', ''):
            if request.GET['type']=='rx':
                resources = CONTAINER.objects.filter(name='rx')
        else:
            resources = CONTAINER.objects.all()
        serializer = ContainerSerializer(resources, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print 'POST request received:', #request.data
        # If there is no resourceID create it, else update it
        if not CONTAINER.objects.filter(resourceID = request.data['resourceID']):
            # print Resource.objects.get(resourceID = request.data['parent'])
            request.data['parent'] = Resource.objects.get(resourceID = request.data['parent']).id
            serializer = ContainerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # Updating the node may not be a good idea if we want to keep the edited name of the node
        else:
            existing_cnt = CONTAINER.objects.get(resourceID=request.data['resourceID'])
            print 'Updating',existing_cnt
            serializer = AppSerializer(existing_cnt, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # return Response(status=status.HTTP_409_CONFLICT)

class CinView(APIView):

    def get(self, request, format=None):
        print 'GET request received:', request.GET #request.data
        if request.GET.get('instances', ''):
            start = time.time()
            cnt_rx = CONTAINER.objects.filter(name='rx')
            resources = []
            for rx in cnt_rx:
                cin = CONTENTINSTANCE.objects.filter(parent=rx).order_by('-creationTime')[0]
                print 'cin', cin.creationTime
                resources.append(cin)
            end = time.time()
            print 'cin Query lasted',end-start, 'seconds'
            print 'cnt_rx', cnt_rx
            # resources = CONTENTINSTANCE.objects.order_by('parent','-creationTime')
            print 'resources max', resources
        else:
            resources = CONTENTINSTANCE.objects.all()
        serializer = CinGetSerializer(resources, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print 'POST request received:', #request.data
        # print Resource.objects.get(resourceID = request.data['parent'])
        request.data['parent'] = Resource.objects.get(resourceID = request.data['parent']).id
        print 'request data', request.data
        serializer = CinPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoraTxView(APIView):

    def get(self, request, format=None):
        print 'GET request received:', request.GET #request.data
        if request.GET.get('instances', ''):
            start = time.time()
            cnt_tx = CONTAINER.objects.filter(name='tx')
            resources = []
            for tx in cnt_tx:
                cin = LoraTx.objects.filter(parent=tx).order_by('-creationTime')[0]
                print 'cin', cin.creationTime
                resources.append(cin)
            end = time.time()
            print 'cin Query lasted',end-start, 'seconds'
            print 'cnt_rx', cnt_tx
            # resources = CONTENTINSTANCE.objects.order_by('parent','-creationTime')
            print 'resources max', resources
        else:
            resources = LoraTx.objects.all()
        serializer = LoraTxGetSerializer(resources, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print 'POST request received:', #request.data
        # print Resource.objects.get(resourceID = request.data['parent'])
        request.data['parent'] = Resource.objects.get(resourceID = request.data['parent']).id
        print 'request data', request.data
        serializer = LoraTxPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

class AppDataView(APIView):

    def get(self, request, format=None):
        print 'GET request received:', #request.data
        resources = AppData.objects.all()
        serializer = AppDataSerializer(resources, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print 'POST request received:', #request.data
        serializer = AppDataSerializer(data=request.data)
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



