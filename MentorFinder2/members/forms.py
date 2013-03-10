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


class AddFieldForm(forms.Form):

    name = forms.ModelChoiceField(queryset=Field.objects.all())
    mentor = forms.ChoiceField(choices=((None, 'No'), (True, 'Yes')))

    def __init__(self, *args, **kwargs):
        member = kwargs.pop('user')
        members_fields = MemberField.objects.filter(member=member.id)
        remove_list = [Field.objects.get(pk=item.field.id).id
                       for item in members_fields]
        super(AddFieldForm, self).__init__(*args, **kwargs)
        if member:
            self.fields['name'].queryset = \
                Field.objects.all().exclude(id__in=[id for id in remove_list])

    def clean(self):
        name = self.cleaned_data['name']
        mentor = self.cleaned_data['mentor']
        if not name:
            raise forms.ValidationError('No field entered.')
        if not mentor:
            raise forms.ValidationError('Mentorship field not answered.')
        return self.cleaned_data




