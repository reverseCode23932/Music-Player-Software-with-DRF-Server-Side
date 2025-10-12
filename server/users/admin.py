from django.contrib import admin
from .models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_staff", "is_superuser", "joined_at")
    search_fields = ("username", "email")
    list_filter = ("is_staff", "is_superuser", "joined_at")


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "image", "created_at")
    search_fields = ("title", "author")
    list_filter = ("title", "author", "created_at")
    
@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "image", "created_at")
    search_fields = ("title", "author")
    list_filter = ("title", "author", "created_at")