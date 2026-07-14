from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.RegistrationAPIView.as_view(), name='registration'),
    path('confirm/', views.ConfirmAPIView.as_view(), name='confirm'),
    path('authorization/', views.AuthorizationAPIView.as_view(), name='authorization'),
]