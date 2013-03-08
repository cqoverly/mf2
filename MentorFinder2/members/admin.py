from django.contrib import admin
from members.models import MFUser, Education, JobExperience, Endorsement
from django.contrib.auth.admin import UserAdmin



admin.site.register(MFUser)
admin.site.register(Education)
admin.site.register(JobExperience)
admin.site.register(Endorsement)