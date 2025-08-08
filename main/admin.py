from django.contrib import admin
from .models import PlaylistUser, PlaylistSong

# Register your models here.
admin.site.register(PlaylistUser)
admin.site.register(PlaylistSong)