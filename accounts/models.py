from django.db import models

from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from organizations.models import Organization

USER_TYPES = (("Admin", "Admin"),("Telecaller","Telecaller"))
GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

class CustomUserManager(BaseUserManager):
    def create_user(self, email, full_name, user_type,contact_number, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, user_type=user_type, contact_number=contact_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, user_type,contact_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email =email,full_name = full_name,user_type = user_type, contact_number=contact_number, password=password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True, related_name='users')
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    location = models.CharField(max_length=20, null=True, blank=True)
    contact_number = models.CharField(max_length=10, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    device_id = models.CharField(max_length=20, null=True, blank=True)
    notification_token = models.CharField(max_length=50, null=True, blank=True)
    user_type = models.CharField(max_length=30, choices=USER_TYPES, null=True, blank=True)
    email_verified = models.BooleanField(default=False, null=True, blank=True)
    contact_number_verified = models.BooleanField(default=False, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name','user_type','contact_number']

    def __str__(self):
        return self.email


class OTP(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
