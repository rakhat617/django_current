from django.shortcuts import render
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.http import HttpRequest, HttpResponse
from django.contrib import messages

from clients.models import Client



# Create your views here.
