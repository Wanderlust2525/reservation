from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
<<<<<<< HEAD
from rest_framework import generics
from rest_framework.generics import RetrieveAPIView  
=======
from datetime import date, datetime, timedelta
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
>>>>>>> be9ca6a (register)
from rest_framework.response import Response
from rest_framework import status, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from account.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CompanyListSerializer, CompanyLoginSerializer, IndustrySerializer, ReservationCreateSerializer, WorkerCreateSerializer, WorkerLoginSerializer, WorkerSerializer


<<<<<<< HEAD
from rest_framework.exceptions import NotFound
from api.serializers import CompanyRegisterSerializer
from onlinereservation.models import Company, Industry, Reservation, Worker
=======
class CompanyLoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CompanyLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)

        if user and user.is_company:
            token, created = Token.objects.get_or_create(user=user)
            company = getattr(user, 'company', None)
            return Response({
                'token': token.key,
                'company_id': company.id,
                'company_name': company.name
            })

        return Response({"error": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

    
>>>>>>> be9ca6a (register)





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
    queryset = Company.objects.all()
    serializer_class = CompanyListSerializer
<<<<<<< HEAD
    permission_classes = [AllowAny]
    queryset = Company.objects.all()  
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'name'] 
    search_fields = ['name', 'address']  
    ordering_fields = ['id', 'name']  
=======
    permission_classes = [AllowAny]  
>>>>>>> be9ca6a (register)

    def get_queryset(self):
        industry_id = self.request.query_params.get('industry')  
        queryset = super().get_queryset()
        if industry_id:
<<<<<<< HEAD
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

=======
            return Company.objects.filter(industry_id=industry_id)
        return Company.objects.all()
    
    
class WorkerLoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = WorkerLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)

        if user and user.is_worker:
            token, created = Token.objects.get_or_create(user=user)
            worker = getattr(user, 'worker_profile', None)
            if not worker:
                return Response({"error": "Профиль работника не найден."}, status=status.HTTP_404_NOT_FOUND)
            return Response({
                'token': token.key,
                'worker_id': worker.id,
                'worker_name': worker.full_name,
            })

        return Response({"error": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)


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
>>>>>>> be9ca6a (register)
    def post(self, request, *args, **kwargs):
        serializer = WorkerLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

<<<<<<< HEAD
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

=======
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)

        if user and user.is_worker:
            token, _ = Token.objects.get_or_create(user=user)
            worker = user.worker_profile

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

        return Response({"error": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)


>>>>>>> be9ca6a (register)

class WorkerFreeSlotsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, worker_id, *args, **kwargs):
        try:
            worker = Worker.objects.get(id=worker_id)
        except Worker.DoesNotExist:
            return Response({'error': 'Работник не найден'}, status=status.HTTP_404_NOT_FOUND)
        
        free_slots = worker.get_free_slots(request.query_params.get('date'))
        return Response({'free_slots': free_slots})
    
class WorkerListView(generics.ListAPIView):
    serializer_class = WorkerSerializer
    permission_classes = [AllowAny]  

    def get_queryset(self):
<<<<<<< HEAD
        company_id = self.kwargs['company_id']
        return Worker.objects.filter(company_id=company_id)
=======
        user = self.request.user

        if not hasattr(user, 'worker_profile'):
            return Reservation.objects.none()  

        worker = user.worker_profile
        date = self.request.query_params.get('date')
>>>>>>> be9ca6a (register)


class WorkerDetailView(RetrieveAPIView ):
    queryset = Worker.objects.all()
    permission_classes = [AllowAny]  
    serializer_class = WorkerSerializer
    lookup_field = 'id'  
    lookup_url_kwarg = 'worker_id'




class WorkerProfessionsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        professions = Worker.objects.values('id', 'profession').distinct()
        return Response(professions)
    

class ReservationCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = ReservationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reservation = serializer.save()

        return Response({
            'reservation_id': reservation.id,
            'message': 'Бронирование успешно создано!'
        }, status=status.HTTP_201_CREATED)
    

class WorkerReservationListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, worker_id, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'worker' and request.user.worker_profile.id == worker_id:
            reservations = Reservation.objects.filter(worker_id=worker_id)
        else:
            reservations = Reservation.objects.filter(worker_id=worker_id).only('date', 'time', 'ticket_number')  
        serializer = ReservationCreateSerializer(reservations, many=True)
        return Response(serializer.data)
    
class IndustryListView(generics.ListAPIView):
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer
    permission_classes = [AllowAny]