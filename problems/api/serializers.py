from rest_framework import serializers
from api.models import Problem, Run


class ProblemRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Problem
        fields = ('title', 'description', 'input', 'output')

class ProblemResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Problem
        fields = ('id', 'setter', 'title', 'description', 'input', 'output')

class RunRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Run
        fields = ('problem', 'code')

class RunResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Run
        fields = ('id', 'user_id', 'problem', 'code')