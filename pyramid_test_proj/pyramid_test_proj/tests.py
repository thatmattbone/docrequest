import unittest

from pyramid import testing

from .views import simple_docrequest, decorated_without_definitions

class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()


    def tearDown(self):
        testing.tearDown()


    def test_decorated_without_definitions(self):
        request = testing.DummyRequest()
        info = decorated_without_definitions(request)
        self.assertEqual("Hello World", info)


    def test_simple_docrequest_post(self):
        expected_response = "1:<class 'int'>, two:<class 'str'>"
        request = testing.DummyRequest(post={'value1': 1,
                                             'value2': 'two'})
        response = simple_docrequest(request)
        self.assertEqual(expected_response, response)

        expected_response = "2:<class 'int'>, four:<class 'str'>"
        request = testing.DummyRequest(post={'value1': 2,
                                             'value2': 'four'})
        response = simple_docrequest(request)
        self.assertEqual(expected_response, response)


    def test_simple_docrequest_get(self):
        expected_response = "1:<class 'int'>, two:<class 'str'>"
        request = testing.DummyRequest(params={'value1': 1,
                                               'value2': 'two'})
        response = simple_docrequest(request)
        self.assertEqual(expected_response, response)

        expected_response = "2:<class 'int'>, four:<class 'str'>"
        request = testing.DummyRequest(params={'value1': 2,
                                               'value2': 'four'})
        response = simple_docrequest(request)
        self.assertEqual(expected_response, response)
