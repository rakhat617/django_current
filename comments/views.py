import logging
from typing import Literal

from django.views import View
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.utils import IntegrityError
from django.db.models.query import QuerySet

from comments.models import Comments
from posts.models import Posts
from clients.models import Client

logger = logging.getLogger()


class AddComment(View):
    def post(self, request: HttpRequest, pk:int) -> HttpResponse:
        user = request.user
        if not isinstance(user, Client):
            return JsonResponse(data={"error": "not authorized"})
        post = Posts.objects.filter(id=pk).first()
        if not post:
            return JsonResponse(data={"error": f"post with id {pk} is not found"})
        comment = Comments(
            post = post,
            user = user,
            text = request.POST.get("text")
        )
        comment.save()
        return redirect("pk_post", pk=pk)


class AddReply(View):
    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        user = request.user
        if not isinstance(user, Client):
            return JsonResponse(data={"error": "not authorized"})
        parent_comment = Comments.objects.filter(id=pk).first()
        if not parent_comment:
            return JsonResponse(
                data={"error": f"Comment with id {pk} not found"}
            )
        comment = Comments(
            post=parent_comment.post,
            user=user,
            parent_comment=parent_comment,
            text=request.POST.get("text")
        )
        comment.save()
        return redirect("pk_post", pk=parent_comment.post.pk)