from django.db import models
import uuid

# Create your models here.

# A Revision represents a state of the schedule - i.e. the set of all visits in the schedule at a point
# A Visit rpresents a visit that was entered into the schedule

# There is a many-to-many relationship between Revisions and Visits. A matching between a revision R and a visit V means that the visit V exists/existed in iteration R of the schedule

class Revision(models.Model):
	create_date_time = 	create_date_time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.id)
    
# Represents a visit that was entered into the schedule
class Visit(models.Model):
	create_date_time = models.DateTimeField(auto_now_add=True)
	public_id = models.UUIDField(default=uuid.uuid4) # Generated name for users to use in URLs
	revisions = models.ManyToManyField(Revision, blank=False)
	start_date_time = models.DateTimeField(null=False, blank=False)
	end_date_time = models.DateTimeField(null=False, blank=False)
	client = models.IntegerField(null=False, blank=False)
	carer = models.IntegerField(null=False, blank=False)

	def __str__(self):
		return str(self.public_id)
