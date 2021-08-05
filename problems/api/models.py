from django.db import models
import uuid

# Create your models here.


class Problem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    setter = models.UUIDField(default=uuid.uuid4)
    title = models.TextField(blank=False)
    description = models.TextField(blank=False)
    input = models.TextField(blank=False)
    output = models.TextField(blank=False)


class Run(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.TextField(blank=False)
    problem = models.ForeignKey(Problem, blank=False, on_delete=models.CASCADE)
    code = models.TextField(blank=False)
