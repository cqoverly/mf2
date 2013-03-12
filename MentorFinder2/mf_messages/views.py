from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, redirect

from .models import MFMessage
from .forms import MFMessageForm
from members.models import MFUser


def new_message(request, member_id):
    recipient = MFUser.objects.get(pk=member_id)
    if request.method == 'POST':
        form = MFMessageForm(request.POST)
        msg = ''
        tag = ''
        if request.POST.get('cancel') == '':
            return redirect('member_profile', request.user.id)
        if form.is_valid():
            params = {'sender': request.user,
                      'recipient': recipient,
                      'subject': form.cleaned_data['subject'],
                      'content': form.cleaned_data['content'],
                      'date_sent': timezone.now()
                      }
            message = MFMessage(**params)
            try:
                message.save()
                msg = "Your message has been sent."
                tag = messages.SUCCESS
            except:
                msg = "Unable to send message. Sorry."
                tag = messages.ERROR
            messages.add_message(request,
                                 tag,
                                 msg,
                                 )
    form = MFMessageForm()
    return render(request,
                  'new_message.html',
                  {'form': form,
                   'recipient': recipient
                   },
                  )



