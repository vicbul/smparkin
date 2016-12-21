from __future__ import unicode_literals

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from polymorphic_tree.models import PolymorphicMPTTModel, PolymorphicTreeForeignKey
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.http import Http404
from django.utils import timezone
import datetime, copy


# Create your models here.

class test(PolymorphicMPTTModel):
    # type = models.IntegerField(default=0, choices=resource_types())
    name = models.CharField(max_length=50, unique=True)
    parent = PolymorphicTreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    def __str__(self):
        return self.name

class test1(test):
    tes1_to_parent = models.OneToOneField(test, parent_link=True)
    test1_field = models.CharField(max_length=10, default='default test 1')

class test2(test):
    tes2_to_parent = models.OneToOneField(test, parent_link=True)
    test2_field = models.CharField(max_length=10, default='default test 2')


class Resource(PolymorphicMPTTModel):
    # Resource resource attributes present in TS-0004 TS-0004 Service Layer Core Protocol standard
    parent = PolymorphicTreeForeignKey('self', null=True, blank=True, related_name='children')
    resourceID = models.CharField(max_length=200, blank=True)
    name = models.CharField(max_length=200, blank=False, unique=True)
    # parentID = models.CharField(max_length=200, blank=True)
    accessControlPolicyIDs = models.CharField(max_length=200, blank=True)
    creationTime = models.DateTimeField(blank=True, null=True)
    lastModifiedTime = models.DateTimeField(blank=True, null=True)
    expirationTime = models.DateTimeField(default=datetime.datetime.strptime('20991116T000000', "%Y%m%dT%H%M%S" ))
    labels = models.CharField(max_length=200, blank=True)
    announceTo = models.CharField(max_length=200, blank=True)
    announcedAttribute = models.CharField(max_length=200, blank=True)

    # Below attributes are present on TS-0004 Service Layer Core Protocol standard but not on IoTdm documentation
    dynamicAuthorizationConsultationIDs = models.CharField(max_length=200, blank=True)

    check_iotdm_response = False
    iotdm_response = None

    # This function will raise a ValidationError in case check_iotdm_response is true and the iotdm server replies with
    # an error.
    def clean(self):
        print self.iotdm_response
        if self.iotdm_response is not None and self.iotdm_response.find('error') != -1 and self.check_iotdm_response == True:
            print 'setting error to True.'
            raise ValidationError('Request to IoTdm server failed for '+self.name+':  '+self.iotdm_response)

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']

class CSE(Resource):
    #cseType = models.CharField(max_length=200, blank=True)
    resourceType = models.IntegerField(default=5, blank=False)
    CSE_ID = models.CharField(max_length=200, blank=False, default='InCSE1')
    CSE_Type = models.CharField(max_length=200, blank=False, default='IN-CSE')
    supportedResourceType = models.CharField(max_length=200, blank=True)
    pointOfAccess = models.CharField(max_length=200, blank=True)
    nodeLink = models.CharField(max_length=200, blank=True)

    # Below attributes are present on TS-0004 Service Layer Core Protocol standard but not on IoTdm documentation
    e2eSecInfo = models.CharField(max_length=200, blank=True)

    # Below attributes are present on IoTdm documentation but not on TS-0004 Service Layer Core Protocol standard
    notificationCongestionPolicy = models.CharField(max_length=200, blank=True)


class APP(Resource):
    resourceType = models.IntegerField(default=2, blank=False)
    # parent_resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='Parent Resource', default=1)
    appName = models.CharField(max_length=200, blank=True)
    App_ID = models.CharField(max_length=200, blank=True)
    AE_ID = models.CharField(max_length=200, blank=True)
    pointOfAccess = models.CharField(max_length=200, blank=True)
    #ontologyRef = models.CharField(max_length=200, blank=True)
    nodeLink = models.CharField(max_length=200, blank=True)
    contentSerialization = models.CharField(max_length=200, blank=True)

    # Below attributes are present on TS-0004 Service Layer Core Protocol standard but not on IoTdm documentation
    requestReachability = models.BooleanField(default=True)
    #e2eSecInfo = models.CharField(max_length=200, blank=True)


class CONTAINER(Resource):
    resourceType = models.IntegerField(default=3, blank=False)
    # parent_resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='Parent Resource', default=1)


class CONTENTINSTANCE(Resource):
    resourceType = models.IntegerField(default=4, blank=False)
    content = models.CharField(max_length=1000, blank=False)


class SUBSCRIPTION(Resource):
    resourceType = models.IntegerField(default=23, blank=False)
    notificationURI = models.CharField(max_length=2000, blank=False, default="http://localhost:8586")
    notificationContentType = models.IntegerField(default=1)
    eventNotificationCriteria = models.CharField(max_length=100, default='{"net":[6]')



