# ─── IMPORTS ────────────────────────────────────────────────────────────────
import os, json
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from youtube_search import YoutubeSearch
from .models import CustomUser
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm # This line is critical!

# ─── HELPER FUNCTIONS ───────────────────────────────────────────────────────

def load_container():
    """Load default song data from static JSON file."""
    path = os.path.join(settings.BASE_DIR, 'card.json')
    with open(path, 'r') as f:
        return json.load(f)

def add_playlist(request):
    """Add a song to the user's playlist if it doesn't already exist."""
    title = request.POST.get('title')
    if not title:
        return

    try:
        cur_user = CustomUser.objects.get(username=request.user)
    except CustomUser.DoesNotExist:
        return

    if cur_user.songs.filter(song_title=title).exists():
        return

    try:
        song_data = YoutubeSearch(title, max_results=1).to_dict()[0]
        cur_user.songs.create(
            song_title=title,
            song_dur=request.POST.get('duration'),
            song_albumsrc=song_data['thumbnails'][0],
            song_channel=request.POST.get('channel'),
            song_date_added=request.POST.get('date'),
            song_youtube_id=request.POST.get('songid')
        )
    except Exception:
        pass

# ─── AUTHENTICATION VIEWS ───────────────────────────────────────────────────

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CustomLoginForm

def login_view(request):
    form = CustomLoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(request, username=email, password=password)  # username=email if USERNAME_FIELD = 'email'

        if user is not None:
            login(request, user)
            return redirect('main:dashboard')  # or wherever you want
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html', {'form': form})



@login_required
def logout_view(request):
    """Log out user and redirect to login page."""
    logout(request)
    messages.info(request, "You’ve been logged out.")
    return redirect('main:login')


def register_view(request):
    """
    Handles user registration by manually creating the user in the view.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Get data from the validated form
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            # Manually create the user using the custom model's manager
            User = get_user_model()
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            messages.success(request, f'Account created for {user.username}!')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
    else:
        form = CustomUserCreationForm()

    return render(request, 'main/register.html', {'form': form})

# ─── CORE VIEWS ─────────────────────────────────────────────────────────────

@login_required
def home(request):
    """Render homepage player and handle song addition."""
    if request.method == 'POST':
        add_playlist(request)
        return HttpResponse("")
    container = load_container()
    return render(request, 'player.html', {'CONTAINER': container, 'song': 'kSFJGEHDCrQ'})

@login_required
def playlist(request):
    """Display user's playlist and handle song deletion/addition."""
    try:
        cur_user = CustomUser.objects.get(username=request.user)
    except CustomUser.DoesNotExist:
        return redirect('main:home')

    if request.method == 'POST':
        add_playlist(request)
        return HttpResponse("")

    song_to_delete = request.GET.get('song')
    if song_to_delete:
        cur_user.songs.filter(song_title=song_to_delete).delete()

    user_playlist = cur_user.songs.all()
    return render(request, 'playlist.html', {'song': 'kSFJGEHDCrQ', 'user_playlist': user_playlist})

@login_required
def search(request):
    """Handle YouTube song search and display results."""
    if request.method == 'POST':
        add_playlist(request)
        return HttpResponse("")

    query = request.GET.get('search')
    if not query:
        return redirect('main:home')

    try:
        results = YoutubeSearch(query, max_results=10).to_dict()
        song_li = [results[:10:2], results[1:10:2]]
        song_id = song_li[0][0]['id']
    except Exception:
        return redirect('main:home')

    return render(request, 'search.html', {'CONTAINER': song_li, 'song': song_id})
