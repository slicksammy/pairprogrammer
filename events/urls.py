from django.urls import path
from . import views

urlpatterns = [
    path('events/<str:integration>', views.EventView.as_view(), name='new_event'),
]
