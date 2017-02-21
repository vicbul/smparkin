from __future__ import unicode_literals

from django.db import models
from django.db.models import Model
from polymorphic_tree.models import PolymorphicMPTTModel, PolymorphicTreeForeignKey
from django.core.exceptions import ValidationError
from SmartParking import settings
import datetime, socket

if settings.CHECK_IOTDM_RESPONSE is True:
    from iotdm import iotdm_api

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
    # TODO add a new field resourceName to sync with IoTdm and keep django name as an modifiable alias
    name = models.CharField(max_length=200, blank=False)
    parentID = models.CharField(max_length=200, blank=True)
    # not supported for subscription/contentinstance in IoTdm BORON
    accessControlPolicyIDs = models.CharField(max_length=200, blank=True, default='[]') # Array expected for this value
    creationTime = models.DateTimeField(blank=True, null=True)
    lastModifiedTime = models.DateTimeField(blank=True, null=True)
    expirationTime = models.DateTimeField(default=datetime.datetime.strptime('20991116T000000', "%Y%m%dT%H%M%S" ))
    labels = models.CharField(max_length=200, blank=True, default='[]') # Array expected for this value
    announceTo = models.CharField(max_length=200, blank=True)
    announcedAttribute = models.CharField(max_length=200, blank=True)

    # Below attributes are present on TS-0004 Service Layer Core Protocol standard but not on IoTdm documentation
    dynamicAuthorizationConsultationIDs = models.CharField(max_length=200, blank=True)

    # To connect with IoTdm handlers need to be imported in resources.apps.ResourcesConfig.ready
    # check_iotdm_response = True
    iotdm_resource_name = None
    iotdm_response = None

    # This function will raise a ValidationError in case check_iotdm_response is true and the iotdm server replies with
    # an error.
    def clean(self):

        # print 'iotdm_response', self.iotdm_response
        # if self.iotdm_response is not None and self.iotdm_response.find('error') != -1 and self.check_iotdm_response == True:
        #     print 'setting error to True.'
        #     raise ValidationError('Request to IoTdm server failed for '+self.name+':  '+self.iotdm_response)

        if settings.CHECK_IOTDM_RESPONSE is True:
            iotdm_connect = socket.socket()
            # TODO Fix connection to IoTdm. Right now is not connecting even when IoTdm is online
            try:
                iotdm_connect.connect((settings.IOTDM_IP, int(settings.IOTDM_PORT)))
                print 'Connection to IoTdm successful.'

            except Exception, e:
                raise ValidationError('Cannot connect to IoTdm: '+str(e))

    # This method returns the polymorphic_ctype_id in string mode so it can be compared with ct_id param sent by filters in changelist
    def polymorphic_ctype_str_id(self):
        return str(self.polymorphic_ctype_id)

    def __str__(self):
        return self.name

    def meta(self):
        return self._meta

    class MPTTMeta:
        order_insertion_by = ['name']


class CSE(Resource):
    #cseType = models.CharField(max_length=200, blank=True)
    resourceType = models.IntegerField(default=5, blank=False)
    CSE_ID = models.CharField(max_length=200, blank=False, default='makazmie')
    CSE_Type = models.CharField(max_length=200, blank=False, default='IN-CSE')
    supportedResourceType = models.CharField(max_length=200, blank=True)
    pointOfAccess = models.CharField(max_length=200, blank=True, default='[]') # Array expected for this value
    nodeLink = models.CharField(max_length=200, blank=True)

    # Below attributes are present on TS-0004 Service Layer Core Protocol standard but not on IoTdm documentation
    e2eSecInfo = models.CharField(max_length=200, blank=True)

    # Below attributes are present on IoTdm documentation but not on TS-0004 Service Layer Core Protocol standard
    notificationCongestionPolicy = models.CharField(max_length=200, blank=True)

    def update_from_iotdm(self):
        print 'Update from IoTdm. Get resource parameters.'


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

    def clean(self):

        if settings.CHECK_IOTDM_RESPONSE is True:
            try:
                parent_uri = '/'.join([ancestor.name for ancestor in self.parent.get_ancestors(include_self=True)])
                print 'parent_uri', parent_uri
            except Exception, e:
                raise ValidationError('Unable to build parent URI. Please choose a Parent instance: '+str(e))

            check_parent = iotdm_api.retrieve(settings.IOTDM_SERVER+parent_uri)
            if check_parent.find('error') != -1:
                raise ValidationError('Resource parent cannot be found on IoTdm.')


