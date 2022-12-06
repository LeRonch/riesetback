from django.contrib import admin
from .models import UserPicture

@admin.register(UserPicture)
class RequestDemoAdmin(admin.ModelAdmin):
  list_display = [field.name for field in
UserPicture._meta.get_fields()]