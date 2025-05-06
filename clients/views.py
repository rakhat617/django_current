import logging
import os

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

from clients.models import Client
from clients.validators import validate_username, validate_email, validate_password
from clients.utils import send_email

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
            code = os.urandom(32).hex()
            Client.objects.create(
                email=email, 
                username=username,
                password=password,
                activation_code=code
                )
            send_email(
                template="account_activation.html", 
                context={
                    "username": username, 
                    "code": f"http://127.0.0.1:8000/activation/{username}/{code})"
                    }, 
                to=email, 
                title="Activate your account"
                )
            messages.info(request=request, message="Check your emeil for activation code")
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
    """Login Controller."""

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request=request, template_name="login.html")

    def post(self, request: HttpRequest) -> HttpResponse:
        username = request.POST.get("username")
        password = request.POST.get("password")
        client: Client | None = authenticate(
            request=request, 
            username=username, 
            password=password,
        )
        if not client:
            messages.error(
                request=request, 
                message="Wrong username or password"
            )
            return render(request=request, template_name="login.html")
        login(request=request, user=client)
        return redirect(to="base")


class LogoutView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        is_active = request.user.is_active
        if not is_active:
            return HttpResponse("Вы не авторизованы")
        logout(request=request)
        return redirect(to="base")
    

class ActivationView(View):
    def get(self, request: HttpRequest, username: str, code: str) -> HttpResponse:
        client = Client.objects.filter(username=username, activation_code=code).first()
        if not client:
            return HttpResponse(content="<h1>Who are you</h1>")
        client.is_active = True
        client.save(update_fields=["is_active"])
        return redirect(to="login")

class ResetPasswordView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request=request, template_name="reset_form.html")

    def post(self, request: HttpRequest) -> HttpResponse:
        username = request.POST.get("username")
        client = Client.objects.filter(username=username).first()
        if not client:
            return HttpResponse(content="<h1>Who are you</h1>")
        email = client.email
        new_password = os.urandom(8).hex()
        send_email(
                template="reset_password.html", 
                context={
                    "username": username, 
                    "new_password": new_password
                    }, 
                to=email, 
                title="Password reset"
                )
        password = make_password(password=new_password)
        client.password = password
        client.save(update_fields=["password"])
        messages.info(request=request, message="Check your email")
        return redirect(to="login") 