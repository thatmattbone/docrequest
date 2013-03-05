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
                                   stdout=open(os.devnull, 'w'),
                                   stderr=open(os.devnull, 'w'))

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
        cls.pid.kill()
        cls.pid.wait()

    def test_decorated_without_definitions(self):
        response = requests.get(self.path + "/decorated-without-definitions")
        self.assertEqual("Hello World", response.text)

    def test_simple_docrequest_get(self):
        endpoint = self.path + "/simple-docrequest"

        response = requests.get(endpoint, params={'value1': '1',
                                                  'value2': 'two'})
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json(),
                         {'value1': {'value': 1,
                                     'type': 'int'},
                          'value2': {'value': u'two',
                                     'type': 'str'}})

        response = requests.get(endpoint, params={'value1': 'one',
                                                  'value2': 'two'})
        self.assertEqual(500, response.status_code)

    def test_simple_docrequest_post(self):
        endpoint = self.path + "/simple-docrequest"

        response = requests.post(endpoint, data={'value1': '1',
                                                 'value2': 'two'})
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json(),
                         {'value1': {'value': 1,
                                     'type': 'int'},
                          'value2': {'value': u'two',
                                     'type': 'str'}})

        response = requests.post(endpoint, data={'value1': 'one',
                                                 'value2': 'two'})
        self.assertEqual(500, response.status_code)

    def test_simple_docrequest_sphinx_get(self):
        endpoint = self.path + "/simple-docrequest-sphinx"

        response = requests.get(endpoint, params={'value1': '1',
                                                  'value2': 'two'})
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json(),
                         {'value1': {'value': 1,
                                     'type': 'int'},
                          'value2': {'value': u'two',
                                     'type': 'str'}})

        response = requests.get(endpoint, params={'value1': 'one',
                                                  'value2': '2'})
        self.assertEqual(500, response.status_code)

    def test_simple_docrequest_sphinx_post(self):
        endpoint = self.path + "/simple-docrequest-sphinx"

        response = requests.post(endpoint, data={'value1': '1',
                                                 'value2': 'two'})
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json(),
                         {'value1': {'value': 1,
                                     'type': 'int'},
                          'value2': {'value': u'two',
                                     'type': 'str'}})

        response = requests.post(endpoint, data={'value1': 'one',
                                                 'value2': '2'})
        self.assertEqual(500, response.status_code)

    def test_choices_docrequest(self):
        endpoint = self.path + "/choices-docrequest"

        response = requests.get(endpoint, params={'intchoice': '5',
                                                  'strchoice': 'foo',
                                                  'floatchoice': '42.42'})

        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json()['intchoice'], 5)
        self.assertEqual(response.json()['strchoice'], 'foo')
        self.assertEqual(response.json()['floatchoice'], 42.42)

    def test_choices_docrequest_shpinx(self):
        endpoint = self.path + "/choices-docrequest-sphinx"

        response = requests.get(endpoint, params={'intchoice': '5',
                                                  'strchoice': 'foo',
                                                  'floatchoice': '42.42'})

        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json()['intchoice'], 5)
        self.assertEqual(response.json()['strchoice'], 'foo')
        self.assertEqual(response.json()['floatchoice'], 42.42)

    # TODO need to rethink this...
    # def test_list_docrequest(self):
    #     endpoint = self.path + "/list-docrequest"
    #
    #     response = requests.get(endpoint, params={'intlist': ['5', '6'],
    #                                               'strlist': ['foo'],
    #                                               'floatlist':['42.42', '39.39']})
    #
    #     self.assertEqual(200, response.status_code)
    #     self.assertEqual(response.json()['intchoice'], [5, 6])
    #     self.assertEqual(response.json()['strchoice'], ['foo'])
    #     self.assertEqual(response.json()['floatchoice'], [42.42, 39.39])



class DjangoIntegrationTest(TestBase, unittest.TestCase):

    path = "http://localhost:8000"
    args = ["manage.py", "runserver"]
    cwd = "../django_test_proj"


class PyramidIntegrationTest(TestBase, unittest.TestCase):

    path = "http://localhost:6543"
    args = ["pserve.py", "development.ini"]
    cwd = "../pyramid_test_proj"


if __name__ == "__main__":
    unittest.main()
