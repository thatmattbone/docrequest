import unittest

from pyramid import testing

from .views import simple_request, my_view

class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()


    def tearDown(self):
        testing.tearDown()


    def test_my_view(self):
        request = testing.DummyRequest()
        info = my_view(request)
        self.assertEqual("Hello World", info)


    def test_simple_request_post(self):
        expected_response = "1:<class 'int'>, two:<class 'str'>"
        request = testing.DummyRequest(post={'value1': 1,
                                             'value2': 'two'})
        response = simple_request(request)
        self.assertEqual(expected_response, response)

        expected_response = "2:<class 'int'>, four:<class 'str'>"
        request = testing.DummyRequest(post={'value1': 2,
                                             'value2': 'four'})
        response = simple_request(request)
        self.assertEqual(expected_response, response)


    def test_simple_request_get(self):
        expected_response = "1:<class 'int'>, two:<class 'str'>"
        request = testing.DummyRequest(params={'value1': 1,
                                               'value2': 'two'})
        response = simple_request(request)
        self.assertEqual(expected_response, response)

        expected_response = "2:<class 'int'>, four:<class 'str'>"
        request = testing.DummyRequest(params={'value1': 2,
                                               'value2': 'four'})
        response = simple_request(request)
        self.assertEqual(expected_response, response)
