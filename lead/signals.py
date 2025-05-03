from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Lead, LeadHistory

@receiver(post_save, sender=Lead)
def create_lead_history_on_create(sender, instance, created, **kwargs):
    if created and instance.lead_status:
        LeadHistory.objects.create(
            lead_id=instance,
            status=instance.lead_status,
            changed_by=instance.created_by
        )

@receiver(pre_save, sender=Lead)
def track_lead_status_change(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old_instance = Lead.objects.get(pk=instance.pk)
    except Lead.DoesNotExist:
        return
    if old_instance.lead_status != instance.lead_status:
        LeadHistory.objects.create(
            lead_id=instance,
            status=instance.lead_status,
            changed_by=instance.updated_by
        )
