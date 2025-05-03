from django.urls import path

from posts.views import PostsView, BasePostView, ShowDeletePostView, ReactionView, LikesView


urlpatterns = [
    path(route="", view=BasePostView.as_view(), name="base"),
    path(route="post_form", view=PostsView.as_view(), name="post_form"),
    path(route="show_post/<int:pk>", view=ShowDeletePostView.as_view(), name="pk_post"),
    # path(route="<int:pk>", view=ReactionView.as_view(), name="reaction_view"),
    path(route="<int:pk>/<str:reaction>", view=LikesView.as_view(), name="likes_view"),
    path(route="show_post/<int:pk>/<str:reaction>", view=LikesView.as_view(), name="likes_view_post"),
]