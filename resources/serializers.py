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
        fields = ['content']


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
        fields = ['id','name','creationTime','groups','children']



# Serializer with a custom sensor satus field just for nodes
class NodeSerializer(serializers.ModelSerializer):

    # Adding a custom field for node serializer
    sensor_status = serializers.SerializerMethodField()

    # Method that extracts the content of last rx cin, which is the latest sensor status
    def get_sensor_status(self, obj):
        obj_rx = obj.get_children().get(name='rx')
        print 'Children', obj_rx
        return obj_rx.last_cin()[0].content

    class Meta:
        model = CONTAINER
        fields = ['id', 'name','groups','sensor_status']#'__all__'
        # depth = 0

#------ Serializers for creating resources. Backwards compatibility with Data Simulator script -----#


class AppSerializer(serializers.ModelSerializer):

    class Meta:
        model = APP
        fields = ["name","resourceID"]


class ContainerPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = CONTAINER
        fields = ["name","resourceID","parent"]


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



