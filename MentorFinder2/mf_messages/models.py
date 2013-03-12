from django.db import models

from members.models import MFUser

class MFMessage(models.Model):
    sender = models.ForeignKey(MFUser, related_name='from')
    recipient = models.ForeignKey(MFUser, related_name='to')
    date_sent = models.DateTimeField()
    subject = models.CharField(max_length=120)
    content = models.TextField(max_length=10000)
    read = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_sent', 'sender', 'recipient', 'subject']

    def __unicode__(self):
        return "From: {0} -- To: {1} -- Date: {2}".format(self.sender,
                                                          self.recipient,
                                                          self.date_sent,
                                                          )


