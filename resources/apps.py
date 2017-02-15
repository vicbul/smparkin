from __future__ import unicode_literals

from django.apps import AppConfig
from SmartParking import settings
from django.core.exceptions import ValidationError


import socket, time


class ResourcesConfig(AppConfig):
    name = 'resources'
    # This class is needed to load signals/handlers with django server
    def ready(self):
        import signals.handlers


    # # Below loop check that connection to IoTdm is available. However it prevents Django server from refreshing
    # # TODO Try thread(), threading() or a django friendly solution
    # while True:
    #     if settings.CHECK_IOTDM_RESPONSE is True:
    #         iotdm_connect = socket.socket()
    #         try:
    #             iotdm_connect.connect((settings.IOTDM_IP, int(settings.IOTDM_PORT)))
    #             print 'Connection to IoTdm successful.'
    #         except Exception, e:
    #             raise ValidationError('Cannot connect to IoTdm: '+str(e))
    #     time.sleep(10)
