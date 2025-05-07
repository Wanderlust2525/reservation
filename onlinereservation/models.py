from django.db import models
from datetime import datetime
from django.utils import timezone
from account.models import User  

class Industry(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': User.DIRECTOR})
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    industry = models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name



class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='worker_profile', limit_choices_to={'role': User.WORKER})
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='workers')
    full_name = models.CharField(max_length=255)
    profession = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    client_duration_minutes = models.PositiveIntegerField(default=15)
    work_start = models.TimeField(default="09:00:00")
    work_end = models.TimeField(default="18:00:00")  

    def __str__(self):
        return self.user.get_full_name

    def get_free_slots(self, date):
        if isinstance(date, str):
            date = datetime.strptime(date, '%Y-%m-%d').date()

       
        start = timezone.datetime.combine(date, self.work_start)
        end_time = timezone.datetime.combine(date, self.work_end)  
        delta = timezone.timedelta(minutes=self.client_duration_minutes)

        
        reservations = self.reservations.filter(date=date).values_list('time', flat=True)        
        current_time = start
        slots = []


        while current_time + delta <= end_time:
            if current_time.time() not in reservations:
                slots.append(current_time.time())
            current_time += delta

        return slots

    def is_slot_available(self, date, time):
        return not self.reservations.filter(date=date, time=time).exists()


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
            same_day_reservations = Reservation.objects.filter(date=self.date, worker=self.worker).order_by('time')
            next_number = same_day_reservations.count() + 1
            self.ticket_number = str(next_number)
        super().save(*args, **kwargs)
