from django.test import TestCase
from api.models import Problem, Run


class ProblemTestCase(TestCase):

    def test_problem(self):

        self.assertEquals(
            Problem.objects.count(),
            0
        )

        Problem.objects.create(
            title='problem A', description='Test case problem', input='1\n', output='hello\n'
        )

        Problem.objects.create(
            title='problem B', description='Test case problem 2', input='12\n', output='world\n'
        )

        self.assertEquals(
            Problem.objects.count(),
            2
        )


class RunTestCase(TestCase):

    def test_run(self):

        self.assertEquals(
            Run.objects.count(),
            0
        )

        Problem.objects.create(
            title='run problem A', description='Test case problem', input='1\n', output='hello\n'
        )

        problem = Problem.objects.get(title__exact='run problem A')
        self.assertIsNotNone(problem)

        Run.objects.create(
            user_id='d4fe3679-9951-450b-a25b-f6e947946420', problem=problem, code="import django")

        self.assertEquals(
            Run.objects.count(),
            1
        )
