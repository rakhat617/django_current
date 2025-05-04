import logging
from typing import Literal

from django.views import View
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.utils import IntegrityError
from django.db.models.query import QuerySet
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login

from posts.models import Posts, Images, Categories, Reactions
from clients.models import Client
from clients.validators import validate_username, validate_email, validate_password

logger = logging.getLogger()


class AccountView(View):
    def get(self, request: HttpRequest):
        user = request.user
        if not user.is_active:
            return redirect(to="login")
        # posts: QuerySet[Posts] = Posts.objects.all()
        return render(
            request=request, template_name="account.html", 
            context={
                "user": user
            }
        )

class EditProfileView(View):
    def get(self, request: HttpRequest):
        user = request.user
        if not user.is_active:
            return redirect(to="login")
        birthdate = str(user.birthday)
        return render(request=request, template_name="edit_profile.html", 
            context={
                "user": user,
                "birthdate": birthdate
            }
        )
    def post(self, request: HttpRequest):
        user = request.user
        username = request.POST.get("username") 
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        gender = request.POST.get("gender")
        birthday = request.POST.get("birthdate")

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
        
        if not is_validated:
            messages.error(request=request, message=f"{validation_errors}")
            return render(request=request, template_name="edit_profile.html")

        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        if gender:
            user.gender = gender
        if birthday:
            user.birthday = birthday
        user.save()
        messages.info(request=request, message="Changes saved!")
        return redirect(to="account")
    
class ChangePasswordView(View):
    def get(self, request: HttpRequest):
        user = request.user
        if not user.is_active:
            return redirect(to="login")
        return render(request=request, template_name="change_password.html")
    def post(self, request: HttpRequest):
        user = request.user
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        if not check_password(current_password, user.password):
            messages.error(request=request, message="Incorrect password")
            return render(request=request, template_name="change_password.html")
        if new_password != confirm_password:
            messages.error(request=request, message="New passwords don't match")
            return render(request=request, template_name="change_password.html")
        try:
            validate_password(new_password)
        except ValidationError as e:
            messages.error(request=request, message=f"{e.message}")
            return render(request=request, template_name="change_password.html")
        password = make_password(password=new_password)
        user.password = password
        user.save()
        login(request=request, user=user)
        messages.info(request=request, message="Password changed successfully!")
        return render(request=request, template_name="account.html")
