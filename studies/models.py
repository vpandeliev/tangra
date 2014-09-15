from django.db import models
from django.contrib.auth.models import User

def get_current_stage(study, user):
	"""	Returns the current Stage object for the supplied user and study. """
	current_stages = UserStage.objects.filter(group_stage__stage__study=study, user=user, status=1)
	if len(current_stages) > 0:
		return current_stages[0]
	else:
		return None

class Study(models.Model):
	"""	A Study contains all of the general data associated with a study. """
	name = models.CharField('Study Name', max_length=300)
	description = models.CharField('Description', max_length=5000)
	consent = models.CharField('Informed Consent Form', max_length=5000)
	instructions = models.CharField('Study Instructions', max_length=5000)
	eligibility = models.CharField('Eligibility Criteria', max_length=5000)
	reward = models.CharField('Compensation and Reward', max_length=5000)
	
	start_date = models.DateField('Starting date', blank=True, null=True)
	end_date = models.DateField('End date', blank=True, null=True)
	started = models.BooleanField('Started', default=False)

	investigators = models.ManyToManyField(User, related_name='investigators')

	def __unicode__(self):
		return u'%s' % (self.name)


class Stage(models.Model):
	"""	A Stage contains all of the general data associated with a stage.
	Once researchers create a Study they can create stages that users/groups
	will have to complete (in a particular order). """
	study = models.ForeignKey(Study)
	name = models.CharField('Stage Name', max_length=300)
	description = models.CharField('Stage Description', max_length=5000)
	instructions = models.CharField('Stage Instructions', max_length=5000)
	deadline = models.IntegerField('Time to finish session (in days)')
	url = models.CharField('Stage URL', max_length=300)

	def __unicode__(self):
		return unicode("%s: %s" % (self.study.name, self.name))


class Group(models.Model):
	"""	A Group contains a list of users contained within the group. It also
	has a list of stages (stored as GroupStage entries) that the users of 
	the group will have to complete. """
	name = models.CharField('Group name', max_length=300)
	study = models.ForeignKey(Study)
	users = models.ManyToManyField(User, related_name='users')
	stages = models.ManyToManyField(Stage, through='GroupStage')

	def __unicode__(self):
		return unicode("%s" % (self.name))


class GroupStage(models.Model):
	"""	A GroupStage object contains additional Stage data shared by a Group."""
	group = models.ForeignKey(Group)
	stage = models.ForeignKey(Stage)
	order = models.PositiveIntegerField()

	def __unicode__(self):
		return unicode("Group: %s | Stage: %s" % (self.group.name, self.stage.name))


class UserStage(models.Model):
	"""	A UserStage contains additional Stage data specific to an individual 
	participant. """
	user = models.ForeignKey(User)
	group_stage = models.ForeignKey(GroupStage)

	CHOICES = ((0, 'Completed'), (1, 'Active'), (2, 'Future'))
	status = models.IntegerField(max_length=1, choices=CHOICES)

	# The date and time this stage can become available
	available = models.DateTimeField(blank=True, null=True)

	# The dates the user started and finished this stage
	start_date = models.DateTimeField(blank=True, null=True)
	end_date = models.DateTimeField(blank=True, null=True)

	def __unicode__(self):
		return unicode("User: %s | Stage: %s (%s)" % 
			(self.user, self.group_stage.stage.name, UserStage.CHOICES[self.status][1]))


class Data(models.Model):
	"""	Data contains all of the data collected from the Study. """
	user = models.ForeignKey(User)
	user_stage = models.ForeignKey(UserStage)
	timestamp = models.DateTimeField()
	datum = models.TextField()
