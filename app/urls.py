from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('dashboard/api_key', views.GenerateTokenView.as_view(), name='generate-api-key'),
    path('api/v1/versions', views.VersionsView.as_view(), name='versions'),
    path('api/v1/client_exception', views.ClientException.as_view(), name='client_exception')
]
