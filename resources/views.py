from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as drfilters
import django_filters
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


class fromfilter(drfilters.FilterSet):
    test = django_filters.DateFilter


# API views
class TestView(APIView):

    def get(self, request):
        resources = test1.objects.all()
        serializer = Test1Serializer(resources, many=True)
        return Response(serializer.data)

    def post(self):
        pass


# resource_tree/
class GetSensors(APIView):

    """
    get:

    Returns a list of all the sensors and their last rx and tx content/state.

    - Use parameter "?from={id}" to get all sensors hanging from a particular resource.

    post:
    Not Implemented.
    """

    def get(self, request):
        # Return all nodes hanging from the parent provided by the parameter 'from'
        if request.GET.get('from',''):
            parent_id = request.GET['from']
            resource_root = CONTAINER.objects.get(id=parent_id)
            resources = resource_root.get_descendants().filter(children__name = 'rx')
        # Return the whole tree
        else:
            resources = Resource.objects.filter(children__name = 'rx')

        serializer = ParentSerializer(resources, many=True)
        # serializer = ResourceSerializer(resources, many=True)
        # serializer = ContentSerializer(cins, many=True)
        return Response(serializer.data)

    def post(self):
        pass


class ResourcesView(viewsets.ReadOnlyModelViewSet): #ReadOnlyModelViewSet

    """
    list:
    Returns a list of resources in JSON. Each object includes the given resource + all its children + content of each children.
    """

    queryset = Resource.objects.all()
    serializer_class = ParentSerializer
    filter_fields = ('name', 'children__name')
    filter_backends = (
                        filters.OrderingFilter,
                        DjangoFilterBackend,
                        # filters.SearchFilter,
                    )
    ordering_fields = ('creationTime',)
    # search_fields = ('name',)

    @detail_route(url_path = 'nodes')
    def get_descendants(self, request, pk=None):
        """
        Lists all the descendants with an 'rx' container hanging from the given resource id.
        """
        resource = self.get_object()
        descendants = resource.get_descendants().filter(children__name='rx').order_by('children__children__creationTime')
        # descendants = resource.get_descendants().filter(name = 'rx').order_by('children__creationTime')
        print 'Descendants', descendants
        serializer = NodeSerializer(descendants, many=True)#self.get_serializer(descendants, many=True)
        return  Response(serializer.data)

#----------  Creating resources when receiving POST notification from MQTT  -----------#

class AppView(APIView):

    def get(self, request, format=None):
        print 'GET request received:', #request.data
        resources = APP.objects.all()
        serializer = AppSerializer(resources, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print 'APP POST request received:', request.data.keys()#['applicationID']
        # If there is no resourceID create it, else update it
        if not APP.objects.filter(resourceID = request.data['resourceID']):
            print "Creating resource"
            serializer = AppSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            print "Updating resource"
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
        resources = CONTAINER.objects.all()
        serializer = ContainerSerializer(resources, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print 'Container POST request received:', request.data
        # If there is no resourceID create it, else update it
        if not CONTAINER.objects.filter(resourceID = request.data['resourceID']):
            print "Creating resource"
            print "Parent ID", Resource.objects.get(resourceID = request.data['parent']).id
            request.data['parent'] = Resource.objects.get(resourceID = request.data['parent']).id
            print "Data parent", request.data
            serializer = ContainerPostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # Updating the node may not be a good idea if we want to keep the edited name of the node
        else:
            print "Updating resource"
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
        print 'GET request received:', #request.data
        resources = CONTENTINSTANCE.objects.all()
        serializer = CinPostSerializer(resources, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print 'POST request received:', #request.data
        print Resource.objects.get(resourceID = request.data['parent'])
        request.data['parent'] = Resource.objects.get(resourceID = request.data['parent']).id
        serializer = CinPostSerializer(data=request.data)
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
