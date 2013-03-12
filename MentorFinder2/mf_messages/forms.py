from django import forms
from django.utils import timezone

from .models import MFMessage
from members.models import MFUser


class MFMessageForm(forms.ModelForm):

    class Meta:
        model = MFMessage
        fields = ('subject', 'content')
