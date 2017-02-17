from rest_framework import serializers
from models import *

class ResourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Resource
        fields = ['id', 'name', 'parent', 'level']#'__all__'
        # depth = 0

class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = ["time","lati","long","alti","rxnb","rxok","rxfw","ackr","dwnb","txnb"]