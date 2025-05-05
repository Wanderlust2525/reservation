from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from account.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CompanyListSerializer, CompanyLoginSerializer, ReservationCreateSerializer, WorkerCreateSerializer, WorkerLoginSerializer, WorkerSerializer


from rest_framework.exceptions import NotFound
from api.serializers import CompanyRegisterSerializer
from onlinereservation.models import Company, Reservation, Worker





class CompanyRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = CompanyRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        company = serializer.save()
        return Response({'company_id': company.id, 'message': 'Компания успешно зарегистрирована!'}, status=status.HTTP_201_CREATED)


class CompanyLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = CompanyLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)

        if user and user.role == User.DIRECTOR:  
           
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            company = getattr(user, 'company', None)
            if company:
                return Response({
                    'refresh': str(refresh), 
                    'access': str(access_token),  
                    'company_id': company.id,
                    'company_name': company.name
                })
            return Response({"error": "Компания не найдена."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"error": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)
        

class CompanyListView(ListAPIView):
    serializer_class = CompanyListSerializer
    permission_classes = [AllowAny]
    queryset = Company.objects.all()  
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'name'] 
    search_fields = ['name', 'address']  
    ordering_fields = ['id', 'name']  

    def get_queryset(self):
        industry_id = self.request.query_params.get('industry')  
        queryset = super().get_queryset()
        if industry_id:
            queryset = queryset.filter(industry_id=industry_id) 
        return queryset
    
    
class WorkerCreateView(APIView):
        permission_classes = [IsAuthenticated]

        def post(self, request, *args, **kwargs):
            serializer = WorkerCreateSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            worker = serializer.save()
            return Response({'worker_id': worker.id, 'message': 'Сотрудник успешно создан!'}, status=status.HTTP_201_CREATED)

class WorkerLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = WorkerLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])

        if user:
            try:
                worker_profile = user.worker_profile
            except Worker.DoesNotExist:
                return Response({'error': 'Профиль сотрудника не найден.'}, status=status.HTTP_404_NOT_FOUND)
            return Response({
                'message': 'Успешный вход как сотрудник!',
                'worker_id': worker_profile.id,
                'full_name': worker_profile.full_name,
                'profession': worker_profile.profession  
            })

        return Response({'error': 'Неверные учетные данные или пользователь не является сотрудником.'}, status=status.HTTP_400_BAD_REQUEST)


class WorkerFreeSlotsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, worker_id, *args, **kwargs):
        try:
            worker = Worker.objects.get(id=worker_id)
        except Worker.DoesNotExist:
            return Response({'error': 'Работник не найден'}, status=status.HTTP_404_NOT_FOUND)
        
        free_slots = worker.get_free_slots(request.query_params.get('date'))
        return Response({'free_slots': free_slots})
    
class WorkerListView(generics.ListAPIView):
    serializer_class = WorkerSerializer
    permission_classes = [IsAuthenticated]  

    def get_queryset(self):
        company_id = self.kwargs['company_id']
        return Worker.objects.filter(company_id=company_id)


class WorkerDetailView(generics.RetrieveAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
    lookup_field = 'id'  
    lookup_url_kwarg = 'worker_id'
    

class ReservationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ReservationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reservation = serializer.save()

        return Response({
            'reservation_id': reservation.id,
            'message': 'Бронирование успешно создано!'
        }, status=status.HTTP_201_CREATED)
    

class WorkerReservationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, worker_id, *args, **kwargs):
        if request.user.role != 'worker' or request.user.worker_profile.id != worker_id:
            return Response({'error': 'У вас нет доступа к этому ресурсу.'}, status=status.HTTP_403_FORBIDDEN)
        reservations = Reservation.objects.filter(worker_id=worker_id)
        serializer = ReservationCreateSerializer(reservations, many=True)
        return Response(serializer.data)