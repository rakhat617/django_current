from django.contrib import admin

from posts.models import Posts, Images, Categories

@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    model = Posts
    list_display = ("title", "date_publication", "user",)
    search_fields = ("title", "user",)
    list_filter = ("date_publication",)
    list_per_page = 50

@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    model = Images
    list_display = ("image", "post")
    search_fields = ("post",)
    # list_filter = ("date_created", "gender")
    list_per_page = 50

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    model = Categories
    list_display = ("title",)
    search_fields = ("title",)
    # list_filter = ("date_created", "gender")
    list_per_page = 50