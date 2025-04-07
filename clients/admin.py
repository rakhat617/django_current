from django.contrib import admin

from clients.models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    model = Client
    list_display = ("username", "email", "date_created", "is_superuser")
    search_fields = ("username", "email")
    list_filter = ("date_created", "gender")
    list_per_page = 50


# admin.site.register(Client, ClientAdmin)

