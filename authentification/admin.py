from django.contrib import admin
from .models import *
class CustomUserAdmin(admin.ModelAdmin):
    model = Clients

admin.site.register(Clients, CustomUserAdmin)
admin.site.register(Websites)
admin.site.register(Subdomain)
admin.site.register(Zapscan)
admin.site.register(Nucleiscan)