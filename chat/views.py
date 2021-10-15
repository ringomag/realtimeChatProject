from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from chat.models import ChatRoom
from .forms import *
from django.contrib import messages
from .models import Message
from django.core.paginator import Paginator



def index(request):
    return render(request, 'index.html', {})

@login_required
def room(request, room_name):
    room = ChatRoom.objects.filter(name=room_name).first()
    chats = []
    if room:
        chats = Message.objects.filter(room=room)
        paginator = Paginator(chats, 8) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        room = ChatRoom(name=room_name)
        room.save()
        paginator = Paginator(chats, 8)
        page_obj = paginator.get_page(1)
    return render(request, 'room.html', {'room_name':room_name, 'page_obj':page_obj})

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