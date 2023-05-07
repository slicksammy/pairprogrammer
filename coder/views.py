from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .interface import Interface

# Create your views here.
class CreateCoderView(APIView):
    def post(self, request):
        data = request.data
        if data["from_planner"]:
            planner_id = data["planner_id"]
            coder = Interface.create_coder_from_planner(planner_id)
        else:
            tasks = data["tasks"]
            requirements = data["requirements"]
            context = data["context"]
            description = data["description"]
            coder = Interface.create_coder(tasks, requirements, context, description)
        return Response({'id': coder.id }, status=status.HTTP_200_OK)
    
class RunCoderView(APIView):
    def post(self, request):
        data = request.data
        id = data["id"]
        interface = Interface(id)
        interface.run()
        return Response({ 'command': interface.current_command() } , status=status.HTTP_200_OK)
    
class AppendOutputView(APIView):
    def post(self, request):
        data = request.data
        id = data["id"]
        output = data["output"]
        interface = Interface(id)
        interface.append_output(output)
        return Response(status=status.HTTP_200_OK)
    
class ListCoderView(APIView):
    def get(self, request):
        coders = Interface.list()
        return Response(coders, status=status.HTTP_200_OK)
    
class CreateUserMessageView(APIView):
    def post(self, request):
        data = request.data
        id = data["id"]
        message = data["message"]
        interface = Interface(id)
        interface.append_user_message(message)
        return Response(status=status.HTTP_200_OK)