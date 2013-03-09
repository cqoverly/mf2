from django import forms

from .models import MFUser, MemberField
from fields.models import Field

class JoinForm(forms.ModelForm):

    class Meta:
        model = MFUser
        fields = ('first_name',
                  'last_name',
                  'username',
                  'password',
                  'email',
                  )



# class AddFieldForm(forms.ModelForm):

#     class Meta:
#         fields = ('name')

#     def __init__(self, *args, **kwargs):
#             self.request = kwargs.pop('request', None)
#             super(AddFieldForm, self).__init__(*args, **kwargs)
#             member = self.request.user
#             has_fields = MemberField.objects.filter(member=member)
#             self.fields.queryset.remove(has_fields)

