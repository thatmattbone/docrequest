"""
Integration tests.

We start up a webserver using each supported framework and issue the
same requests, hoping we get the responses we expect.
"""
import subprocess
import sys
import time
import unittest

import requests


class TestBase(object):

    MAX_TRIES = 10

    @classmethod
    def setUpClass(cls):
        cls.pid = subprocess.Popen([sys.executable] + cls.args,
                                   cwd=cls.cwd)

        for i in range(cls.MAX_TRIES):
            try:
                requests.get(cls.path)
                break
            except:
                print("sleep!")
                time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.pid.kill()
        cls.pid.wait()


    def test_decorated_without_definitions(self):
        response = requests.get(self.path + "/decorated-without-definitions")
        import pdb; pdb.set_trace()
        self.assertEqual("Hello World", response.text)


class DjangoIntegrationTest(unittest.TestCase, TestBase):

    path = "http://localhost:8000"
    args = ["manage.py", "runserver"]
    cwd = "../django_test_proj"


class PyramidIntegrationTest(unittest.TestCase, TestBase):

    path = "http://localhost:6543"
    args = ["pserve.py", "development.ini"]
    cwd = "../pyramid_test_proj"


if __name__ == "__main__":
    unittest.main()
