"""
Integration tests.

We start up a webserver using each supported framework and issue the
same requests, hoping we get the responses we expect.
"""
import subprocess
import sys
import time
import unittest
import os

import requests


class TestBase(object):
    MAX_TRIES = 10

    @classmethod
    def setUpClass(cls):
        # fork off our framework's dev server
        cls.pid = subprocess.Popen([sys.executable] + cls.args,
                                   cwd=cls.cwd,
                                   stdout=sys.stdout,
                                   stderr=sys.stderr,
                                   )

        # try to request the root url MAX_TRIES times to make sure the dev server has started
        for i in range(cls.MAX_TRIES):
            try:
                requests.get(cls.path)
                break
            except requests.ConnectionError:
                # sleep if we can't make the connection yet
                time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.pid.terminate()
        cls.pid.wait()

    def response_funcs(self):

        def get_func(url, params={}):
            return requests.get(url, params=params)

        def post_func(url, params={}):
            return requests.post(url, data=params)

        yield get_func
        yield post_func

    def test_decorated_without_definitions(self):
        for response_func in self.response_funcs():
            response = response_func(self.path + "/decorated-without-definitions")
            self.assertEqual("Hello World", response.text)

    def test_simple_docrequest(self):
        for response_func in self.response_funcs():

            endpoint = self.path + "/simple-docrequest"

            response = response_func(endpoint, {'value1': '1',
                                                'value2': 'two'})
            self.assertEqual(200, response.status_code)
            self.assertEqual(response.json(), {'value1': {'value': 1,
                                                          'type': 'int'},
                                               'value2': {'value': u'two',
                                                          'type': 'str'}})

            response = response_func(endpoint, {'value1': 'one',
                                                'value2': 'two'})
            self.assertEqual(500, response.status_code)

    def test_choices_docrequest(self):
        for response_func in self.response_funcs():
            endpoint = self.path + "/choices-docrequest"

            response = response_func(endpoint, {'intchoice': '5',
                                                'strchoice': 'foo',
                                                'floatchoice': '42.42'})

            self.assertEqual(200, response.status_code)
            self.assertEqual(response.json()['intchoice'], 5)
            self.assertEqual(response.json()['strchoice'], 'foo')
            self.assertEqual(response.json()['floatchoice'], 42.42)

    def test_list_docrequest(self):
        for response_func in self.response_funcs():
            endpoint = self.path + "/list-docrequest"

            response = response_func(endpoint, {'intlist': ['5', '6'],
                                                'strlist': ['foo', 'bar'],  # TODO test with one element
                                                'floatlist': ['42.42', '39.39']})

            self.assertEqual(200, response.status_code)
            self.assertEqual(response.json()['intlist'], [5, 6])
            self.assertEqual(response.json()['strlist'], ['foo', 'bar'])
            self.assertEqual(response.json()['floatlist'], [42.42, 39.39])

    # def test_with_url_param(self):
    #     endpoint = self.path + "/with-url-param/5"
    #
    #     response = requests.get(endpoint, params={'testint': 4})
    #
    #     self.assertEqual(200, response.status_code)
    #     self.assertEqual(response.json()['testint'], 4)
    #     self.assertEqual(response.json()['url_param'], 5)


class DjangoIntegrationTest(TestBase, unittest.TestCase):
    path = "http://localhost:8000"
    args = ["manage.py", "runserver", "--noreload"]
    cwd = "../django_test_proj"


class PyramidIntegrationTest(TestBase, unittest.TestCase):
    path = "http://localhost:6543"
    args = ["pserve.py", "development.ini"]
    cwd = "../pyramid_test_proj"


class FlaskIntegrationTest(TestBase, unittest.TestCase):
    path = "http://localhost:5000"
    args = ["app.py"]
    cwd = "../flask_test_proj"
