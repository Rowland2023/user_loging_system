from django.contrib import admin
from .models import CustomUser, PlaylistSong

admin.site.register(CustomUser)
admin.site.register(PlaylistSong)
