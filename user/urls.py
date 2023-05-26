from django.contrib import admin
from django.urls import path
from .views import *
# from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('managerregister/', ManagerRegisterView.as_view(), name='managerregister'),
    path('developerregister/', DeveloperRegisterView.as_view(), name='developerregister'),
    path('teamleaderregister/', TeamLeaderRegisterView.as_view(), name='teamleaderregister'),
    path('testerregister/', TesterRegisterView.as_view(), name='testerregister'),
    path('login/', UserLoginView.as_view(), name='login'),
    # path('logout/',LogoutView.as_view(), name='logout'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('updateprofile/<int:pk>', ProfileUpdateView.as_view(), name='updateprofile'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='user/password_reset.html'), name='password_reset'),
    path('password_change/', PasswordsChangeView.as_view(template_name='user/password_change.html'), name='password_change'),
    path('password_success/', PasswordsChangeDoneView, name='password_success'),
]