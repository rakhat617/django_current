from django.urls import path
from clients.views import RegistrationView, LoginView, BasePageView, LogoutView

urlpatterns = [
    path(route='reg/', view=RegistrationView.as_view(), name="registration"),
    path(route='login/', view=LoginView.as_view(), name="login"),
    # path(route="", view=BasePageView.as_view(), name="BasePageView"),
    path(route="logout/", view=LogoutView.as_view(), name="logout"),
]