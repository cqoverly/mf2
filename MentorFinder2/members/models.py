from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser




class MFUser(AbstractUser):
    date_modified = models.DateTimeField(null=True)
    intro = models.TextField('Introduction', max_length=6000, default='')
    is_mentor = models.BooleanField('Is a mentor?', default=False)
    is_mentoree = models.BooleanField('Has a mentor?', default=False)
    profile_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = "Member"
        verbose_name_plural = "Members"

    def __unicode__(self):
        name = self.username  # default
        if self.first_name and self.last_name:
            name = " ".join((self.first_name, self.last_name))
        elif self.first_name:
            name = self.first_name
        elif self.last_name:
            name = self.last_name
        return "{0}".format(name)

    def check_active(self):
        year_ago = datetime.now() - timedelta(years=1)
        since_last = datetime.now() - self.last_login
        if since_last > year_ago:
            self.is_active = False

    def endorsed_by(self):
        pass

    def endorsed(self):
        pass


class Education(models.Model):
    member = models.ForeignKey(MFUser)
    ed_type = models.CharField('Level', max_length=20)
    year_completed = models.DateTimeField('Completed')
    focus1 = models.CharField(max_length=32, default='')
    focus2 = models.CharField(max_length=32, default='')

    class Meta:
        ordering = ['-year_completed', 'member']
        verbose_name = 'Education'
        verbose_name_plural = 'Education'


class JobExperience(models.Model):
    member = models.ForeignKey(MFUser)
    start_date = models.DateField()
    end_date = models.DateField()
    company = models.CharField(max_length=40)
    job_summary = models.TextField(max_length=600, default='')

    class Meta:
        ordering = ['-end_date', 'member']
        verbose_name = 'Job Experience'
        verbose_name_plural = 'Job Experience'


class Endorsement(models.Model):
    endorsee = models.ForeignKey(MFUser,
                                 db_column='member',
                                 related_name='was_endoresed'
                                 )
    endorser = models.ForeignKey(MFUser,
                                 db_column='endorsed_by',
                                 related_name='endorsed'
                                 )
    date_made = models.DateField()
    reason = models.CharField('Reason for endorsement',
                              max_length=600,
                              default=''
                              )

    class Meta:
        ordering = ['-date_made', 'endorsee']
        verbose_name = 'Endorsement'
        verbose_name_plural = 'Endorsements'




