from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

class Camp(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('emergency', 'Emergency'),
        ('special', 'Special Drive'),
    ]

    title = models.CharField(max_length=200)
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    description = models.TextField()
    capacity = models.PositiveIntegerField(default=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    contact_email = models.EmailField(null=True, blank=True)
    contact_phone = models.CharField(max_length=15, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def is_past(self):
        return self.date < timezone.now()

    @property
    def is_full(self):
        return self.registrations.count() >= self.capacity

    @property
    def available_slots(self):
        return self.capacity - self.registrations.count()

    @property
    def status(self):
        if self.is_past:
            return 'past'
        elif self.is_full:
            return 'full'
        elif self.available_slots < 10:
            return 'almost-full'
        return 'open'

    @property
    def status_class(self):
        status_classes = {
            'past': 'secondary',
            'full': 'danger',
            'almost-full': 'warning',
            'open': 'success'
        }
        return status_classes.get(self.status, 'secondary')

    def send_registration_email(self, user):
        if not self.contact_email:
            return  # Skip sending email if no contact email is set
            
        subject = f'Registration Confirmation - {self.title}'
        message = f'''
        Dear {user.get_full_name()},

        Thank you for registering for the blood donation camp "{self.title}".

        Camp Details:
        Date: {self.date.strftime('%B %d, %Y at %I:%M %p')}
        Location: {self.location}
        
        Please arrive 15 minutes before the scheduled time.
        Don't forget to bring a valid ID proof.

        For any queries, please contact:
        Email: {self.contact_email}
        Phone: {self.contact_phone or 'Not provided'}

        Best regards,
        Blood Donation Management System
        '''
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

class CampRegistration(models.Model):
    camp = models.ForeignKey(Camp, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='camp_registrations')
    registered_at = models.DateTimeField(auto_now_add=True)
    attended = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('camp', 'user')
        ordering = ['-registered_at']

    def __str__(self):
        return f"{self.user.username} - {self.camp.title}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            self.camp.send_registration_email(self.user)
