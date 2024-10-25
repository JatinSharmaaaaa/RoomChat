from django.contrib.auth.decorators import login_required# type: ignore
from .models import Room, Message
# views.py (add these to the existing file)
from django.contrib.auth import login, authenticate# type: ignore
from django.contrib.auth.forms import UserCreationForm# type: ignore

from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.contrib.auth.decorators import login_required# type: ignore
from .forms import RoomForm  # Make sure this import is present

@login_required
def dashboard(request):
    rooms = Room.objects.all()
    return render(request, 'dashboard.html', {'rooms': rooms})



@login_required
def room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    messages = Message.objects.filter(room=room).order_by('-timestamp')[:50]
    return render(request, 'room.html', {'room': room, 'messages': messages})

@login_required
def room_view(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    return render(request, 'room.html', {'room': room})

@login_required
def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.created_by = request.user
            room.save()
            room.members.add(request.user)  # Add the creator as a member
            return redirect('room', room_id=room.id)  # Redirect to the room page
    else:
        form = RoomForm()
    return render(request, 'create_room.html', {'form': form})

@login_required
def join_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    room.members.add(request.user)
    return redirect('room', room_id=room.id)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def logout_view(request):
    if request.method == 'GET' or request.method == 'POST':
        logout(request)
        return HttpResponseRedirect('/')