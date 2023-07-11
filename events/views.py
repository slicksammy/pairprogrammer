from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .events import GithubPullReviewComment
from coder.interface import Interface as CoderInterface
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class EventView(View):
    @csrf_exempt
    def post(self, request, integration):
        parsed_body = GithubPullReviewComment.parse_event(json.loads(request.body))
        if GithubPullReviewComment.should_respond(parsed_body):
            user = User.objects.get(email="real@me.com")
            coder = CoderInterface.create_coder(tasks=[], requirements=str(parsed_body), context="", requested_recipe="github_comment_reply", user=user)
            interface = CoderInterface(coder.id)
            interface.run()
            interface.run()

        return JsonResponse({}, status=status.HTTP_200_OK)