from django.urls import path
from clients.views import RegistrationView, LoginView, BasePageView

urlpatterns = [
    path(route='reg/', view=RegistrationView.as_view(), name="RegistrationView"),
    path(route='login/', view=LoginView.as_view(), name="LoginView"),
    path(route="", view=BasePageView.as_view(), name="BasePageView"),
]