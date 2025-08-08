from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# ============================
# 🔐 Custom User Model
# ============================
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)

    # Fix reverse accessor conflicts
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self):
        return self.username


# ============================
# 🎵 Playlist User Model
# ============================
class PlaylistUser(models.Model):
    username = models.CharField(max_length=200)

    def __str__(self):
        liked_songs = self.playlist_song_set.all()
        return f'Username = {self.username}, Liked Songs = {[song.song_title for song in liked_songs]}'


# ============================
# 🎶 Playlist Song Model
# ============================
class PlaylistSong(models.Model):
    user = models.ForeignKey(
        PlaylistUser,
        on_delete=models.CASCADE,
        related_name='songs'
    )
    song_title = models.CharField(max_length=200)
    song_youtube_id = models.CharField(max_length=20)
    song_albumsrc = models.CharField(max_length=255)
    song_dur = models.CharField(max_length=7)
    song_channel = models.CharField(max_length=100)
    song_date_added = models.CharField(max_length=12)

    def __str__(self):
        return f'Title = {self.song_title}, Date = {self.song_date_added}'
