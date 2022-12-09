from django.contrib import admin
from .models import UserPicture, Comment, Country, Creation, Tag

@admin.register(UserPicture)
class RequestDemoAdmin(admin.ModelAdmin):
  list_display = [field.name for field in
UserPicture._meta.get_fields()]

admin.site.register(Country)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Creation)