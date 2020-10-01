from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Treasure
from .forms import TreasureForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    treasures = Treasure.objects.all()
    return render(request, 'index.html',
                  {'treasures': treasures})


def detail(request, treasure_id):
    treasure = Treasure.objects.get(id=treasure_id)
    return render(request, 'detail.html', {'treasure': treasure})


def post_treasure(request):
    form = TreasureForm(request.POST, request.FILES)
    if form.is_valid():
        treasure = form.save(commit=False)
        treasure.user = request.user
        treasure.likes = 0
        treasure.save()
    return HttpResponseRedirect('/')


def profile(request, username):
    user = get_object_or_404(User.objects, username=username)
    if request.user.is_authenticated:
        user2 = request.user
        username = user.username
        if user2.username == user.username:
            treasures = Treasure.objects.filter(user=user)            
        else:
            treasures = Treasure.objects.filter(user=user2)
        form = TreasureForm()
        return render(request, 'profile.html',
                      {'username': username,
                       'treasures': treasures, 'form': form})
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/user/' + username)
                else:
                    print("The account has ben disabled")
            else:
                print("The username and password were incorrect .")
        else:
            form = LoginForm()
    return render(request, 'login.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/user/' + username)
                else:
                    print("The account has ben disabled")
            else:
                print("The username and password were incorrect .")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def like_treasure(request):
    treasure_id = request.POST.get('treasure_id', None)
    likes = 0
    if (treasure_id):
        treasure = Treasure.objects.get(id=int(treasure_id))
        if treasure is not None:
            likes = treasure.likes + 1
            treasure.likes = likes
            treasure.save()
    return HttpResponse(likes)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})
