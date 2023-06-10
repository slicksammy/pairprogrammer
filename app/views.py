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
from .models import UserApiKey, ClientUsage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from .interface import Interface


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
        signup_code = request.POST.get('signup_code')
        form = CustomUserCreationForm(request.POST)
        
        if Interface.signup_code_exists(signup_code) is False:
            messages.error(request, 'Invalid signup code')
            return render(request, 'signup.html', {'form': form})
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        else:
            error_message = ''
            for field, errors in form.errors.items():
                # Construct the error message for each field
                field_errors = ', '.join(errors)
                error_message += f"{field}: {field_errors}\n"
            messages.error(request, error_message)
            return render(request, 'signup.html', {'form': form})


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
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
    login_url = '/login'

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


class VersionsView(View):
    def get(self, request):
        latest_version = Interface.latest_version().version
        project_versions = { 'cli': latest_version }
        return JsonResponse(project_versions)
    
class ExceptionHandlerView(APIView):
    authentication_classes = []

    def handle_exception(self, exc):
        return Response({'error': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(csrf_exempt, name='dispatch')
class ClientException(APIView):
    @csrf_exempt
    def post(self, request):
        data = request.data
        command = data['command']
        exception_class = data['exception']
        exception_message = data['message']
        exception_backtrace = data['backtrace']
        version = data['version']
        user_id = request.session.get("api_user_id")
        usage = ClientUsage(user_id=user_id,command=command, exception_class=exception_class, exception_message=exception_message, exception_backtrace=exception_backtrace, client_version=version)
        usage.save()
        return Response(status=status.HTTP_200_OK)