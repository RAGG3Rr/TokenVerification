from django.contrib import admin
from api.models import CustomUser, Post

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    pass

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Post)