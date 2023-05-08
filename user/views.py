from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView, UpdateView
from .models import User
from .forms import ManagerRegisterForm, DeveloperRegisterForm, TeamLeaderRegisterForm, TesterRegisterForm, ProfileUpdateForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from django.core.mail import send_mail
from .decorators import *
from django.contrib import messages

# Create your views here.
class ManagerRegisterView(CreateView):
    model = User
    form_class = ManagerRegisterForm
    template_name = 'user/managerregister.html'
    success_url = '/project/dashboard'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'manager'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user = form.save()
        # get email if form valid
        email = form.cleaned_data.get('email')
        subject = "New Account Created"
        message = "Welcome! New Account Created as Manager Successfully!"
        res = sendMail(email,subject,message)
        print(res)
        login(self.request, user)
        messages.success(self.request, "Manager registered successfully!")
        messages.success(self.request, "Mail sent successfully!")
        return super().form_valid(form)
    
class DeveloperRegisterView(CreateView):
    model = User
    form_class = DeveloperRegisterForm
    template_name = 'user/developerregister.html'
    success_url = '/project/dashboard'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'developer'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user = form.save()
        # get email if form valid
        email = form.cleaned_data.get('email')
        subject = "New Account Created"
        message = "Welcome! New Account Created as Developer Successfully!"
        res = sendMail(email,subject,message)
        print(res)
        login(self.request, user)
        messages.success(self.request, "Developer registered successfully!")
        messages.success(self.request, "Mail sent successfully!")
        return super().form_valid(form)
    
class TeamLeaderRegisterView(CreateView):
    model = User
    form_class = TeamLeaderRegisterForm
    template_name = 'user/teamleaderregister.html'
    success_url = '/project/dashboard'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teamleader'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user = form.save()
        # get email if form valid
        email = form.cleaned_data.get('email')
        subject = "New Account Created"
        message = "Welcome! New Account Created as Team Leader Successfully!"
        res = sendMail(email,subject,message)
        print(res)
        login(self.request, user)
        messages.success(self.request, "Team Leader registered successfully!")
        messages.success(self.request, "Mail sent successfully!")
        return super().form_valid(form)
    
class TesterRegisterView(CreateView):
    model = User
    form_class = TesterRegisterForm
    template_name = 'user/testerregister.html'
    success_url = '/project/dashboard'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'tester'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user = form.save()
        # get email if form valid
        email = form.cleaned_data.get('email')
        subject = "New Account Created"
        message = "Welcome! New Account Created as Tester Successfully!"
        res = sendMail(email,subject,message)
        print(res)
        login(self.request, user)
        messages.success(self.request, "Tester registered successfully!")
        messages.success(self.request, "Mail sent successfully!")
        return super().form_valid(form)

class UserLoginView(LoginView):
    template_name = 'user/login.html'

    def get_redirect_url(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_manager:
                return '/project/dashboard/'
            if self.request.user.is_developer:
                return '/project/dashboard/'
            if self.request.user.is_teamleader:
                return '/project/dashboard/'
            else:
                return '/project/dashboard/'   
            
class UserLogoutView(LogoutView):
    def get_redirect_url(self):
        return '/user/login'    

@method_decorator(login_required(login_url='/user/login'), name='dispatch')
class ProfileUpdateView(UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'user/update_profile.html'
    success_url = '/project/dashboard'

def sendMail(mailid,subject,message):
    # subject = "New Account Created"
    subject = subject
    # message = "Welcome! New Account Created Successfully!"
    message = message
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [mailid]
    res = send_mail(subject, message, email_from, recipient_list)
    if res>0:
        print("mail sent")
    else:
        print("mail not sent")
    print(res)
    return HttpResponse("mail sent")