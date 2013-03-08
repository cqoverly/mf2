from django import forms

from .models import MFUser

class JoinForm(forms.ModelForm):

    class Meta:
        model = MFUser
        fields = ('first_name',
                  'last_name',
                  'username',
                  'password',
                  'email',
                  )
