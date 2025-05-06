from django.urls import path

from comments.views import AddComment, AddReply


urlpatterns = [
    path(route="comment/<int:pk>", view=AddComment.as_view(), name="add_comment"),
    path(route="reply/<int:pk>", view=AddReply.as_view(), name="add_reply")
]