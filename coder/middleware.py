from django.http import JsonResponse
from app.interface import Interface as AppInterface
from rest_framework import status
from coder.views import CreateCoderView, AppendOutputView, RunCoderView, ListCoderView, CreateUserMessageView, AppendExceptionView
from app.views import ClientException


class APIKeyAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Exit early if the request is for the admin dashboard
        if request.path.startswith('/admin/'):
            return None

        api_views = [CreateCoderView, AppendOutputView, RunCoderView, ListCoderView, CreateUserMessageView, AppendExceptionView, ClientException]
        # Need class based views for this to work
        # Configure which views need auth above
        if view_func.view_class not in api_views:
            return None

        api_key = request.headers.get('Pairprogrammer-Api-Key')
        if not api_key:
            return JsonResponse({ 'error': "missing api key" }, status=status.HTTP_401_UNAUTHORIZED)
        user = AppInterface.user_from_api_key(api_key)
        if user is None:
            return JsonResponse({ 'error': "api_key is invalid" }, status=status.HTTP_401_UNAUTHORIZED)
        request.session["api_user_id"] = user.id
