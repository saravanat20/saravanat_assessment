# serializers.py
from rest_framework import serializers
from .models import Record

class RecordModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = '__all__'  # Or specify the fields you want to include
