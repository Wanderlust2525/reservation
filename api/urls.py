from django.urls import path
from .views import *
from .yasg import urlpatterns as url_doc

urlpatterns = [
    path('company/register/', CompanyRegisterView.as_view(), name='company-register'),
    path('company/login/', CompanyLoginView.as_view(), name='company-login'),
    path('company/current/', CurrentCompanyView.as_view(), name='current-company'),
    path('companies/', CompanyListView.as_view(), name='companies_list'),
    path('companies/<int:company_id>/workers/', WorkerListView.as_view(), name='worker-list'),


    path('companies/', CompanyListView.as_view(), name='companies_list'),
    path('companies/<int:company_id>/workers/', WorkerListView.as_view()),
        


    path('workers/add/', WorkerCreateView.as_view(), name='worker-create'),
    path('workers/login/', WorkerLoginView.as_view(), name='worker-login'),
    path('workers/<int:worker_id>/', WorkerDetailView.as_view(), name='worker-detail'),
    path('workers/professions/', WorkerProfessionsView.as_view(), name='worker-professions'),
    path('workers/<int:worker_id>/free-slots/', WorkerFreeSlotsView.as_view(), name='worker-free-slots'),
    path('reservations/create/', ReservationCreateView.as_view(), name='reservation-create'),
    path('workers/<int:worker_id>/reservations/', WorkerReservationListView.as_view(), name='worker-reservations'),

    path('industries/', IndustryListView.as_view(), name='industry-list'),
    
    
   

]


urlpatterns += url_doc