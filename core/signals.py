from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Student, Room, Fee, Complaint, Visitor
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Fee

@receiver(post_save, sender=Student)
def update_room_occupancy_on_student_save(sender, instance, created, **kwargs):
    """Update room occupancy when student is created or modified"""
    if instance.room:
        room = instance.room
        
        # Recalculate occupied beds
        occupied = Student.objects.filter(room=room, is_active=True).count()
        room.occupied_beds = occupied
        
        # Update status
        if occupied >= room.capacity:
            room.status = 'occupied'
        elif occupied == 0:
            room.status = 'available'
        else:
            room.status = 'available'
        
        room.save(update_fields=['occupied_beds', 'status'])


@receiver(post_delete, sender=Student)
def update_room_occupancy_on_student_delete(sender, instance, **kwargs):
    """Update room occupancy when student is deleted"""
    if instance.room:
        room = instance.room
        occupied = Student.objects.filter(room=room, is_active=True).count()
        room.occupied_beds = occupied
        
        if occupied == 0:
            room.status = 'available'
        elif occupied >= room.capacity:
            room.status = 'occupied'
        
        room.save(update_fields=['occupied_beds', 'status'])


@receiver(post_save, sender=Fee)
def check_fee_status(sender, instance, created, **kwargs):

    if instance.amount_paid >= instance.amount:

        status = "paid"

    elif instance.amount_paid > 0:

        status = "partially_paid"

    else:

        status = "pending"

    # overdue
    if (
        instance.due_date and
        instance.due_date < timezone.now().date() and
        status == "pending"
    ):
        status = "overdue"

    Fee.objects.filter(
        pk=instance.pk
    ).update(
        status=status
    )


@receiver(post_save, sender=Complaint)
def log_complaint_activity(sender, instance, created, **kwargs):
    """Log complaint activities"""
    if created:
        # New complaint created
        pass
    else:
        # Complaint updated - could send notifications here
        if instance.status == 'resolved':
            instance.resolved_date = instance.updated_at
            Complaint.objects.filter(pk=instance.pk).update(
                resolved_date=instance.resolved_date
            )


@receiver(post_save, sender=Visitor)
def update_visitor_checkout(sender, instance, created, **kwargs):
    """Handle visitor checkout"""
    if not created and instance.check_out_date:
        # Visitor has checked out
        pass


def ready():
    """Called when app is ready"""
    pass
