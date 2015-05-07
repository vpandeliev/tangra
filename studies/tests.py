from django.test import TestCase
from models import *
from django.utils import timezone
import datetime
from django.test.client import Client
from django.core.urlresolvers import reverse


class StudyBuilder:
	"""	Helper class for creating a study. """

	@staticmethod
	def create_study():
		"""	Return a study with dummy data. """
		return Study.objects.create(
			name = "Test study",
			description = "Sample study",
			consent = "Sample consent",
			instructions = "Sample instructions",
			eligibility = "Sample eligibility",
			reward = "Sample reward",
		)

	@staticmethod
	def create_stage(study, deadline=None):
		"""	Return a stage with dummy data.
			The stage can include a deadline (in days). """
		return Stage.objects.create (
			study = study,
			name = "Stage",
			description = "Sample stage",
			instructions = "Sample instructions",
			deadline = deadline,
			url = "www.taglab.ca",
		)

	@staticmethod
	def create_participant(username, email, password):
		""" Return a user with the provided 'username', 'email', and 'password'. """
		return User.objects.create_user(
			username, 
			email, 
			password,
		)

	@staticmethod
	def create_group(study, participant):
		"""	Return a group containing the 'participant'. """
		group = Group.objects.create(
			name = "Group",
			study = study,
		)
		group.users.add(participant)
		group.save()
		return group

	@staticmethod
	def create_group_stage(group, stage, order):
		"""	Return a group stage for the 'group' and 'stage', in the specified 'order'. """
		return GroupStage.objects.create(
			group = group,
			stage = stage,
			order = order,
		)

	@staticmethod
	def create_user_stage(participant, group_stage, status):
		"""	Create a user stage for the specified 'participant' and 'group_stage'.
			Status can be 0:completed, 1:active, 2:future. """
		return UserStage.objects.create(
			user = participant,
			group_stage = group_stage,
			status = status,
		)

class UserStageTests(TestCase):

	def test_get_deadline(self):
		""" Test get_deadline() with Stage deadline. """
		# Create a study containing a group of 1 participant
		study = StudyBuilder.create_study()
		participant = StudyBuilder.create_participant("participant", "part@taglab.ca", "asdf")
		group = StudyBuilder.create_group(study, participant)

		# Create a stage with a deadline
		deadline_in_days = 2
		stage = StudyBuilder.create_stage(study, deadline_in_days)
		group_stage = StudyBuilder.create_group_stage(group, stage, 1)

		start_date = timezone.now()
		user_stage = UserStage.objects.create(
			user = participant,
			group_stage = group_stage,
			status = 1,					# active stage
			start_date = start_date		# now
		)

		# The returned deadline should start_date + deadline_in_days
		self.assertEqual(
			start_date + datetime.timedelta(days=deadline_in_days),
			user_stage.get_deadline()
		)

	def test_get_deadline_with_no_deadline(self):
		""" Test get_deadline() with no Stage deadline. """
		# Create a study containing a group of 1 participant
		study = StudyBuilder.create_study()
		participant = StudyBuilder.create_participant("participant", "part@taglab.ca", "asdf")
		group = StudyBuilder.create_group(study, participant)

		# Create a stage with no deadline
		stage = StudyBuilder.create_stage(study)	# no deadline added
		group_stage = StudyBuilder.create_group_stage(group, stage, 1)

		start_date = timezone.now()
		user_stage = UserStage.objects.create(
			user = participant,
			group_stage = group_stage,
			status = 1,					# active stage
			start_date = start_date		# now
		)

		# There should be no returned deadline for this stage
		self.assertEqual(None, user_stage.get_deadline())

	def test_get_deadline_with_future_stage(self):
		""" Test get_deadline() when the stage hasn't started yet. """
		# Create a study containing a group of 1 participant
		study = StudyBuilder.create_study()
		participant = StudyBuilder.create_participant("participant", "part@taglab.ca", "asdf")
		group = StudyBuilder.create_group(study, participant)

		# Create a stage with a deadline
		deadline_in_days = 2
		stage = StudyBuilder.create_stage(study, deadline_in_days)
		group_stage = StudyBuilder.create_group_stage(group, stage, 1)

		# Create the future user stage
		user_stage = UserStage.objects.create(
			user = participant,
			group_stage = group_stage,
			status = 2,					# future stage, no start_date
		)

		# There should be no set deadline yet
		self.assertEqual(None, user_stage.get_deadline())

	def test_is_overdue_with_past_deadline(self):
		"""	Test is_overdue() with an active stage and deadline that has passed. """
		# Create a study containing a group of 1 participant
		study = StudyBuilder.create_study()
		participant = StudyBuilder.create_participant("participant", "part@taglab.ca", "asdf")
		group = StudyBuilder.create_group(study, participant)

		# Create a stage with a deadline
		deadline_in_days = 2
		stage = StudyBuilder.create_stage(study, deadline_in_days)
		group_stage = StudyBuilder.create_group_stage(group, stage, 1)

		# Make the start_date happen in the past
		start_date = timezone.now() - datetime.timedelta(days=deadline_in_days)
		user_stage = UserStage.objects.create(
			user = participant,
			group_stage = group_stage,
			status = 1,					# active stage
			start_date = start_date		# deadline_in_days ago
		)

		# Deadline should have passed and is overdue
		self.assertTrue(timezone.now() > user_stage.get_deadline())
		self.assertTrue(user_stage.is_overdue())

	def test_is_overdue_with_future_deadline(self):
		"""	Test is_overdue() with an active stage and a future deadline. """
		# Create a study containing a group of 1 participant
		study = StudyBuilder.create_study()
		participant = StudyBuilder.create_participant("participant", "part@taglab.ca", "asdf")
		group = StudyBuilder.create_group(study, participant)

		# Create a stage with a deadline
		deadline_in_days = 2
		stage = StudyBuilder.create_stage(study, deadline_in_days)
		group_stage = StudyBuilder.create_group_stage(group, stage, 1)

		start_date = timezone.now()	
		user_stage = UserStage.objects.create(
			user = participant,
			group_stage = group_stage,
			status = 1,					# active stage
			start_date = start_date		# now
		)

		# The deadline should be in the future and is not overdue
		self.assertTrue(timezone.now() <= user_stage.get_deadline())
		self.assertFalse(user_stage.is_overdue())

	def test_is_overdue_with_unstarted_stage(self):
		"""	Test is_overdue() with a stage that has not been started yet. """
		# Create a study containing a group of 1 participant
		study = StudyBuilder.create_study()
		participant = StudyBuilder.create_participant("participant", "part@taglab.ca", "asdf")
		group = StudyBuilder.create_group(study, participant)

		# Create a stage with a deadline
		deadline_in_days = 2
		stage = StudyBuilder.create_stage(study, deadline_in_days)
		group_stage = StudyBuilder.create_group_stage(group, stage, 1)

		user_stage = UserStage.objects.create(
			user = participant,
			group_stage = group_stage,
			status = 2,					# future stage, no start_date
		)

		# There is no deadline set yet so it is not overdue
		self.assertFalse(user_stage.is_overdue())

	def test_is_overdue_with_completed_stage(self):
		"""	Test is_overdue() with a stage that has already been completed. """
		# Create a study containing a group of 1 participant
		study = StudyBuilder.create_study()
		participant = StudyBuilder.create_participant("participant", "part@taglab.ca", "asdf")
		group = StudyBuilder.create_group(study, participant)

		# Create a completed stage with a deadline
		deadline_in_days = 2
		stage = StudyBuilder.create_stage(study, deadline_in_days)
		group_stage = StudyBuilder.create_group_stage(group, stage, 1)

		user_stage = UserStage.objects.create(
			user = participant,
			group_stage = group_stage,
			status = 0,					# completed stage
			start_date = timezone.now() - datetime.timedelta(days=deadline_in_days + 5),
			end_date = timezone.now()
		)

		# The stage should not be overdue because it has been completed
		self.assertFalse(user_stage.is_overdue())

	def test_get_active_stages(self):
		pass

