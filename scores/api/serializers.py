from rest_framework import serializers
from .models import Score


class ScoreResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Score
        fields = ('id', 'user_id', 'resolved_count',
                  'resolved_list', 'tried_count', 'tried_list')
