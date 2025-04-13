import logging

from django.views import View
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.utils import IntegrityError

from comments.models import Comments

logger = logging.getLogger()


class CommentsView(View):
    """Comments controller with all methods."""

    def get(self, request: HttpRequest) -> HttpResponse:
        pass

    def post(self, request: HttpRequest) -> HttpResponse:
        pass

    def put(self, request: HttpRequest) -> HttpResponse:
        pass

    def patch(self, request: HttpRequest) -> HttpResponse:
        pass

    def delete(self, request: HttpRequest) -> HttpResponse:
        pass

# ТУПО СКОПИРОВАЛ С ПОСТС.ВЬЮ, ПОМЕНЯЛ НАЗВАНИЕ И СДЕЛАЛ ВСЕ МЕТОДЫ ПУСТЫМИ