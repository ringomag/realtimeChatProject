from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from chat.models import ChatRoom
from .forms import *
from django.contrib import messages
from .models import Message


def index(request):
    return render(request, 'index.html', {})

@login_required
def room(request, room_name):
    room = ChatRoom.objects.filter(name=room_name).first()
    chats = []
    if room:
        chats = Message.objects.filter(room=room)
    else:
        room = ChatRoom(name=room_name)
        room.save()
    return render(request, 'room.html', {'room_name':room_name, 'chats':chats})

def signup(request):
    if request.method == 'POST':
        form = ModifiedForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Succesfuly registered!")
            return redirect('login')
        else:
            print("errors ",form.errors)
    else:
        form = ModifiedForm()
    return render(request, 'registration/signup.html', {'form': form})