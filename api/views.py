from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import status

from .serializers import *

class CompanyLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_company:
            login(request, user)
            return Response({"message": "Вы успешно вошли как компания"})
        return Response({"error": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)
    

class CompanyRegisterView(CreateAPIView):
    serializer_class = CompanyRegisterSerializer
    permission_classes = [AllowAny]


class CompanyListView(ListAPIView):
    serializer_class = CompanyListSerializer
   

    def get_queryset(self):
        industry_id = self.request.query_params.get('industry')
        if industry_id:
            return Company.objects.filter(industry_id=industry_id)
        return Company.objects.all()


class WorkerCreateView(CreateAPIView):
    serializer_class = WorkerCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}


class WorkerListView(ListAPIView):
    serializer_class = WorkerListSerializer

    def get_queryset(self):
        company_id = self.kwargs.get('company_id')
        return Worker.objects.filter(company_id=company_id)
    
class WorkerLoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None and hasattr(user, 'worker'):
            login(request, user)
            return Response({"message": "Успешный вход как сотрудник"})
        return Response({"error": "Неверные данные или вы не сотрудник"}, status=status.HTTP_401_UNAUTHORIZED)

class WorkerFreeSlotsView(APIView):
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

        
        start_time = datetime.combine(date_obj, datetime.strptime('09:00', '%H:%M').time())
        end_time = datetime.combine(date_obj, datetime.strptime('18:00', '%H:%M').time())
        slot_duration = timedelta(minutes=worker.client_duration_minutes)

        all_slots = []
        current_time = start_time
        while current_time + slot_duration <= end_time:
            all_slots.append(current_time.time().strftime('%H:%M'))
            current_time += slot_duration

        
        reserved_times = Reservation.objects.filter(worker=worker, date=date_obj).values_list('time', flat=True)
        reserved_times = [t.strftime('%H:%M') for t in reserved_times]

        free_slots = [slot for slot in all_slots if slot not in reserved_times]

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
        worker = self.request.user.worker  
        date = self.request.query_params.get('date')  

        queryset = Reservation.objects.filter(worker=worker)
        if date:
            queryset = queryset.filter(date=date)

        return queryset.order_by('time')
