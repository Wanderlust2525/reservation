from rest_framework import serializers

from onlinereservation.models import Company, Reservation, User, Worker


class CompanyRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Company
        fields = ['name', 'phone', 'address', 'industry', 'username', 'password', 'password2']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Пользователь с таким username уже существует.")
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Пароли не совпадают")
        return data

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        validated_data.pop('password2')
        user = User.objects.create_user(username=username, password=password, is_company=True)
        company = Company.objects.create(user=user, **validated_data)
        return company

class CompanyLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class WorkerLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class WorkerCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Worker
        fields = ['full_name', 'profession', 'phone', 'client_duration_minutes', 'username', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Пароли не совпадают")
        return data

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        validated_data.pop('password2')
        user = User.objects.create_user(username=username, password=password, is_worker=True)
        company = self.context['request'].user.company  # авторизованная компания
        worker = Worker.objects.create(user=user, company=company, **validated_data)
        return worker


class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'phone', 'address', 'industry']


class WorkerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['id', 'full_name', 'profession']


class ReservationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [
            'id',
            'full_name',
            'phone',
            'comment',
            'date',
            'time',
            'ticket_number',
            'worker',
        ]
        read_only_fields = ['ticket_number']

