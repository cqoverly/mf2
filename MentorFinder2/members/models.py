from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.utils import timezone

from fields.models import Field
# from mf_messages.models import MFMessage
import mentorships.models
# from mentorships.models import MentorshipRequest, Mentorship


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
        year_ago = datetime.now() - timedelta(days=365)
        since_last = datetime.now() - self.last_login
        if since_last > year_ago:
            self.is_active = False

    def endorsed_by(self):
        endorsements = Endorsement.objects.filter(endorsee=self.id)
        member_endorsers = [e.endorser for e in endorsements]
        return member_endorsers

    def has_endorsed(self):
        endorsements = Endorsement.objects.filter(endorser=self.id)
        members_endorsed = [e.endorsee for e in endorsements]
        return members_endorsed

    def get_education(self):
        education = Education.objects.filter(member=self.id)
        return education

    def get_interests(self):
        interests = MemberField.objects.filter(member=self)
        interest_fields = [Field.objects.get(id=row.field.id)
                           for row in interests]
        return interest_fields

    def get_mentorships(self):
        mentorships_list = mentorships.models.Mentorship.objects.filter(mentoree=self)
        return mentorships_list

    def get_mentorship_requests(self):
        requested = mentorships.models.MentorshipRequest.objects.filter(requesting_member=self)
        requesting = mentorships.models.MentorshipRequest.objects.filter(requested_mentor=self)                                                          
        return (requesting, requested)

    # def check_messages(self):
    #     pass

    # def get_messages(self):
    #     pass

    def get_jobs(self):
        job_list = JobExperience.objects.filter(member=self)
        return 

    def create_profile(self):
        mr_requested, mr_requesting = self.get_mentorship_requests()
        params = {'member': self,
                'endorsed_by': self.endorsed_by(),
                'endorsed': self.has_endorsed(),
                'education': self.get_education(),
                'interests': self.get_interests(),
                'intro': self.intro,
                'status': self.is_active,
                'mr_requested': mr_requested,
                'mr_requesting': mr_requesting,
                'mentorships_list': self.get_mentorships(),
                'job_list': self.get_jobs()
                }
        return params


class Education(models.Model):
    choices = (('HS', 'High School'),
               ('UG', 'Undergraduate'),
               ('PG', 'Post-Graduate'),
               )
    member = models.ForeignKey(MFUser)
    ed_type = models.CharField('Level', max_length=20, choices=choices)
    year_completed = models.DateField('Completed')
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

    def add_job(self, *args, **kwargs):
        new_job = JobExperience(**kwargs)
        new_job.save()
        return True


class Endorsement(models.Model):
    endorsee = models.ForeignKey(MFUser,
                                 db_column='member',
                                 related_name='was_endorsed'
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

    def __unicode__(self):
            return "{0} is endorsed by {1}".format(self.endorsee, self.endorser)


class MemberField(models.Model):
    field = models.ForeignKey(Field)
    member = models.ForeignKey(MFUser)
    can_mentor = models.BooleanField(default=False)
    date_entered = models.DateField()

    class Meta:
        ordering = ['-date_entered']

    def __unicode__(self):
        return "{0}: {1}".format(self.member, self.field)

