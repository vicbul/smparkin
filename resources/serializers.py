from rest_framework import serializers
from models import *

class ResourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Resource
        fields = ['id', 'name', 'parent', 'level']#'__all__'
        # depth = 0


class AppSerializer(serializers.ModelSerializer):

    class Meta:
        model = APP
        fields = ["name","resourceID"]


class ContainerSerializer(serializers.ModelSerializer):

    class Meta:
        model = CONTAINER
        fields = ["name","resourceID","parent"]


class CinSerializer(serializers.ModelSerializer):

    class Meta:
        model = CONTENTINSTANCE
        fields = ["creationTime","name","parent","content"]
        depth = 1


class GatewayStatsSerializer(serializers.ModelSerializer):

    class Meta:
        model = GatewayStats
        fields = ["mac","time","latitude","longitude","altitude","rxPacketsReceived","rxPacketsReceivedOK","txPacketsReceived","txPacketsEmitted","customData"]


class GatewayRxSerializer(serializers.ModelSerializer):

    class Meta:
        model = GatewayRx
        fields = ["rxInfo","phyPayload"]


class AppDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppData
        fields = ["applicationID","applicationName","nodeName","devEUI","data", "data_decoded"]

# class StatusSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Status
#         fields = ["time","lati","long","alti","rxnb","rxok","rxfw","ackr","dwnb","txnb"]