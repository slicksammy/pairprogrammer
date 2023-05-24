from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .interface import Interface
   
# Create your views here.
class CreateCoderView(APIView):
    def post(self, request):
        data = request.data
        if data.get("from_planner"):
            planner_id = data["planner_id"]
            coder = Interface.create_coder_from_planner(planner_id)
        else:
            tasks = data["tasks"]
            requirements = data["requirements"]
            context = data["context"]
            coder = Interface.create_coder(tasks, requirements, context)
        return Response({'id': coder.id }, status=status.HTTP_200_OK)
    
class RunCoderView(APIView):
    def post(self, request):
        data = request.data
        id = data["id"]
        print("*"*50)
        print(f"starting coder run for {id}")
        interface = Interface(id)
        interface.run()
        response = Response(interface.status() , status=status.HTTP_200_OK)
        print("*"*50)
        print("api response")
        print(response.data)
        return response
    
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


class AppendExceptionView(APIView):    
    def post(self, request):
        data = request.data
        coder_id = data.get('id')
        exception_message = data.get('exception_message')
        exception_class = data.get('exception')
        if not coder_id or not exception_class or not exception_message:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        interface = Interface(coder_id)
        interface.client_error(exception_class, exception_message)
        return Response(status=status.HTTP_200_OK)
