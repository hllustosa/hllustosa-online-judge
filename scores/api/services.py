import json
from django.db import models
from django.utils import timezone
from .models import Score


def score_update(message):
    print('processing message:')
    print(message)
    message = json.loads(message)
    try:
        score = Score.objects.get(user_id=message['user_id'])
    except Score.DoesNotExist:
        score = Score()
        score.create(message['user_id'])

    problem_id = message['problem_id']
    status = message['progress']

    if status == 'Pending' or status == 'Running':
        return

    tried = score.tried_list
    if problem_id not in tried:
        tried.append(problem_id)
        score.tried_list = tried

    if status == 'Success':
        resolved = score.resolved_list
        if problem_id not in resolved:
            resolved.append(problem_id)
            score.resolved_list = resolved

    score.save()
