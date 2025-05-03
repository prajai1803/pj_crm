from rest_framework import serializers
from .models import Lead, CallLogs

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'


class LeadCardSerializer(serializers.ModelSerializer):
    lead_status_name = serializers.CharField(source='lead_status.name', read_only=True)
    class Meta:
        model = Lead
        fields = ['id','lead_name','contact_number','lead_status','assigned', 'created_on', 'updated_on', 'lead_status_name']

class CallLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallLogs
        fields = '__all__'  