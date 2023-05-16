from django.contrib import admin
from django.urls import path
from app.views import home, signup, login_view

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('api/v1/coder', CreateCoderView.as_view(), name="create_coder"),
    path('api/v1/coder/run', RunCoderView.as_view(), name="run_coder"),
    path('api/v1/coder/append_output', AppendOutputView.as_view(), name="append_output"),
    path('api/v1/coder/user_message', CreateUserMessageView.as_view(), name="user_message"),
    path('api/v1/coder/list', ListCoderView.as_view(), name="append_output"),
    path('api/v1/coder/append_exception', AppendExceptionView.as_view(), name="append_exception"),
    path('api/v1/planner', CreatePlannerView.as_view(), name="create_planner"),
    path('api/v1/planner/run', RunPlannerView.as_view(), name="run_planner"),
    path('api/v1/planner/respond', RespondPlannerView.as_view(), name="respond_planner"),
    path('api/v1/planner/list', ListPlannerView.as_view(), name="list_planner"),
    path('api/v1/planner/generate_tasks', GenerateTaskView.as_view(), name="generate_tasks"),
    path('api/v1/planner/list_tasks', ListTasksView.as_view(), name="list_tasks"),
    path('api/v1/planner/get_messages', GetMessagesView.as_view(), name="get_messages"),
]
