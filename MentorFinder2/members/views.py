from django.views.generic import ListView, DetailView
from django.forms import ModelForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

from .models import MFUser, Education, Endorsement
from .forms import JoinForm #AddFieldForm


def home(request):
    message = request.session.get('message')
    text_class = request.session.get('text_class')
    if not message:
        message = ''
    test_message = 'This is the home page.'
    test_message_class = 'text-info'
    return render(request, 'home.html', {'message': message, 'class': text_class})


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
            user = authenticate(username=username, password=password)
            login(request, user)
            request.session['message'] = 'Welcome, {0}!'.format(member)
            request.session['text_class'] = 'text-info'
        return redirect('home')
    else:
        form = JoinForm()

    return render(request,
                  'join.html',
                  {'form': form,
                   'message': message}
                  )

@login_required
def member_profile(request, pk):

    member_user = MFUser.objects.get(pk=pk)
    profile = member_user.create_profile()
    return render(request,
                  'member_profile.html',
                  {'member': member_user,
                   'endorsed_by': profile.get('member_endorsers'),
                   'endorsed': profile.get('members_endorsed'),
                   'education': profile.get('education'),
                   }
                  )

# @login_required
# def add_field(request):
#     member = request.user
#     if request.method == 'POST':
#         form = AddFieldForm(request.POST)
#     if form.is_valid():
#         field_name = form.cleaned_data['name']
#         # process the data
#     members_fields = MemberField.objects.filter(member=member)
#     form = AddFieldForm()
#     form.queryset = Field.objects.exclude()




