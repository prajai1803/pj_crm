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
    
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    


    lead_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15, unique=True)
    lead_source = models.ForeignKey(LeadSource, on_delete=models.SET_NULL, null=True, blank=True)
    lead_status = models.ForeignKey(LeadStatus, on_delete=models.SET_NULL, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    profession = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    qualification = models.CharField(max_length=255, null=True, blank=True)
    annual_income = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, related_name='leads_created', on_delete=models.SET_NULL, null=True, blank=True)
    assigned = models.ForeignKey(CustomUser, related_name='leads_assigned', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(CustomUser, related_name='leads_updated', on_delete=models.SET_NULL, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='leads', null=True)
    
    

    def __str__(self):
        return self.lead_name
    


    

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
        return self.lead_id
    

    

