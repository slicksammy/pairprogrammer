import string
import random
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from app.authentication.email_backend import EmailBackend
from .forms import CustomUserCreationForm
from .models import UserToken


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = EmailBackend().authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password')
    return render(request, 'login.html')


@login_required(login_url='/')
def dashboard(request):
    tokens = UserToken.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'tokens': tokens})


@login_required(login_url='/')
def generate_token(request):
    tokens_count = UserToken.objects.filter(user=request.user).count()
    if tokens_count < 2:
        if request.method == 'POST':
            token = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
            user_token = UserToken(user=request.user, token=token)
            user_token.save()
            messages.success(request, 'API key generated successfully')
    else:
        messages.error(request, 'A user can only have up to 2 API keys')
    return redirect('dashboard')
