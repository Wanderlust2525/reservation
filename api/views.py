from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from datetime import datetime, date, timedelta

from onlinereservation.models import Company, Reservation, Worker

from .serializers import (
    CompanyLoginSerializer, CompanyRegisterSerializer, CompanyListSerializer,
    WorkerLoginSerializer, WorkerCreateSerializer, WorkerListSerializer,
    ReservationCreateSerializer
)




class CompanyLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = CompanyLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )

        if user and user.is_company:
            token, _ = Token.objects.get_or_create(user=user)
            company = getattr(user, 'company', None)
            if company:
                return Response({
                    'token': token.key,
                    'company_id': company.id,
                    'company_name': company.name
                })
            return Response({"error": "Компания не найдена."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"error": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

class CompanyRegisterView(CreateAPIView):
    serializer_class = CompanyRegisterSerializer
    permission_classes = [AllowAny]

class CompanyListView(ListAPIView):
    serializer_class = CompanyListSerializer
    permission_classes = [AllowAny]
    queryset = Company.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'name']
    search_fields = ['name', 'address']
    ordering_fields = ['id', 'name', 'created_at']

    def get_queryset(self):
        industry_id = self.request.query_params.get('industry')
        queryset = super().get_queryset()
        if industry_id:
            queryset = queryset.filter(industry_id=industry_id)
        return queryset



class WorkerLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = WorkerLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )

        if user and user.is_worker:
            token, _ = Token.objects.get_or_create(user=user)
            worker = getattr(user, 'worker_profile', None)
            if worker:
                today = date.today()
                free_slots = worker.get_free_slots(today)

                reservations = worker.reservations.filter(date=today).values(
                    'id', 'full_name', 'phone', 'time'
                )

                return Response({
                    'token': token.key,
                    'worker_id': worker.id,
                    'worker_name': worker.full_name,
                    'date': today,
                    'free_slots': free_slots,
                    'reservations': list(reservations)
                })

            return Response({"error": "Профиль работника не найден."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"error": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

class WorkerCreateView(CreateAPIView):
    serializer_class = WorkerCreateSerializer
    permission_classes = [IsAuthenticated]
    queryset = Worker.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}


class WorkerListView(ListAPIView):
    serializer_class = WorkerListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['company', 'full_name', 'profession', 'work_start']  
    search_fields = ['full_name', 'profession']  
    ordering_fields = ['full_name', 'profession', 'work_start'] 
    ordering = ['full_name'] 

    def get_queryset(self):
        company_id = self.kwargs.get('company_id')
        if company_id:
            return Worker.objects.filter(company_id=company_id)
        return Worker.objects.all()



class WorkerFreeSlotsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, worker_id):
        date_str = request.query_params.get('date')
        if not date_str:
            return Response({'error': 'Укажите дату в параметре ?date=YYYY-MM-DD'}, status=400)

        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Неверный формат даты. Используйте YYYY-MM-DD'}, status=400)

        try:
            worker = Worker.objects.get(id=worker_id)
        except Worker.DoesNotExist:
            return Response({'error': 'Работник не найден'}, status=404)

        free_slots = worker.get_free_slots(date_obj)

        return Response({
            'date': str(date_obj),
            'worker_id': worker.id,
            'free_slots': free_slots
        })

class ReservationCreateView(CreateAPIView):
    serializer_class = ReservationCreateSerializer
    permission_classes = [AllowAny]

class WorkerReservationListView(ListAPIView):
    serializer_class = ReservationCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not hasattr(user, 'worker_profile'):
            return Reservation.objects.none()

        worker = user.worker_profile
        date_param = self.request.query_params.get('date')

        queryset = Reservation.objects.filter(worker=worker)
        if date_param:
            queryset = queryset.filter(date=date_param)

        return queryset.order_by('time')
