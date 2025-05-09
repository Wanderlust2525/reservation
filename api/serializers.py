from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from onlinereservation.models import Company, Industry, Reservation, Worker



from account.models import User


class CompanyRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Company
        fields = ['name', 'phone', 'address', 'industry', 'username', 'password']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Пользователь с таким username уже существует.")
        return value


    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        user = User.objects.create_user(username=username, password=password, role=User.DIRECTOR)
        company = Company.objects.create(user=user, **validated_data)
        return company

class CompanyLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class WorkerLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'phone', 'address', 'industry']

class CompanyLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)

class WorkerCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    work_start = serializers.TimeField(required=False)  

    class Meta:
        model = Worker
        fields = ['full_name', 'profession', 'phone', 'client_duration_minutes', 'work_start', 'work_end','username', 'password']


    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')

        user = User.objects.create_user(username=username, password=password, role='worker')

        request_user = self.context['request'].user
        if request_user.role != User.DIRECTOR:
            raise serializers.ValidationError("Только директор (компания) может добавлять сотрудников.")

        try:
            company = request_user.company
        except Company.DoesNotExist:
            raise serializers.ValidationError("У текущего пользователя нет связанной компании.")

        if 'work_start' not in validated_data:
            from datetime import time
            validated_data['work_start'] = time(hour=9, minute=0)

        worker = Worker.objects.create(user=user, company=company, **validated_data)
        return worker


class WorkerLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['id', 'full_name', 'profession', 'phone', 'client_duration_minutes', 'work_start', 'work_end','company']

class ReservationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['worker', 'full_name', 'phone', 'comment', 'date','time','ticket_number'] 
        read_only_fields = ['ticket_number']  

    def validate(self, data):
        worker = data['worker']
        if not worker.is_slot_available(data['date'], data['time']):
            raise serializers.ValidationError("Этот временной слот уже занят.")
        return data

    def create(self, validated_data):
        worker = validated_data['worker']
        date = validated_data['date']
        reservations_count = Reservation.objects.filter(worker=worker, date=date).count()
        ticket_number = f"{reservations_count + 1}"

        reservation = Reservation.objects.create(
            **validated_data,
            ticket_number=ticket_number
        )
        return reservation
    
class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ['id', 'name']