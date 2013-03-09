from django.contrib import admin
from members.models import (MFUser, Education, JobExperience, Endorsement,
                            MemberField,
                            )
from django.contrib.auth.admin import UserAdmin


admin.site.register(MFUser, UserAdmin)
admin.site.register(Education)
admin.site.register(JobExperience)
admin.site.register(Endorsement)
admin.site.register(MemberField)
