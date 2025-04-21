from rest_framework import serializers
from .models import Lead, CallLogs

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'


class LeadCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['id','lead_name','contact_number','lead_status',"assigned"]

class CallLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallLogs
        fields = '__all__'  