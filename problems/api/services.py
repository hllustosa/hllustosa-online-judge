
import json
from django.utils import timezone
from .models import Run


def process_update(message):
    print('processing message:')
    print(message)
    message = json.loads(message)
    run = Run.objects.get(pk=message['run_id'])
    run.status = message['progress']

    if run.status not in ['pending', 'running']:
        run.finished_at = timezone.now()

    run.save()
