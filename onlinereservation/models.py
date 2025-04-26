from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    is_company = models.BooleanField(default=False)
    is_worker = models.BooleanField(default=False)

class Industry(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    industry = models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='worker_profile')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='workers')
    full_name = models.CharField(max_length=255)
    profession = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    client_duration_minutes = models.PositiveIntegerField()

    def __str__(self):
        return self.full_name

    def get_free_slots(self, date):
        start = timezone.datetime.combine(date, timezone.datetime.min.time())
        end = timezone.datetime.combine(date, timezone.datetime.max.time())
        reservations = self.reservations.filter(date=date).values_list('time', flat=True)
        slots = []
        current_time = timezone.datetime.combine(date, timezone.datetime.min.time()).replace(hour=9, minute=0)  
        end_time = current_time.replace(hour=18, minute=0)  
        delta = timezone.timedelta(minutes=self.client_duration_minutes)

        while current_time + delta <= end_time:
            if current_time.time() not in reservations:
                slots.append(current_time.time())
            current_time += delta

        return slots


class Reservation(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='reservations')
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    comment = models.TextField(blank=True)
    date = models.DateField()
    time = models.TimeField()
    ticket_number = models.CharField(max_length=10, blank=True, unique=False)

    def save(self, *args, **kwargs):
        if not self.ticket_number:
            same_day_reservations = Reservation.objects.filter(date=self.date).order_by('ticket_number')
            next_number = same_day_reservations.count() + 1
            self.ticket_number = str(next_number) 
        super().save(*args, **kwargs)
