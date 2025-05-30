from django.db import models
from accounts.models import CustomUser
from organizations.models import Organization


class LeadSource(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='lead_source', null=True)


    def __str__(self):
        return self.name
    
class LeadGender(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='lead_gender', null=True)


    def __str__(self):
        return self.name
    
class LeadFollowUp(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='lead_follow_up', null=True)


    def __str__(self):
        return self.name

class LeadStatus(models.Model):
    name = models.CharField(max_length=100)
    name_alias = models.CharField(max_length=100, null=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='lead_status', null=True)


    def __str__(self):
        return self.name

class Lead(models.Model):
    lead_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    lead_source = models.ForeignKey(LeadSource, on_delete=models.SET_NULL, null=True, blank=True)
    lead_status = models.ForeignKey(LeadStatus, on_delete=models.SET_NULL, null=True)
    gender = models.ForeignKey(LeadGender, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, related_name='leads_created', on_delete=models.SET_NULL, null=True, blank=True)
    assigned = models.ForeignKey(CustomUser, related_name='leads_assigned', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(CustomUser, related_name='leads_updated', on_delete=models.SET_NULL, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='leads', null=True)
    # changable
    qualification = models.CharField(max_length=255, null=True, blank=True)
    profession = models.CharField(max_length=255, null=True, blank=True)
    annual_income = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    

    def __str__(self):
        return self.lead_name

class LeadHistory(models.Model):
    lead_id = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='status_history')
    status = models.ForeignKey(LeadStatus, on_delete=models.SET_NULL, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.lead_id.lead_name} ➡ {self.status}"
        

class CallLogs(models.Model):

    CALL_TYPE_CHOICES = (
        (1, 'Incoming'),
        (2, 'Outgoing'),
        (3, 'Missed'),
    )

    id = models.AutoField(primary_key=True)
    call_type = models.IntegerField(choices=CALL_TYPE_CHOICES)
    called_time = models.DateTimeField()
    call_duration = models.IntegerField(help_text="Duration in seconds")
    lead_id = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='leads')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='call_logs', null=True)

    def __str__(self):
        return str(self.lead_id)


# Lead Reminders
class LeadReminder(models.Model):
    lead_id = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='lead_reminder')
    title = models.TextField()
    description = models.TextField(max_length=225, null=True, blank=True)
    follow_up = models.ForeignKey(LeadFollowUp, on_delete=models.SET_NULL, null=True)
    meeting_link = models.URLField(max_length=255, null=True, blank=True)
    reminder_date = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='lead_reminder', null=True)

    def __str__(self):
        return str(self.title)

class LeadReminderGuest(models.Model):
    lead_reminder = models.ForeignKey(LeadReminder, on_delete=models.CASCADE, related_name='guests')
    email = models.EmailField()

    def __str__(self):
        return self.email





