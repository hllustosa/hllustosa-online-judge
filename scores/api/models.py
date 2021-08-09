from django.db import models
import uuid
import json

class Score(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.TextField(blank=False)
    resolved = models.TextField(blank=False)
    resolved_count = models.IntegerField(blank=False)
    tried = models.TextField(blank=False)
    tried_count = models.IntegerField(blank=False)
    
    def create(self, user_id):
        self.user_id = user_id
        self.resolved = '[]'
        self.resolved_count = 0
        self.tried = '[]'
        self.tried_count = 0

    @property
    def resolved_list(self):
        return json.loads(self.resolved)

    @resolved_list.setter
    def resolved_list(self, value):
        self.resolved_count = len(value)
        self.resolved = json.dumps(value)

    @property
    def tried_list(self):
        return json.loads(self.tried)

    @tried_list.setter
    def tried_list(self, value):
        self.tried_count = len(value)
        self.tried = json.dumps(value)