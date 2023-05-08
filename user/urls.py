from django.contrib import admin
from django.urls import path
from .views import *
# from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('managerregister/', ManagerRegisterView.as_view(), name='managerregister'),
    path('developerregister/', DeveloperRegisterView.as_view(), name='developerregister'),
    path('teamleaderregister/', TeamLeaderRegisterView.as_view(), name='teamleaderregister'),
    path('testerregister/', TesterRegisterView.as_view(), name='testerregister'),
    path('login/', UserLoginView.as_view(), name='login'),
    # path('logout/',LogoutView.as_view(), name='logout'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('updateprofile/<int:pk>', ProfileUpdateView.as_view(), name='updateprofile'),
]