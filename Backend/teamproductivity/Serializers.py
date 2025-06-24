from .models import *
from rest_framework import serializers


class TeamsSerializer(serializers.ModelSerializer):
     class Meta:
        model = Teams
        fields = '__all__'

class SprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = '__all__'

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__' 

