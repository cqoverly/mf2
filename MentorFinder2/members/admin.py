from django.contrib import admin
from members.models import (MFUser, Education, JobExperience, Endorsement,
                            MemberField,
                            )
from django.contrib.auth.admin import UserAdmin


class MemberFieldAdmin(admin.ModelAdmin):
    list_display = ['member', 'field', 'can_mentor']
    ordering = ['member']


class EducationAdmin(admin.ModelAdmin):
    list_display = ['member',
                    'ed_type',
                    'year_completed',
                    'focus1',
                    'focus2',
                    ]
    ordering = ['member', '-year_completed']


class JobExperienceAdmin(admin.ModelAdmin):
    list_display = ['member',
                    'company',
                    'start_date',
                    'end_date',
                    ]
    ordering = ['member', '-end_date']


class EndorsementAdmin(admin.ModelAdmin):
    list_display = ['endorsee',
                    'endorser',
                    'date_made'
                    ]
    ordering = ['endorsee', 'endorser']


admin.site.register(MFUser, UserAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(JobExperience, JobExperienceAdmin)
admin.site.register(Endorsement, EndorsementAdmin)
admin.site.register(MemberField, MemberFieldAdmin)
