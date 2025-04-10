import logging

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

from clients.models import Client
from clients.validators import validate_username, validate_email, validate_password

logger = logging.getLogger()

class BasePageView(View):
    """Base Control, later to be rewritten"""

    def get(self, request: HttpRequest) -> HttpResponse:
        """To be rewritten"""
        return HttpResponse(content=f"<h1>Hello</h1>")


class RegistrationView(View):
    """Registration controller. Only get and post methods"""

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request=request, template_name='reg.html')
    
    def post(self, request: HttpRequest) -> HttpResponse:
        username = request.POST.get("username") 
        email = request.POST.get("email")
        raw_password = request.POST.get("password")

        is_validated = True
        validation_errors = ""

        try:
            validate_username(username)
        except ValidationError as e:
            is_validated = False
            validation_errors += f"{e.message}; "
        
        try:
            validate_email(email)
        except ValidationError as e:
            is_validated = False
            validation_errors += f"{e.message}; "

        try:
            validate_password(raw_password)
        except ValidationError as e:
            is_validated = False
            validation_errors += f"{e.message}; "

        if not is_validated:
            messages.error(request=request, message=f"{validation_errors}")
            return render(request=request, template_name="reg.html")
        
        password = make_password(password=raw_password)

        # client = Client.objects.get(email=email, username=username)
        # if client:
        #     messages.error(request=request, message="This username already exist")
        #     return render(request=request, template_name="reg.html")
        # client = Client.objects.create(username=username, email=email, password=password)
        # if client:
        #     messages.info(request=request, message="Thank you for registration")
        #     return render(request=request, template_name="reg.html")

        try:
            Client.objects.create(
                email=email, 
                username=username,
                password=password
                )
            messages.info(request=request, message="Thank you for registration")
            return render(request=request, template_name="reg.html")
        except IntegrityError as ie:
            logger.error(msg="Integrity error", exc_info=ie)
            messages.error(request=request, message="User already exist")
            return render(request=request, template_name="reg.html")
        except Exception as e:
            logger.error(msg="Something went wrong", exc_info=e)
            messages.error(request=request, message="Oops! Something went wrong")
            return render(request=request, template_name="reg.html")


class LoginView(View):
    """Login controller. Only get and post methods"""

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request=request, template_name='login.html')