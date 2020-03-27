from rest_framework import serializers
from .models import Employee, Log



class employeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = '__all__'



class logSerializer(serializers.ModelSerializer):

    class Meta:
        model = Log
        fields = '__all__'