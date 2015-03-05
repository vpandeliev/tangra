import os
from django.db import models
from django.conf import settings
from django.utils import timezone
import datetime
from django.db.models import Q

class Study(models.Model):
	"""	A Study contains all of the general data associated with a study. """
	
	name = models.CharField('Study Name', max_length=300)
	api_name = models.CharField('API Name', max_length=300) 
	description = models.CharField('Description', max_length=5000, blank=True, null=True)
	consent = models.CharField('Informed Consent Form', max_length=5000, blank=True, null=True)
	instructions = models.CharField('Study Instructions', max_length=5000, blank=True, null=True)
	eligibility = models.CharField('Eligibility Criteria', max_length=5000, blank=True, null=True)
	reward = models.CharField('Compensation and Reward', max_length=5000, blank=True, null=True)

	start_date = models.DateField('Starting date', blank=True, null=True)
	end_date = models.DateField('End date', blank=True, null=True)

	investigators = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='investigators')

	def __unicode__(self):
		return u'%s' % (self.name)

	def has_started(self):
		if self.start_date is not None and datetime.datetime.now().date() >= self.start_date:
			# The start date has already passed
			return True
		return False

	def has_ended(self):
		if self.end_date is not None and datetime.datetime.now().date() >= self.end_date:
			# The end date has already passed
			return True
		return False


class Stage(models.Model):
	"""	A Stage contains all of the general data associated with a stage.
	Once researchers create a Study they can create stages that users/groups
	will have to complete (in a particular order). """
	
	study = models.ForeignKey(Study)
	name = models.CharField('Stage Name', max_length=300)
	description = models.CharField('Stage Description', max_length=5000)
	instructions = models.CharField('Stage Instructions', max_length=5000)
	deadline = models.IntegerField('Time to finish session (in days)', blank=True, null=True)
	url = models.CharField('Stage URL', max_length=300)

	def __unicode__(self):
		return unicode("%s: %s" % (self.study.name, self.name))


class Group(models.Model):
	"""	A Group contains a list of users contained within the group. It also
	has a list of stages (stored as GroupStage entries) that the users of
	the group will have to complete. """
	
	name = models.CharField('Group name', max_length=300)
	study = models.ForeignKey(Study)
	users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='users')
	stages = models.ManyToManyField(Stage, through='GroupStage')

	def __unicode__(self):
		return unicode("%s" % (self.name))


class GroupStage(models.Model):
	"""	A GroupStage object contains additional Stage data shared by a Group."""
	
	group = models.ForeignKey(Group)
	stage = models.ForeignKey(Stage)
	order = models.PositiveIntegerField()

	def __unicode__(self):
		return unicode("Group: %s | Stage: %s (%s)" % (self.group.name, self.stage.name, self.order))


class UserStage(models.Model):
	"""	A UserStage contains additional Stage data specific to an individual
	participant. """
	
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	group_stage = models.ForeignKey(GroupStage)
	

	CHOICES = ((0, 'Completed'), (1, 'Active'), (2, 'Future'))
	status = models.IntegerField(max_length=1, choices=CHOICES, default=2)

	# The date and time this stage can become available
	available = models.DateTimeField(blank=True, null=True, default=timezone.now())

	# The dates the user started and finished this stage
	start_date = models.DateTimeField(blank=True, null=True)
	end_date = models.DateTimeField(blank=True, null=True)
	
	def __unicode__(self):
		return unicode("User: %s | Stage: %s (%s)" %
			(self.user, self.group_stage.stage.name, UserStage.CHOICES[self.status][1]))


	def get_deadline(self):
		"""	Return the date/time of the deadline for this stage.
			Return None if there is no deadline for this stage.  """
		if self.start_date is None:
			# The stage hasn't been started yet: no deadline
			return None

		if self.group_stage.stage.deadline is None:
			# This stage has no deadline associated with it
			return None

		# Compute the deadline for this stage
		days_to_complete_stage = datetime.timedelta(days=self.group_stage.stage.deadline)
		return self.start_date + days_to_complete_stage


	def is_overdue(self):
		"""	Return True if this stage is overdue, False otherwise. """
		deadline = self.get_deadline()

		if deadline is None:
			# No deadline has been set for this stage
			return False

		if self.status == 0:
			# The stage has already been completed
			return False

		return timezone.now() > deadline
	
	def is_available(self):
		""" Return True if the stage is available. Otherwise, False."""
		
		return self.available == None or timezone.now() >= self.available
		
	def complete_stage(self):
		""" Complete the user stage. """
		self.status = 0
		self.end_date = timezone.now()
		self.save()


	def start_stage(self):
		""" Start the user stage. """
		self.status = 1
		self.start_date = timezone.now()
		self.save()
		
	def save(self, *args, **kwargs):
		if not self.pk:
			if self.group_stage.order == 0:
				self.status = 1
		super(UserStage, self).save(*args, **kwargs)


	@staticmethod
	def get_active_stages(user, study=None):
		""" Get the active stages for the specified 'user' and 'study'.
			An active stage is defined as a stage that has been started but not ended. """
		active_stages = UserStage.objects.filter(user=user, status=1)

		# Studies should be started
		start_date_exists = Q(group_stage__stage__study__start_date__isnull=False)
		start_date_in_past = Q(group_stage__stage__study__start_date__lte=timezone.now())
		active_stages = active_stages.filter(start_date_exists & start_date_in_past)

		# Studies should not have ended
		end_date_does_not_exist = Q(group_stage__stage__study__end_date__isnull=True)
		end_date_is_in_future = Q(group_stage__stage__study__end_date__gt=timezone.now())
		active_stages = active_stages.filter(end_date_does_not_exist | end_date_is_in_future)

		if study is not None:
			active_stages = active_stages.filter(group_stage__stage__study=study)

		return active_stages


def get_next_user_stage(user, study):
	""" Get the next user stage. """
	
	us = UserStage.objects.filter(user=user, group_stage__stage__study=study).order_by('group_stage__order')
	
	for s in us.all():
		if s.status != 0:
			return s
		
	return None


class Data(models.Model):
	"""	Data table contains all of the data collected from the Study. """
	# user: the author of the data (most commonly the participant)
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	user_stage = models.ForeignKey(UserStage)
	timestamp = models.DateTimeField(auto_now=True)
	datum = models.TextField(null=True, blank=True)
	attachment = models.FileField(null=True, blank=True)

	def __unicode__(self):
		return unicode("Data: %s" % (self.datum))

	def filename(self):
		if self.attachment is not None:
			return os.path.basename(self.attachment.url)


class Note(models.Model):
	""" Note table contains all of the notes collected from the Study. """
	# user: author of the note (this is most likely be the investigator)
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	timestamp = models.DateTimeField(auto_now=True)
	datum = models.TextField(null=True, blank=True)
	attachment = models.FileField(null=True, blank=True)
	study = models.ForeignKey(Study)

	# What notes can be associated with
	#participant = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
	stage = models.ForeignKey(Stage, blank=True, null=True)
	group = models.ForeignKey(Group, blank=True, null=True)
	group_stage = models.ForeignKey(GroupStage, blank=True, null=True)
	user_stage = models.ForeignKey(UserStage, blank=True, null=True)

	# If this note was sent as an email to investigators
	email = models.BooleanField(default=False)

	def __unicode__(self):
		return unicode("Note: %s" % (self.datum))

	def filename(self):
		if self.attachment is not None:
			return os.path.basename(self.attachment.url)