class ShowActiveStudiesTests(TestCase):

	def test_with_no_studies(self):
		"""	Test views.show_active_studies() with no existing studies. """
		client = Client()

		# Create a participant and log them in
		participant = StudyBuilder.create_participant("participant", "part@taglab.ca", "asdf")
		self.assertTrue(client.login(username='participant', password='asdf'))

		# Go to the page and make sure there are no studies
		response = client.get(reverse('studies:active_studies'))
		self.assertEqual(200, response.status_code)
		self.assertEqual(0, len(response.context['current_stages']))
		

	def test_with_no_started_study(self):
		"""	Test views.show_active_studies() with a study that hasn't started yet. """
		client = Client()

		# Create a participant and study (with no start date)
		# - Give participant an active stage
		study = StudyBuilder.create_study()
		participant = StudyBuilder.create_participant("participant", "part@taglab.ca", "asdf")
		group = StudyBuilder.create_group(study, participant)
		stage = StudyBuilder.create_stage(study)
		group_stage = StudyBuilder.create_group_stage(group, stage, 1)
		user_stage = UserStage.objects.create(
			user = participant,
			group_stage = group_stage,
			status = 1,					# active stage
		)

		# Log the participant into Tangra
		self.assertTrue(client.login(username='participant', password='asdf'))

		# Go to the page and make sure there are no studies
		response = client.get(reverse('studies:active_studies'))
		self.assertEqual(200, response.status_code)
		self.assertEqual(0, len(response.context['current_stages']))

		# Edit the study to have a future start date
		study.start_date = timezone.now() + datetime.timedelta(days=2)
		study.save()

		# Go to the page and make sure there are no studies
		response = client.get(reverse('studies:active_studies'))
		self.assertEqual(200, response.status_code)
		self.assertEqual(0, len(response.context['current_stages']))

	def test_with_ended_study(self):
		""" Test views.show_active_studies() with a study that has ended. """
		client = Client()

		# Create a participant and a study (with a past end date)
		# - Give participant an active stage
		study = StudyBuilder.create_study()
		study.start_date = timezone.now() - datetime.timedelta(days=3) # started 3 days ago
		study.end_date = timezone.now() - datetime.timedelta(days=1) # ended 1 day ago
		study.save()
		participant = StudyBuilder.create_participant("participant", "part@taglab.ca", "asdf")
		group = StudyBuilder.create_group(study, participant)
		stage = StudyBuilder.create_stage(study)
		group_stage = StudyBuilder.create_group_stage(group, stage, 1)
		user_stage = UserStage.objects.create(
			user = participant,
			group_stage = group_stage,
			status = 1,					# active stage
		)

		# Log the participant into Tangra
		self.assertTrue(client.login(username='participant', password='asdf'))

		# Go to the page and make sure there are no studies
		response = client.get(reverse('studies:active_studies'))
		self.assertEqual(200, response.status_code)
		self.assertEqual(0, len(response.context['current_stages']))

	def test_with_no_active_stages(self):
		"""	Test views.show_active_studies() with a study that has no active stages. """
		client = Client()

		# Create a participant and a study with all future stages
		study = StudyBuilder.create_study()
		study.start_date = timezone.now() - datetime.timedelta(days=3) # started 3 days ago
		study.save()
		participant = StudyBuilder.create_participant("participant", "part@taglab.ca", "asdf")
		group = StudyBuilder.create_group(study, participant)
		stage = StudyBuilder.create_stage(study)
		group_stage = StudyBuilder.create_group_stage(group, stage, 1)
		user_stage = UserStage.objects.create(
			user = participant,
			group_stage = group_stage,
			status = 2,					# future stage
		)

		# Log the participant into Tangra
		self.assertTrue(client.login(username='participant', password='asdf'))

		# Go to the page and make sure there are no studies
		response = client.get(reverse('studies:active_studies'))
		self.assertEqual(200, response.status_code)
		self.assertEqual(0, len(response.context['current_stages']))

		# Edit stages of the study to be all completed
		user_stage.status = 0
		user_stage.save()

		# Go to the page and make sure there are no studies
		response = client.get(reverse('studies:active_studies'))
		self.assertEqual(200, response.status_code)
		self.assertEqual(0, len(response.context['current_stages']))

	def test_with_one_active_study(self):
		"""	Test views.show_active_studies() with study that has one active stage. """
		client = Client()

		# Create a participant and a study with an active stage
		study = StudyBuilder.create_study()
		study.start_date = timezone.now() - datetime.timedelta(days=3) # started 3 days ago
		study.save()
		participant = StudyBuilder.create_participant("participant", "part@taglab.ca", "asdf")
		group = StudyBuilder.create_group(study, participant)
		stage = StudyBuilder.create_stage(study)
		group_stage = StudyBuilder.create_group_stage(group, stage, 1)
		user_stage = UserStage.objects.create(
			user = participant,
			group_stage = group_stage,
			status = 1,					# active stage
		)

		# Log the participant into Tangra
		self.assertTrue(client.login(username='participant', password='asdf'))

		# Go to the page and make sure there is a study
		response = client.get(reverse('studies:active_studies'))
		self.assertEqual(200, response.status_code)
		self.assertEqual(1, len(response.context['current_stages']))

	def test_with_one_active_study_and_overdue_stage(self):
		"""	Test views.show_active_studies() a study that has an overdue stage. """
		client = Client()

		# Create a participant and a study
		study = StudyBuilder.create_study()
		study.start_date = timezone.now() - datetime.timedelta(days=3) # started 3 days ago
		study.save()
		participant = StudyBuilder.create_participant("participant", "part@taglab.ca", "asdf")
		group = StudyBuilder.create_group(study, participant)

		# Create a stage with a deadline
		deadline_in_days = 2
		stage = StudyBuilder.create_stage(study, deadline_in_days)
		group_stage = StudyBuilder.create_group_stage(group, stage, 1)

		# Make the start_date happen in the past
		start_date = timezone.now() - datetime.timedelta(days=deadline_in_days)
		user_stage = UserStage.objects.create(
			user = participant,
			group_stage = group_stage,
			status = 1,					# active stage
			start_date = start_date		# deadline_in_days ago
		)

		# Log the participant into Tangra
		self.assertTrue(client.login(username='participant', password='asdf'))

		# Go to the page and make sure there is an overdue study
		# Note: use stage.is_overdue() to test
		response = client.get(reverse('studies:active_studies'))
		self.assertEqual(200, response.status_code)
		self.assertEqual(1, len(response.context['current_stages']))
		overdue_stage = response.context['current_stages'][0]
		self.assertTrue(overdue_stage.is_overdue())

	def test_with_multiple_active_studies(self):
		"""	Test views.show_active_studies() with multiple studies that have active stages. """
		client = Client()

		# Create a participant and two studies with active stages

		# Log the participant into Tangra

		# Go to the page and make sure there are two studies
		# - Note: does order matter?
		pass

class ShowStudyTests(TestCase):

	def test_stage_ordering(self):
		pass
