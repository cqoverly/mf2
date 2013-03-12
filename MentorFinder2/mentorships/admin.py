from django.contrib import admin
from .models import Mentorship, MentorshipRequest


class MentorshipAdmin(admin.ModelAdmin):
    list_display = ['mentoree', 'mentor', 'date_started', 'date_ended']
    ordering = ['mentoree', '-date_started']


class MentorshipRequestAdmin(admin.ModelAdmin):
    list_display = ['requesting_member',
                    'requested_mentor',
                    'request_date',
                    'accepted_date']
    ordering = ['requesting_member', '-request_date']


admin.site.register(Mentorship, MentorshipAdmin)
admin.site.register(MentorshipRequest, MentorshipRequestAdmin)

