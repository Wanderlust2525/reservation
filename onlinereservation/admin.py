from django.contrib import admin
from .models import Industry, Company, Worker, Reservation

@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'address', 'industry']
    list_filter = ['industry']
    search_fields = ['name', 'phone']

@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'profession', 'company', 'client_duration_minutes']
    list_filter = ['company']
    search_fields = ['full_name', 'profession']

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['ticket_number', 'full_name', 'worker', 'date', 'time']
    list_filter = ['worker__company', 'date']
    search_fields = ['full_name', 'phone']
