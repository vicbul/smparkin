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


class ResourcesView(viewsets.ReadOnlyModelViewSet):

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

    @detail_route(url_path = 'descendants')
    def get_descendants(self, request, pk=None):
        """
        Lists all the descendants with an 'rx' container hanging from the given resource id.
        """
        resource = self.get_object()
        descendants = resource.get_descendants().filter(children__name='rx').order_by('children__children__creationTime')
        serializer = self.get_serializer(descendants, many=True)
        return  Response(serializer.data)



