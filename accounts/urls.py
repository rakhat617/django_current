from django.urls import path
from accounts.views import AccountView, EditProfileView, ChangePasswordView

urlpatterns = [
    path(route='', view=AccountView.as_view(), name="account"),
    path(route='edit/', view=EditProfileView.as_view(), name="edit_profile"),
    path(route='passwordchange/', view=ChangePasswordView.as_view(), name="change_password"),
]