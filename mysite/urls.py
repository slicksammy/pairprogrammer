"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from coder.views import CreateCoderView, AppendOutputView, RunCoderView, ListCoderView, CreateUserMessageView, AppendExceptionView
from planner.views import CreatePlannerView, RunPlannerView, RespondPlannerView, ListPlannerView, GenerateTaskView, ListTasksView, GetMessagesView
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/coder', CreateCoderView.as_view(), name="create_coder"),
    path('api/v1/coder/run', RunCoderView.as_view(), name="run_coder"),
    path('api/v1/coder/append_output', AppendOutputView.as_view(), name="append_output"),
    path('api/v1/coder/user_message', CreateUserMessageView.as_view(), name="user_message"),
    path('api/v1/coder/list', ListCoderView.as_view(), name="append_output"),
    path('api/v1/coder/append_exception', AppendExceptionView.as_view(), name="append_exception"),
    # path('api/v1/planner', CreatePlannerView.as_view(), name="create_planner"),
    # path('api/v1/planner/run', RunPlannerView.as_view(), name="run_planner"),
    # path('api/v1/planner/respond', RespondPlannerView.as_view(), name="respond_planner"),
    # path('api/v1/planner/list', ListPlannerView.as_view(), name="list_planner"),
    # path('api/v1/planner/generate_tasks', GenerateTaskView.as_view(), name="generate_tasks"),
    # path('api/v1/planner/list_tasks', ListTasksView.as_view(), name="list_tasks"),
    # path('api/v1/planner/get_messages', GetMessagesView.as_view(), name="get_messages"),
    path('', include('app.urls'))
]
