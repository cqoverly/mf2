from django.contrib import admin
from .models import MFMessage


class MFMessageAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'sender', 'subject', 'date_sent']
    ordering = ['-date_sent']

admin.site.register(MFMessage, MFMessageAdmin)