from datetime import datetime

from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages

from .models import MFUser, MemberField, JobExperience
from .forms import JoinForm, AddFieldForm, IntroForm
from fields.models import Field
from mf_messages.models import MFMessage


def home(request):

    return render(request, 'home.html')


class ViewMembers(ListView):
    """
    Creates view of all current members.
    Lists fields of interest for each member.
    Allows links for viewing detailed profiles of each member.
    """

    model = MFUser
    template_name = 'view_members.html'
    fields = ('last_name', 'first_name')
    context_object_name = 'member'

    def get_queryset(self):
        member = self.request.user
        return MFUser.objects.exclude(id=member.id)


def join(request):
    """
    Generates a form with which to become member.
    """
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
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Welcome, {0}'.format(request.user)
                                 )
        return redirect('member_profile', pk=member.id)
    else:
        form = JoinForm()

    return render(request,
                  'join.html',
                  {'form': form,
                   'message': message}
                  )


@login_required
def member_profile(request, pk):
    """
    Creates a profile listing for the logged in user.
    Allows adding/deleting of fields of interest.
    Allows links to endorsers, endorsees, mentors, mentorees.
    Allows for editing of Bio.
    """
    member_user = MFUser.objects.get(pk=pk)
    profile = member_user.create_profile()
    member_msgs = MFMessage.objects.filter(recipient=member_user, read=False)
    msg_count = member_msgs.count()

    if request.method == 'POST':
        intro_form = IntroForm(request.POST)
        if request.POST.get('save') == '':
            if intro_form.is_valid():
                intro_entry = intro_form.cleaned_data['intro_entry']
                member_user.intro = intro_entry
                member_user.save()
                messages.add_message(request,
                                     messages.SUCCESS,
                                     'Your new member intro has been saved')
                return redirect('member_profile', request.user.id)
    intro_form = IntroForm(initial={'intro_entry': profile.get('intro')})
    profile['intro_form'] = intro_form
    profile['msg_count'] = msg_count
    return render(request, 'member_profile.html', profile)

@login_required
def member_detail(request, pk):
    """
    Creates a profile of another user for the logged in user to examine.
    """

    member_user = MFUser.objects.get(pk=pk)
    profile = member_user.create_profile()
    return render(request,
                  'member_detail.html',
                  {'member': member_user,
                   'endorsed_by': profile.get('member_endorsers'),
                   'endorsed': profile.get('members_endorsed'),
                   'education': profile.get('education'),
                   'interests': profile.get('interests'),
                   'intro': profile.get('intro'),
                   'status': profile.get('status'),
                   }
                  )


@login_required
def add_field(request):
    message = ''
    member = request.user
    field_name = ''
    mentor = ''
    if request.method == 'POST':
        form = AddFieldForm(request.POST, user=request.user)
        if request.POST.get('cancel') == '':
            pk = member.id
            return redirect('member_profile', pk=pk)
        elif request.POST.get('add') == '':
            if form.is_valid():
                field_name = form.cleaned_data['name']
                mentor = form.cleaned_data['mentor'] == u'True'
                new_field = MemberField(field=field_name,
                                        member=member,
                                        can_mentor=mentor,
                                        date_entered=datetime.now().date())
                new_field.save()
                message = "{0} has been added to you profile.".format(type(mentor))
            else:
                message = "Invalid form."
    form = AddFieldForm(user=request.user)
    return render(request, 'add_field.html', {'message': message,
                                              'form': form})


def delete_field(request, field_pk):
        field = Field.objects.get(pk=field_pk)
        member_field = MemberField.objects.get(field=field, member=request.user)
        member_field.delete()
        return redirect('member_profile', pk=request.user.id)

def new_job(request):
    if request.method == 'POST':
        form = AddJobForm(request.POST)
        if request.POST.get('canel') == '':
            return redirect ('profile', request.user.id)
        else:
            params = {'member': request.user,
                      'company': form.cleaned_data['compay'],
                      'start_date': forrm.cleaned_data['start_date'],
                      'end_date': form.cleaned_data['end_date'],
                      'job_summary': form.cleaned_data['job_summary']
                      }
            new_job = JobExperience.add_job(params)
            return redirect('profile', request.user.id)

    form = AddJobForm()
    return render('new_job', {'form': form})


