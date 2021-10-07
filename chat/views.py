from django.shortcuts import redirect, render
from .forms import *
from django.contrib import messages

def index(request):
    return render(request, 'index.html', {})

def room(request, room_name):
    return render(request, 'room.html', {'room_name':room_name})

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