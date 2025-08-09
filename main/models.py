from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission

# ============================
# 🧠 Custom User Manager
# ============================
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field is required.")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

# ============================
# 🔐 Custom User Model
# ============================
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)

    # ✅ Use email as login field
    USERNAME_FIELD = 'email'
    # ✅ Do NOT include 'email' in REQUIRED_FIELDS
    REQUIRED_FIELDS = ['username', 'phone_number']

    # Override default manager
    objects = CustomUserManager()

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
        return f'Username = {self.username}'

# ============================
# 🎶 Playlist Song Model
# ============================
class PlaylistSong(models.Model):
    user = models.ForeignKey(
        CustomUser,
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
