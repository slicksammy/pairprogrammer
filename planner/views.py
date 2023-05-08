from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .interface import Interface

# Create your views here.
class CreatePlannerView(APIView):
    def post(self,request):
        data = request.data
        requirements = data["requirements"]
        context = data["context"]
        planner = Interface.create_planner(requirements, context)
        return Response({'id': planner.id }, status=status.HTTP_200_OK)
    
class RunPlannerView(APIView):
    def post(self, request):
        data = request.data
        id = data["id"]
        interface = Interface(id)
        interface.run()
        message_content = interface.get_last_message()
        return Response(message_content , status=status.HTTP_200_OK)
    
class RespondPlannerView(APIView):
    def post(self, request):
        data = request.data
        id = data["id"]
        content = data["content"]
        interface = Interface(id)
        interface.respond(content)
        return Response(status=status.HTTP_200_OK)
    
class ListPlannerView(APIView):
    def get(self, request):
        planners = Interface.list()
        return Response(planners, status=status.HTTP_200_OK)
    
class GenerateTaskView(APIView):
    def post(self, request):
        data = request.data
        id = data["id"]
        interface = Interface(id)
        tasks = interface.generate_tasks()
        return Response(tasks, status=status.HTTP_200_OK)
    
class ListTasksView(APIView):
    def get(self, request):
        data = request.data
        id = data["id"]
        interface = Interface(id)
        tasks = interface.get_tasks()
        return Response(tasks, status=status.HTTP_200_OK)
    
class GetMessagesView(APIView):
    def get(self, request):
        data = request.query_params
        id = data["id"]
        interface = Interface(id)
        messages = interface.get_messages()
        return Response(messages, status=status.HTTP_200_OK)