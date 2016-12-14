from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.http import Http404
from django.utils import timezone
import datetime, copy



def crudn_choices():
    # CRUDN (create, Retrieve, Update, Delete, Notify) operation to be performed
    create = 'create'
    retrieve = 'retrieve'
    update = 'update'
    delete = 'delete'
    notify = 'notify'
    crudn = (
        (create, 'create'),
        (retrieve, 'retrieve'),
        (update, 'update'),
        (delete, 'delete'),
        (notify, 'notify'),
    )
    return crudn

# Create your models here.

class test(models.Model):
    test2 = models.ForeignKey('APP', on_delete=models.CASCADE)
    test3 = models.ForeignKey('self')

class Common(models.Model):
    # Common resource attributes present in TS-0004 TS-0004 Service Layer Core Protocol standard
    resourceID = models.CharField(max_length=200, blank=True)
    resourceName = models.CharField(max_length=200, blank=False)
    parentID = models.CharField(max_length=200, blank=False)
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


    def __init__(self, *args, **kwargs):
        super(Common, self).__init__(*args, **kwargs)
        self.previous_resourceName = copy.deepcopy(self.resourceName)
        self.previous_parentID = copy.deepcopy(self.parentID)

    # This function will raise a ValidationError in case check_iotdm_response is true and the iotdm server replies with
    # an error.
    def clean(self):
        print self.iotdm_response
        if self.iotdm_response is not None and self.iotdm_response.find('error') != -1 and self.check_iotdm_response == True:
            print 'setting error to True.'
            raise ValidationError('Request to IoTdm server failed for '+self.resourceName+':  '+self.iotdm_response)

    def __str__(self):
        return self.resourceName

    class Meta:
        # This attibute put common and child model's attributes together in the same MySQL table
        abstract = True



class CSE(Common):
    #cseType = models.CharField(max_length=200, blank=True)
    resourceType = 5
    CSE_ID = models.CharField(max_length=200, blank=False, default='InCSE1')
    CSE_Type = models.CharField(max_length=200, blank=False, default='IN-CSE')
    supportedResourceType = models.CharField(max_length=200, blank=True)
    pointOfAccess = models.CharField(max_length=200, blank=True)
    nodeLink = models.CharField(max_length=200, blank=True)

    # Below attributes are present on TS-0004 Service Layer Core Protocol standard but not on IoTdm documentation
    e2eSecInfo = models.CharField(max_length=200, blank=True)

    # Below attributes are present on IoTdm documentation but not on TS-0004 Service Layer Core Protocol standard
    notificationCongestionPolicy = models.CharField(max_length=200, blank=True)


class APP(Common):
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # content_object = GenericForeignKey('content_type', 'object_id')
    resourceType = 2
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



class CONTAINER(Common):
    resourceType = 3


class CONTENTINSTANCE(Common):
    resourceType = 4
    content = models.CharField(max_length=1000, blank=False)


class SUBSCRIPTION(Common):
    resourceType = 23
    notificationURI = models.CharField(max_length=2000, blank=False, default="http://localhost:8586")
    notificationContentType = models.IntegerField(default=1)
    eventNotificationCriteria = models.CharField(max_length=100, default='{"net":[6], "om":[6]}')


