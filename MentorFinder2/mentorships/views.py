from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils import timezone

from .models import MentorshipRequest
from .forms import MentorshipRequestForm
from members.models import MFUser


def request_mentorship(request, mentor_pk):

    if request.method == 'POST':
        form = MentorshipRequestForm(request.POST)
        if request.POST.get('cancel') == '':
            return redirect('member_detail', pk=mentor_pk)
        elif form.is_valid():
            # process mentorship request
            req_message = form.cleaned_data['request_message']
            mentor = MFUser.objects.get(pk=mentor_pk)
            params = {'requesting_member': request.user,
                      'requested_mentor': mentor,
                      'request_message': req_message
                      }
            m_request = MentorshipRequest(**params)
            m_request.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 "Your request has been sent.")
        return redirect('member_detail', pk=mentor_pk)

    form = MentorshipRequestForm()
    return render(request,
                  'request_mentorship.html',
                  {'form': form,
                   'mentor': MFUser.objects.get(pk=mentor_pk),
                   },
                  )


def accept_mentorship(request, pk):

    mentorship = MentorshipRequest.objects.get(pk=pk)
    mentorship.accept_request()
    return redirect('member_profile', request.user.id)