class CONTAINER(Resource):
    resourceType = models.IntegerField(default=3, blank=False)
    # parent_resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='Parent Resource', default=1)

    def clean(self):

        if settings.CHECK_IOTDM_RESPONSE is True:
            try:
                parent_uri = '/'.join([ancestor.name for ancestor in self.parent.get_ancestors(include_self=True)])
                print 'parent_uri', parent_uri
            except Exception, e:
                raise ValidationError('Unable to build parent URI. Please choose a Parent instance: '+str(e))

            check_parent = iotdm_api.retrieve(settings.IOTDM_SERVER+parent_uri)
            if check_parent.find('error') != -1:
                raise ValidationError('Resource parent cannot be found on IoTdm.')


class CONTENTINSTANCE(Resource):
    resourceType = models.IntegerField(default=4, blank=False)
    content = models.CharField(max_length=1000, blank=False)

    can_have_children = False

    def clean(self):

        if settings.CHECK_IOTDM_RESPONSE is True:
            try:
                parent_uri = '/'.join([ancestor.name for ancestor in self.parent.get_ancestors(include_self=True)])
                print 'parent_uri', parent_uri
            except Exception, e:
                raise ValidationError('Unable to build parent URI. Please choose a Parent instance: '+str(e))

            check_parent = iotdm_api.retrieve(settings.IOTDM_SERVER+parent_uri)
            if check_parent.find('error') != -1:
                raise ValidationError('Resource parent cannot be found on IoTdm.')


class SUBSCRIPTION(Resource):
    resourceType = models.IntegerField(default=23, blank=False)
    notificationURI = models.CharField(max_length=2000, blank=False, default='["http://localhost:8000/admin/resources/iotdm"]')#"http://localhost:8586")
    notificationContentType = models.IntegerField(default=3)
    eventNotificationCriteria = models.CharField(max_length=100, default='{"net":[6]}')

    def clean(self):

        if settings.CHECK_IOTDM_RESPONSE is True:
            try:
                parent_uri = '/'.join([ancestor.name for ancestor in self.parent.get_ancestors(include_self=True)])
                print 'parent_uri', parent_uri
            except Exception, e:
                raise ValidationError('Unable to build parent URI. Please choose a Parent instance: '+str(e))

            check_parent = iotdm_api.retrieve(settings.IOTDM_SERVER+parent_uri)
            if check_parent.find('error') != -1:
                raise ValidationError('Resource parent cannot be found on IoTdm.')

class MQTTSubscription(Model):
    mac = models.CharField(max_length=200, blank=True)
    time = models.DateTimeField(blank=True)
    latitude = models.FloatField(max_length=100, blank=True)
    longitude = models.FloatField(max_length=100, blank=True)
    altitude = models.FloatField(max_length=100, blank=True)
    rxPacketsReceived = models.FloatField(max_length=100, blank=True)
    rxPacketsReceivedOK = models.FloatField(max_length=100, blank=True)
    txPacketsReceived = models.FloatField(max_length=100, blank=True)
    txPacketsEmitted = models.FloatField(max_length=100, blank=True)
    customData = models.FloatField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'MQTT Subscription'

    def __str__(self):
        return str(self.id)

# class Status(Model):
#     time = models.DateTimeField(blank=True)
#     lati = models.FloatField(max_length=100, blank=True)
#     long = models.FloatField(max_length=100, blank=True)
#     alti = models.FloatField(max_length=100, blank=True)
#     rxnb = models.FloatField(max_length=100, blank=True)
#     rxok = models.FloatField(max_length=100, blank=True)
#     rxfw = models.FloatField(max_length=100, blank=True)
#     ackr = models.FloatField(max_length=100, blank=True)
#     dwnb = models.FloatField(max_length=100, blank=True)
#     txnb = models.FloatField(max_length=100, blank=True)
#
#     class Meta:
#         verbose_name_plural = 'Statuses'
#
#     def __str__(self):
#         return str(self.id)