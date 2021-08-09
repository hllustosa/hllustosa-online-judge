from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid


class Problem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    setter = models.TextField(blank=False)
    title = models.TextField(blank=False)
    description = models.TextField(blank=False)
    input = models.TextField(blank=False)
    output = models.TextField(blank=False)
    timeout = models.IntegerField(blank=False, validators=[
                                  MinValueValidator(1), MaxValueValidator(100)])


class Run(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.TextField(blank=False)
    problem = models.ForeignKey(Problem, blank=False, on_delete=models.CASCADE)
    code = models.TextField(blank=False)
    status = models.TextField(blank=False)
    created_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
