from rest_framework import serializers
from .models import UploadedCSVFile

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedCSVFile
        fields = ('file',)