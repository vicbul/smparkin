from rest_framework import serializers
from models import *
from django.db.models import Max

class TestSerializer(serializers.ModelSerializer):

    class Meta:
        model = test
        fields = ('name','id')
        depth=1


class Test1Serializer(serializers.ModelSerializer):
    parent = TestSerializer()

    class Meta:
        model = test
        fields = ('name','parent')
        depth=1


# This represent the data received/transmitted from/to the sensors
class ContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = CONTENTINSTANCE
        fields = ['content', 'creationTime']


# this represent the rx/tx container
class ContainerSerializer(serializers.ModelSerializer):
    cin = ContentSerializer(many=True, source = 'last_cin', read_only=True)
    print ('Serializer Cin:', cin.data)

    class Meta:
        model = CONTAINER
        fields = ['id', 'name', 'cin', 'creationTime']#'__all__'
        # depth = 0


# this represents the sensor container
class ParentSerializer(serializers.ModelSerializer):

    children = ContainerSerializer(many=True, read_only=True)

    class Meta:
        model = Resource
        fields = ['id','name','creationTime','children']


class AppSerializer(serializers.ModelSerializer):

    class Meta:
        model = APP
        fields = ["name","resourceID"]


# class ContainerSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = CONTAINER
#         fields = ["name","resourceID","parent"]


class CinPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = CONTENTINSTANCE
        fields = ["creationTime","name","parent","content"]


class CinGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = CONTENTINSTANCE
        fields = ["creationTime","name","parent","content"]
        depth = 2


class LoraTxPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoraTx
        fields = ["creationTime","name","parent","applicationID","devEUI","data"]


class LoraTxGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoraTx
        fields = ["creationTime","name","parent","applicationID","devEUI","data"]
        depth = 2


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

#----------------------#

class ResourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Resource
        fields = ['id', 'name', 'parent', 'level']#'__all__'
        # depth = 0


class CinSerializer(serializers.ModelSerializer):

    class Meta:
        model = CONTENTINSTANCE
        fields = ["creationTime","name","parent","content"]
        depth = 1

