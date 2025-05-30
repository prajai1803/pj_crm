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
    guest_emails = serializers.ListField(
        child=serializers.EmailField(),
        write_only=True,
        required=False
    )
    # add read-only version
    guest_emails_read = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = LeadReminder
        fields = '__all__'
        extra_fields = ['guest_emails', 'guest_emails_read']  # optional clarity

    def get_guest_emails_read(self, obj):
        return [guest.email for guest in obj.guests.all()]

    def to_representation(self, instance):
        # Get the default representation
        rep = super().to_representation(instance)
        # Add guest_emails as read field (from guest_emails_read)
        rep['guest_emails'] = rep.pop('guest_emails_read', [])
        return rep

    def create(self, validated_data):
        guest_emails = validated_data.pop('guest_emails', [])
        lead_reminder = LeadReminder.objects.create(**validated_data)
        LeadReminderGuest.objects.bulk_create([
            LeadReminderGuest(lead_reminder=lead_reminder, email=email)
            for email in guest_emails
        ])
        return lead_reminder

    def update(self, instance, validated_data):
        guest_emails = validated_data.pop('guest_emails', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if guest_emails is not None:
            instance.guests.all().delete()
            LeadReminderGuest.objects.bulk_create([
                LeadReminderGuest(lead_reminder=instance, email=email)
                for email in guest_emails
            ])

        return instance


