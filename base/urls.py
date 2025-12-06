from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.loginPage, name='login'),
    path('voting/', views.voting_dashboard, name='voting_dashboard'),
    path('success/', views.voting_success, name='voting_success'),
]
