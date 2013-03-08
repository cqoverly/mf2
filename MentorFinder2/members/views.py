from django.views.generic import ListView, DetailView
from django.forms import ModelForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

from .models import MFUser
from .forms import JoinForm


def home(request):
    message = ''

    test_message = 'This is the home page.'
    test_message_class = 'text-info'
    return render(request,
                  'home.html',
                  {'mesage': test_message,
                   'class': test_message_class},
                  )


def login(request):
    message = ''
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            message = 'Welcome back {}'.format(user)
            return redirect('home', {'message': message})
        else:
            message = 'Account is no longer valid.'
            # Return a 'disabled account' error message
    else:
        message = 'Invalid login'


def join(request):
    message = ''
    if request.method == 'POST':
        form = JoinForm(request.POST)
        if request.POST.get('cancel') == '':
            return redirect('home')
        elif form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            member = MFUser.objects.create_user(username=username,
                                                password=password,
                                                email=email
                                                )
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            member.first_name = first_name
            member.last_name = last_name
            member.save()
            message = 'Thank you for joining.'
        return redirect('home',
                        {'message': message,
                         'class': 'text-info'})

    else:
        form = JoinForm()

    return render(request,
                  'join.html',
                  {'form': form,
                   'message': message}
                  )

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
