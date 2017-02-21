from django.conf.urls import url
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404
from resources.models import *
from rest_framework.urlpatterns import format_suffix_patterns
from SmartParking import settings
from resources.signals.handlers import parse_date

if settings.CHECK_IOTDM_RESPONSE is True:
    from iotdm import iotdm_api

from references import shortToLongDict

from resources import views

# This function selects the model to create based on IoTdm response
iotdm_to_model = {
    'm2m:cse': CSE,
    'm2m:ae': APP,
    'm2m:cnt': CONTAINER,
    'm2m:cin': CONTENTINSTANCE,
    'm2m:sub': SUBSCRIPTION
}

# iotdm_django_sync function is called when 'django_subscription' sends a HTTP notification to django
# Using subscription nct = 3 (send only target resource URI)
# csrf_exempt decorator is used to avoid the need for a csrf cookie

#TODO find a way to disable signals for incoming subscriptions
@csrf_exempt
def iotdm_django_sync(response):
    print 'Test function response', response.body
    # TODO for IoTdm connection try django.utils.six.BytesIO and rest_framework.parsers import JSONParser
    response_dict = eval(response.body)
    resource_uri = response_dict['nev']['rep']['rn']
    path_split = resource_uri.rsplit('/',1)
    parent_uri, name = path_split[0], path_split[1]
    parent = parent_uri.rsplit('/',1)[1]
    # Convertion JSON in text format into python dict
    retrieve_iotdm_resource_raw = iotdm_api.retrieve(settings.IOTDM_SERVER+resource_uri[1:])
    # In some cases IoTdm is using true or false as values which eval() does not recognize. It needs to be replaced.
    retrieve_iotdm_resource = eval(retrieve_iotdm_resource_raw.replace(':true,',':True,').replace(':false,', ':False,'))
    print retrieve_iotdm_resource
    # Getting just resource parameters dictionary
    parameters = retrieve_iotdm_resource[retrieve_iotdm_resource.keys()[0]]
    print 'parameters', parameters
    if retrieve_iotdm_resource.keys()[0] is 'error':
        return HttpResponse('Resource not found on IoTdm')
    # Get all django resources with the IoTdm resource name
    resource_model = iotdm_to_model[retrieve_iotdm_resource.keys()[0]]
    django_resources = resource_model.objects.filter(name = name)
    django_resource = None
    # Check if any of the instances returned has the same URI as the IoTdm resource
    for instance in django_resources:
        parent_uri = '/'+'/'.join([ancestor.name for ancestor in instance.get_ancestors(include_self = True)])
        print instance, 'parent URI', parent_uri
        if parent_uri == resource_uri:
            django_resource = instance
            break

    # trying to get resourceID, otherwise resource do not exists and needs to be removed from Django
    if retrieve_iotdm_resource.get('error') is None:

        # UPDATE
        if django_resource is not None:
            # If there is a existing resource in django we need to get it as a queryset in order to be able to update
            django_resource_queryset = resource_model.objects.filter(resourceID = django_resource.resourceID)
            resource_fields = [f.name for f in django_resource._meta.get_fields()]
            # Creating a dictionary with all parameters:values to update the queryset. Including 'name' instead of 'resourceName'
            d = {'name':parameters['rn']}
            for f in parameters:
                if shortToLongDict[f] not in resource_fields:
                    continue
                # Fields are being updated one by one creating a dictionary "d" for each paramenter:value
                try:
                    # Try to parse date, in case it fails is not a date
                    date_field = parse_date(parameters[f])
                    d[shortToLongDict[f]] = date_field
                except Exception, e:
                    print 'Is not a date', e
                    d[shortToLongDict[f]] = parameters[f]

            django_resource_queryset.update(**d)

        # CREATE
        else:
            # If there is no such resource on django green light to create it
            print 'Resource does not exists on IoTdm. Creating resource.'
            # Getting parent_instance by resourceID using new resource parentID parameter. Otherwise return
            try:
                parent_instance = Resource.objects.get(resourceID = parameters['pi'].rsplit('/',1)[1])#name=parent_uri.rsplit('/',1)[1])#.filter(parent=parent[1:])
                print 'parent instance', parent_instance
            except Exception, e:
                print 'Error:', e
                return HttpResponse('')

            django_resource = resource_model(name=name, parent=parent_instance)
            for f in parameters:
                print shortToLongDict[f], parameters[f]
                try:
                    # try to format the parameter into django date format. In case it fails it is not a date
                    try:
                        date_field = parse_date(parameters[f])
                        parameter = setattr(django_resource, shortToLongDict[f], date_field)
                    except Exception, e:
                        print 'Is not a date', e
                        parameter = setattr(django_resource, shortToLongDict[f], parameters[f])
                except Exception, e:
                    print e,':', parameters[f], 'is not present on Django model.'
                    continue

            django_resource.save()
    # DELETE
    else:
        # If we cannot extract a "ri" parameter from the IoTdm response is because the resource could not be found
        print 'The resource does not exists on IoTdm.'
        print 'Checkin if there is a django resource', parent, name
        try:

            # If there is a match, delete it
            if django_resource != None:
                django_resource.delete()
            else:
                print 'The resource is neither on IoTdm nor in Django.'

        except Exception, e:
            print e
            print 'The resource is neither on IoTdm nor in Django.'

    return HttpResponse('')


urlpatterns = [
    # url(r'^$', views.subscription, name='subs'),
    url(r'^structure', TemplateView.as_view(template_name='resources/home.html'), name='home'),
    url(r'^iotdm', iotdm_django_sync),#views.MyView.as_view(), name='my-view')
    url(r'^full_resource_tree', views.ResouceTree.as_view()),
    # url(r'^status', views.Status.as_view()),
    url(r'^mqttsub', views.MQTTSubscription.as_view())
]