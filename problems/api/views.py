from django.shortcuts import render

from django.http.response import JsonResponse
from django.core.paginator import Paginator
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.utils import timezone

from api.utils import JWTAuthentication
from api.models import Problem, Run
from api.utils import IsAuthenticatedWith, method_permission_classes, ANY, TEACHER
from api.serializers import ProblemRequestSerializer, ProblemResponseSerializer, RunRequestSerializer, RunResponseSerializer
from .bus import Bus

from rest_framework.views import APIView


class ProblemsListView(APIView):

    @method_permission_classes((IsAuthenticatedWith(ANY),))
    def get(self, request):
        problems = Problem.objects.all().order_by('id')

        title = request.query_params.get('title', None)
        page = request.query_params.get('page', 1)
        pageSize = request.query_params.get('pageSize', 10)

        if title is not None:
            problems = problems.filter(title__icontains=title)

        count = problems.count()
        paginator = Paginator(problems, pageSize)

        problems_serializer = ProblemResponseSerializer(
            paginator.page(page), many=True)
        return JsonResponse({'items': problems_serializer.data, 'count': count}, safe=False)

    @method_permission_classes((IsAuthenticatedWith(TEACHER),))
    def post(self, request):

        auth = JWTAuthentication()
        user_id = auth.get_user_id(request)

        problem_data = JSONParser().parse(request)
        problems_serializer = ProblemRequestSerializer(data=problem_data)

        if problems_serializer.is_valid():
            problem = problems_serializer.create(
                problems_serializer.validated_data)
            problem.setter = user_id
            problem.save()

            return JsonResponse(ProblemResponseSerializer(problem).data, status=status.HTTP_201_CREATED)

        return JsonResponse(problems_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProblemsDetailsView(APIView):

    @property
    def not_found():
        return JsonResponse({'message': 'The problem does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def get_problem(self, pk):
        try:
            problem = Problem.objects.get(pk=pk)
            return problem
        except Problem.DoesNotExist:
            return None

    @method_permission_classes((IsAuthenticatedWith(ANY),))
    def get(self, request, pk):
        problem = self.get_problem(pk)

        if problem == None:
            return self.not_found()

        problem_serializer = ProblemResponseSerializer(problem)
        return JsonResponse(problem_serializer.data)

    @method_permission_classes((IsAuthenticatedWith(TEACHER),))
    def put(self, request, pk):
        problem = self.get_problem(pk)

        if problem == None:
            return self.not_found()

        problem_data = JSONParser().parse(request)
        problem_serializer = ProblemResponseSerializer(
            problem, data=problem_data)

        if problem_serializer.is_valid():
            problem_serializer.save()
            return JsonResponse(problem_serializer.data)

        return JsonResponse(problem_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_permission_classes((IsAuthenticatedWith(TEACHER),))
    def delete(self, request, pk):
        problem = self.get_problem(pk)

        if problem == None:
            return self.not_found()

        problem.delete()
        return JsonResponse({'message': 'Problem was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


class RunsListView(APIView):

    @method_permission_classes((IsAuthenticatedWith(ANY),))
    def get(self, request):

        auth = JWTAuthentication()
        user_id = auth.get_user_id(request)

        runs = Run.objects.filter(user_id=user_id).order_by('id')
        page = request.query_params.get('page', 1)
        pageSize = request.query_params.get('pageSize', 10)

        count = runs.count()
        paginator = Paginator(runs, pageSize)

        runs_serializer = RunResponseSerializer(
            paginator.page(page), many=True)
        return JsonResponse({'items': runs_serializer.data, 'count': count}, safe=False)

    @method_permission_classes((IsAuthenticatedWith(ANY),))
    def post(self, request):

        auth = JWTAuthentication()
        user_id = auth.get_user_id(request)

        run_data = JSONParser().parse(request)
        runs_serializer = RunRequestSerializer(data=run_data)

        if runs_serializer.is_valid():
            run = runs_serializer.create(runs_serializer.validated_data)
            run.user_id = user_id
            run.status = 'pending'
            run.created_at = timezone.now()
            run.save()

            run = Run.objects.select_related('problem').get(pk=run.id)
            run = RunResponseSerializer(run).data
            bus = Bus()
            bus.send_run(run)

            return JsonResponse(run, status=status.HTTP_201_CREATED)

        return JsonResponse(runs_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RunsAllListView(APIView):

    @method_permission_classes((IsAuthenticatedWith(TEACHER),))
    def get(self, request):

        runs = Run.objects.all().order_by('id')
        page = request.query_params.get('page', 1)
        pageSize = request.query_params.get('pageSize', 10)

        count = runs.count()
        paginator = Paginator(runs, pageSize)

        runs_serializer = RunResponseSerializer(
            paginator.page(page), many=True)
        return JsonResponse({'items': runs_serializer.data, 'count': count}, safe=False)


class RunsDetailsView(APIView):

    @property
    def not_found():
        return JsonResponse({'message': 'The run does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def get_run(self, pk):
        try:
            run = Run.objects.get(pk=pk)
            return run
        except Problem.DoesNotExist:
            return None

    @method_permission_classes((IsAuthenticatedWith(ANY),))
    def get(self, request, pk):
        run = self.get_run(pk)

        if run == None:
            return self.not_found()

        auth = JWTAuthentication()
        user_id = auth.get_user_id(request)

        if run.user_id != user_id and run.problem.setter != user_id:
            return JsonResponse({'message': 'You don\'t have permission to access this run '}, status=status.HTTP_403_FORBIDDEN)

        serializer = RunResponseSerializer(run)
        return JsonResponse(serializer.data)

    @method_permission_classes((IsAuthenticatedWith(TEACHER),))
    def delete(self, request, pk):
        run = self.get_run(pk)

        if run == None:
            return self.not_found()

        run.delete()
        return JsonResponse({'message': 'Run was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
