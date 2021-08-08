import unittest
from runner.runner import execute
import json

class MockBus():

    def __init__(self, test, expected):
        self.test = test
        self.expected = expected
        self.position = 0

    def send_notification(self, notification):

        if notification == 'Server Error':
            return

        self.test.assertEqual(notification['progress'], self.expected[self.position])
        self.position = self.position + 1


class TestRunner(unittest.TestCase):

    def test_right_run(self):
        message = """
        {
            "id": "1bd23e5f-6829-4ff8-9f56-982d144ef0a9",
            "user_id": "1",
            "problem": {
                "id": "221cf9b7-f24f-497c-8b50-c1f5cb36a151",
                "setter": "00000000-0000-0000-0000-000000000001",
                "title": "problem a2",
                "description": "teste",
                "input": "1 2\\n2 4\\n3 5\\n4 6",
                "output": "3\\n6\\n8\\n10",
                "timeout": 100
            },
            "code": "while True:\\n        try:\\n            [v1, v2] = [int(val) for val in input().split() ]\\n            print(\\"%d\\" % (v1 + v2))\\n        except EOFError:\\n            break",
            "status": "pending"
        }
        """

        bus = MockBus(self, ["Running", "Success"])
        execute(json.loads(message), bus)

    def test_0_run(self):
        message = """
        {
            "id": "1bd23e5f-6829-4ff8-9f56-982d144ef0a9",
            "user_id": "1",
            "problem": {
                "id": "221cf9b7-f24f-497c-8b50-c1f5cb36a151",
                "setter": "00000000-0000-0000-0000-000000000001",
                "title": "problem a2",
                "description": "teste",
                "input": "1 2\\n2 4\\n3 5\\n4 6",
                "output": "3\\n6\\n8\\n10",
                "timeout": 100
            },
            "code": "while True:\\n        try:\\n            [v1, v2] = [int(val) for val in input().split() ]\\n            print(\\"%d\\" % (v1 + v2 + 5))\\n        except EOFError:\\n            break",
            "status": "pending"
        }
        """

        bus = MockBus(self, ["Running", "Wrong Answer(0.0%)"])
        execute(json.loads(message), bus)

    def test_runtime_run(self):
        message = """
        {
            "id": "1bd23e5f-6829-4ff8-9f56-982d144ef0a9",
            "user_id": "1",
            "problem": {
                "id": "221cf9b7-f24f-497c-8b50-c1f5cb36a151",
                "setter": "00000000-0000-0000-0000-000000000001",
                "title": "problem a2",
                "description": "teste",
                "input": "1 2\\n2 4\\n3 5\\n4 6",
                "output": "3\\n6\\n8\\n10",
                "timeout": 100
            },
            "code": "while True:\\n        try:\\n            [v1, v2 = [int(val) for val in input().split() ]\\n            print(\\"%d\\" % (v1 + v2 + 5))\\n        except EOFError:\\n            break",
            "status": "pending"
        }
        """

        bus = MockBus(self, ["Running", "Runtime or Compilation Error"])
        execute(json.loads(message), bus)

    def test_timeout_run(self):
        message = """
        {
            "id": "1bd23e5f-6829-4ff8-9f56-982d144ef0a9",
            "user_id": "1",
            "problem": {
                "id": "221cf9b7-f24f-497c-8b50-c1f5cb36a151",
                "setter": "00000000-0000-0000-0000-000000000001",
                "title": "problem a2",
                "description": "teste",
                "input": "1 2\\n2 4\\n3 5\\n4 6",
                "output": "3\\n6\\n8\\n10",
                "timeout": 1
            },
            "code": "while True:\\n        continue",
            "status": "pending"
        }
        """

        bus = MockBus(self, ["Running", "Wrong Answer(0.0%)"])
        execute(json.loads(message), bus)

if __name__ == '__main__':
    unittest.main()
