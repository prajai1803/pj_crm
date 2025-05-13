from rest_framework import serializers
from .models import Lead, CallLogs
from .models import LeadReminder, LeadReminderGuest

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



# Lead Reminder Serializer

class LeadReminderGuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadReminderGuest
        fields = ['email']


class LeadReminderSerializer(serializers.ModelSerializer):
    guests = serializers.ListField(
        child=serializers.EmailField(),
        write_only=True,
        required=False
    )
    guest_emails = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = LeadReminder
        fields = '__all__'
        extra_fields = ['guests', 'guest_emails']  # for clarity

    def get_guest_emails(self, obj):
        return [guest.email for guest in obj.guests.all()]

    def create(self, validated_data):
        guests = validated_data.pop('guests', [])
        lead_reminder = LeadReminder.objects.create(**validated_data)
        LeadReminderGuest.objects.bulk_create([
            LeadReminderGuest(lead_reminder=lead_reminder, email=email)
            for email in guests
        ])
        return lead_reminder

    def update(self, instance, validated_data):
        guests = validated_data.pop('guests', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if guests is not None:
            instance.guests.all().delete()
            LeadReminderGuest.objects.bulk_create([
                LeadReminderGuest(lead_reminder=instance, email=email)
                for email in guests
            ])

        return instance
