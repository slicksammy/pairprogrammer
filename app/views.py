import os
import string
import random
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views import View
from app.authentication.email_backend import EmailBackend
from .forms import CustomUserCreationForm, CoderRecipeForm, CoderRecipeEditForm
from .models import UserApiKey, ClientUsage, ExternalApiKey, UserPreference
from coder.models import CoderRecipe
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from .interface import Interface
from integrations.interface import Interface as IntegrationsInterface
from coder.interface import Interface as CoderInterface


class HomeView(View):
    def get(self, request):
        return render(request, 'index_3.html')


class SignupView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        # signup_code = request.POST.get('signup_code')
        
        # if Interface.signup_code_exists(signup_code) is False:
        #     messages.error(request, 'Invalid signup code')
        #     return render(request, 'signup.html', {'form': form})
        
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            UserPreference.objects.create(user=user, preferences={ "model": "gpt-4-0613" })
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
        external_api_keys = ExternalApiKey.objects.filter(user=request.user)
        user_preference = UserPreference.objects.get(user=request.user)
        user_preference_keys = ['model']
        return render(request, 'dashboard.html', {'api_keys': api_keys, 'external_api_keys': external_api_keys, 'user': request.user, 'user_preference': user_preference, 'user_preference_keys': user_preference_keys})


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

class AddExternalApiKeyView(LoginRequiredMixin, View):
    login_url = '/login'

    def post(self, request):
        api_key = request.POST.get('api_key')
        service = request.POST.get('service')
        if api_key and service:
            new_key = ExternalApiKey(user=request.user, service_name=service, api_key=api_key)
            new_key.save()
            messages.success(request, 'External API key added successfully')
        else:
            messages.error(request, 'No API key or Service provided')
        return redirect('dashboard')

class UpdateUserPreferencesView(LoginRequiredMixin, View):
    login_url = '/login'

    def post(self, request):
        # Query for the existing UserPreference for the current user
        user_preference = UserPreference.objects.get(user=request.user)

        # Update the user preferences with the form data
        fields = ['model']
        form_data = {field: request.POST.get(field) for field in fields}
        user_preference.preferences = form_data
        user_preference.save()

        # Redirect back to the dashboard with a success message
        messages.success(request, 'Preferences updated successfully')
        return redirect('dashboard')

class CoderRecipeFormView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request):
        form = CoderRecipeForm()
        return render(request, 'coder_recipes_new.html', {'form': form})

    def post(self, request):
        form = CoderRecipeForm(request.POST)
 
        if form.is_valid():
            try:
                form.save(user=request.user)
            except Exception as e:
                messages.error(request, "There was an issue creating your recipe. It could be that your recipe name already exists.")
                return render(request, 'coder_recipes_new.html', {'form': form})

            messages.success(request, 'Agent deployed successfully')
            return redirect('/dashboard/recipes')
        else:
            error_message = ''
            for field, errors in form.errors.items():
                # Construct the error message for each field
                field_errors = ', '.join(errors)
                error_message += f"{field}: {field_errors}\n"
            messages.error(request, error_message)
            return render(request, 'coder_recipes_new.html', {'form': form})
        

class CoderRecipeEditFormView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request, recipe):
        recipe_data = CoderInterface.get_recipe(user=request.user, recipe=recipe)
        form = CoderRecipeEditForm(recipe_data)
        return render(request, 'coder_recipes_new.html', {'form': form})

    def post(self, request, recipe):
        params = {
            "recipe": request.POST['recipe'],
            "prompt": request.POST['prompt'],
            "functions": request.POST.getlist('functions')
        }

        form = CoderRecipeEditForm(params)
        if form.is_valid():
            try:
                form.save(user=request.user)
            except Exception as e:
                breakpoint()
                messages.error(request, "There was an issue updating your agent. It could be that your agent name already exists.")
                return render(request, 'coder_recipes_new.html', {'form': form})

            messages.success(request, 'Agent deployed successfully')
            return render(request, 'coder_recipes_new.html', {'form': form})
        else:
            error_message = ''
            for field, errors in form.errors.items():
                # Construct the error message for each field
                field_errors = ', '.join(errors)
                error_message += f"{field}: {field_errors}\n"
            messages.error(request, error_message)
            return render(request, 'coder_recipes_new.html', {'form': form})

class CoderRecipes(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request):
        recipes = CoderRecipe.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'coder_recipes.html', {'recipes': recipes})
    
class Integrations(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request):
        user = request.user

        return render(request, 'integrations.html', { 'integrations': IntegrationsInterface.available_integrations() })
    
    def post(self, request):
        integration_params = {k: v for k, v in request.POST.items() if k != "csrfmiddlewaretoken"}
        response = IntegrationsInterface.save_form(user=request.user, **integration_params)

        if response.get('integration_identifier'):
            messages.success(request, 'Integration saved successfully')
            return redirect(f'/dashboard/integrations/{response.get("integration_identifier")}')
        elif response.get('error_message'):
            messages.error(request, response.get('error_message'))
            return render(request, 'integrations_new.html', {'form': response.get('form')})
        else:
            form = response.get('form')
            error_message = ''
            for field, errors in form.errors.items():
                # Construct the error message for each field
                field_errors = ', '.join(errors)
                error_message += f"{field}: {field_errors}\n"
            messages.error(request, error_message)
            return render(request, 'integrations_new.html', {'form': form})
    
class IntegrationsFormView(LoginRequiredMixin, View):
    login_url = '/login'
    
    def get(self, request, integration):
        form = IntegrationsInterface.form(request.user, integration)
        return render(request, 'integrations_new.html', {'form': form, "integration": integration})

