from django.urls import path
from .views import *
from .yasg import urlpatterns as url_doc

urlpatterns = [
    path('register/company/', CompanyRegisterView.as_view()),
    path('login/company/', CompanyLoginView.as_view(), name='company-login'),
    path('login/worker/', WorkerLoginView.as_view(), name='worker-login'),

    path('companies/', CompanyListView.as_view()),
    path('companies/<int:company_id>/workers/', WorkerListView.as_view()),
        

    path('workers/add/', WorkerCreateView.as_view()),
    path('workers/<int:worker_id>/free-slots/', WorkerFreeSlotsView.as_view()),

    path('reservations/create/', ReservationCreateView.as_view()),
    path('worker/reservations/', WorkerReservationListView.as_view()),
    
   

]


urlpatterns += url_doc