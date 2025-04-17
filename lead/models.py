from django.db import models
from accounts.models import CustomUser
from organizations.models import Organization

class Lead(models.Model):
    LEAD_SOURCES = [
        (1, 'Source 1'),
        (2, 'Source 2'),
    ]
    
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    
    LEAD_STATUSES = [
        ('Fresh', 'Fresh'),
        ('Follow Up', 'Follow Up'),
        ('Won', 'Won'),
        ('Re-Enquired', 'Re-Enquired'),
        ('Closed', 'Closed'),
    ]

    CENTER_CHOICES = [
        ('B2B', 'B2B'),
        ('Pune', 'Pune'),
    ]

    lead_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15, unique=True)
    lead_source = models.IntegerField(choices=LEAD_SOURCES, null=True, blank=True)
    lead_status = models.CharField(max_length=14, choices=LEAD_STATUSES, default='Fresh')
    center_name = models.CharField(max_length=50, choices=CENTER_CHOICES)
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
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='leads', null=True,)
    
    

    def __str__(self):
        return self.lead_name
