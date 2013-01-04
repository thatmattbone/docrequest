import unittest

from pyramid import testing


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()


    def tearDown(self):
        testing.tearDown()


    def test_my_view(self):
        from .views import my_view

        request = testing.DummyRequest()
        info = my_view(request)
        self.assertEqual("Hello World", info)


    def test_simple_post(self):
        from .views import simple_post

        expected_response = "1:<class 'int'>, two:<class 'str'>"
        request = testing.DummyRequest(post={'value1': 1,
                                             'value2': 'two'})
        response = simple_post(request)
        self.assertEqual(expected_response, response)

        expected_response = "two:<class 'str'>, 1:<class 'int'>"
        request = testing.DummyRequest(post={'value1': 'two',
                                             'value2': 2})
        response = simple_post(request)
        self.assertEqual(expected_response, response)
