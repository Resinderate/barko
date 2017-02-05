from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Task(models.Model):
	owner = models.ForeignKey(
		User,
		related_name="owner",
		on_delete=models.CASCADE
	)
	marked_complete_by = models.ForeignKey(
		User,
		related_name="marked_complete_by",
		on_delete=models.CASCADE,
		null=True
	)
	title = models.CharField(max_length=100)
	description = models.TextField()
	task_open = models.BooleanField(default=True)
	created_date = models.DateTimeField("date created")
	completed_date = models.DateTimeField("date completed", null=True)

	@classmethod
	def create(cls, owner, title, description):
		"""
		Utility method to fill in default values upon creation.
		"""
		return Task(
			owner=owner,
			marked_complete_by=None,
			title=title,
			description=description,
			task_open=True,
			created_date=timezone.now(),
			completed_date=None
		)

	def complete(self, completed_by):
		self.task_open = False
		self.marked_complete_by = completed_by
		self.completed_date = timezone.now()
		self.save()

	def uncomplete(self):
		self.task_open = True
		self.marked_complete_by = None
		self.completed_date = None
		self.save()

	def __str__(self):
		return self.title
