from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .interface import Interface
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class ExceptionHandlerView(APIView):
    authentication_classes = []

    def handle_exception(self, exc):
        return Response({'error': "there was a system error, please try again"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class CreateCoderView(ExceptionHandlerView):
    @csrf_exempt
    def post(self, request):
        data = request.data
        user_id = request.session.get("api_user_id")
        if data.get("from_planner"):
            planner_id = data["planner_id"]
            coder = Interface.create_coder_from_planner(planner_id)
        else:
            tasks = data["tasks"]
            requirements = data["requirements"]
            context = data["context"]
            coder = Interface.create_coder(tasks=tasks, requirements=requirements, context=context, user_id=user_id)
        return Response({'id': coder.id }, status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name='dispatch')
class RunCoderView(ExceptionHandlerView):
    @csrf_exempt
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
    
class AppendOutputView(ExceptionHandlerView):
    def post(self, request):
        data = request.data
        id = data["id"]
        output = data["output"]
        command = data.get("command")
        interface = Interface(id)
        interface.append_output(output, command)
        return Response(status=status.HTTP_200_OK)
    
class ListCoderView(ExceptionHandlerView):
    def get(self, request):
        user_id = request.session.get("api_user_id")
        coders = Interface.list(user_id)
        return Response(coders, status=status.HTTP_200_OK)
    
class CreateUserMessageView(ExceptionHandlerView):
    def post(self, request):
        data = request.data
        id = data["id"]
        message = data["message"]
        interface = Interface(id)
        interface.append_user_message(message)
        return Response(status=status.HTTP_200_OK)


class AppendExceptionView(ExceptionHandlerView):    
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
