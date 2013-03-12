from django.db import models
from django.utils import timezone


from members.models import MFUser
from mf_messages.models import MFMessage


class Mentorship(models.Model):
    mentoree = models.ForeignKey(MFUser, related_name='is_mentored')
    mentor = models.ForeignKey(MFUser, related_name='mentors')
    date_started = models.DateField()
    date_ended = models.DateField(null=True)

    class Meta:
        ordering = ['mentoree', '-date_started']
        verbose_name = 'Mentorship'
        verbose_name_plural = 'Mentorships'


class MentorshipRequest(models.Model):
    requesting_member = models.ForeignKey(MFUser, related_name='requests')
    requested_mentor = models.ForeignKey(MFUser, related_name='is_requested')
    request_message = models.TextField(max_length=1000)
    request_date = models.DateField()
    accepted_date = models.DateField(null=True)

    class Meta:
        ordering = ['requesting_member', '-request_date']

    def save(self, *args, **kwargs):
        if not self.id:  # is a new instance.
            self.request_date = timezone.now()
        # run base save method.
        # send message to notify requested_mentor
            sender = self.requesting_member
            recipient = self.requested_mentor
            subject = "Mentor Request from {0}".format(sender)
            message = self.request_message
            sent_request = MFMessage(sender=sender,
                                     recipient=recipient,
                                     date_sent=timezone.now(),
                                     subject=subject,
                                     content=message,
                                     )
            sent_request.save()
        super(MentorshipRequest, self).save(*args, **kwargs)


    def accept_request(self):
        # create and save Mentorship instance
        mentoree = self.requesting_member
        mentor = self.requested_mentor
        date_started = timezone.now()
        mentorship = Mentorship(mentoree=mentoree,
                                mentor=mentor,
                                date_started=date_started,
                                )
        mentorship.save()
        self.accepted_date = timezone.now()
        # send message back to
        msg = """
This notice is to inform you that {0} has accepted your mentorship request.

Contact your mentor to exchange contact information.

Sicnerely,

The MentorFinder Team
"""
        params = {'subject': "Your mentorship request has been accepted!",
                  'content': msg,
                  'sender': mentor,
                  'recipient': mentoree,
                  'date_sent': timezone.now()
                  }
        message = MFMessage(**params)
        message.save()







