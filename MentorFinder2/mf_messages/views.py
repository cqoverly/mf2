from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView

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


class MFMessage_list(ListView):

    model = MFMessage
    fields = ('recipient', 'sender', 'date_sent')
    context_object_name = 'member_msgs'
    template_name = 'mfmessage_list.html'

    def get_queryset(self):
        member = self.request.user
        return MFMessage.objects.filter(recipient=member)


def mfmessage_detail(request, msg_id):
    mfmessage = MFMessage.objects.get(pk=msg_id)
    mfmessage.read = True
    mfmessage.save()
    return render(request,
                  'msg_detail.html',
                  {'mfmessage': mfmessage}
                  )



