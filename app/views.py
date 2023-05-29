import os
import string
import random
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views import View
from app.authentication.email_backend import EmailBackend
from .forms import CustomUserCreationForm
from .models import UserApiKey
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings


class HomeView(View):
    def get(self, request):
        readme_content = None
        readme_path = os.path.join(settings.BASE_DIR, 'README.md')
        with open(readme_path, 'r') as f:
            readme_content = f.read()

        return render(request, 'home.html', {'readme_content': readme_content})


class SignupView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        user = EmailBackend().authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password')
            return render(request, 'login.html')


class DashboardView(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        api_keys = UserApiKey.objects.filter(user=request.user)
        return render(request, 'dashboard.html', {'api_keys': api_keys, 'user': request.user})


class GenerateTokenView(LoginRequiredMixin, View):
    login_url = '/'

    def post(self, request):
        keys_count = UserApiKey.objects.filter(user=request.user).count()
        if keys_count < 2:
            key = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
            api_key = UserApiKey(user=request.user, key=key)
            api_key.save()
            messages.success(request, 'API key generated successfully')
        else:
            messages.error(request, 'A user can only have up to 2 API keys')
        return redirect('dashboard')
