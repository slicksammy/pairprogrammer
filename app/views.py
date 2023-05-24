import string
import random
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views import View
from app.authentication.email_backend import EmailBackend
from .forms import CustomUserCreationForm
from .models import UserToken
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')


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
        tokens = UserToken.objects.filter(user=request.user)
        return render(request, 'dashboard.html', {'tokens': tokens, 'user': request.user})


class GenerateTokenView(LoginRequiredMixin, View):
    login_url = '/'

    def post(self, request):
        tokens_count = UserToken.objects.filter(user=request.user).count()
        if tokens_count < 2:
            token = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
            user_token = UserToken(user=request.user, token=token)
            user_token.save()
            messages.success(request, 'API key generated successfully')
        else:
            messages.error(request, 'A user can only have up to 2 API keys')
        return redirect('dashboard')
