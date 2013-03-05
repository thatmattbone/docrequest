"""
Tests.
"""
import unittest

from docrequest import schema_node_for_line
from docrequest import docrequest_django

import colander


class TestSchemaGeneration(unittest.TestCase):
    
    def test_failure(self):
        line = "invalid"
        self.assertRaises(Exception, lambda: schema_node_for_line(line))

    def test_missing_mapping(self):
        lines = ["  - foobar:fizzle",
                 " :param foobar fizzle: my description"]

        for line in lines:
            self.assertRaises(Exception, lambda: schema_node_for_line(line))

    def test_int(self):
        lines = ["  - value1:int",
                 " :param int value1: my description"]

        for line in lines:
            schema_node = schema_node_for_line(line)

            self.assertIsInstance(schema_node, colander.SchemaNode)
            self.assertIsInstance(schema_node.typ, colander.Int)
            self.assertEqual(schema_node.name, "value1")

    def test_str(self):
        lines = ["  - value2:str",
                 " :param str value2: my description"]

        for line in lines:
            schema_node = schema_node_for_line(line)

            self.assertIsInstance(schema_node, colander.SchemaNode)
            self.assertIsInstance(schema_node.typ, colander.Str)
            self.assertEqual(schema_node.name, "value2")

    def test_float(self):
        lines = ["  - myfloat:float",
                 " :param float myfloat: my description"]

        for line in lines:
            schema_node = schema_node_for_line(line)

            self.assertIsInstance(schema_node, colander.SchemaNode)
            self.assertIsInstance(schema_node.typ, colander.Float)
            self.assertEqual(schema_node.name, "myfloat")

    def test_list_int(self):
        lines = [" - myintlist:[int]",
                 ":param [int] myintlist: my integer list"]

        for line in lines:
            schema_node = schema_node_for_line(line)

            self.assertIsInstance(schema_node, colander.SchemaNode)
            self.assertIsInstance(schema_node.typ, colander.Sequence)
            self.assertIsInstance(schema_node.children[0].typ, colander.Int)
            self.assertEqual(schema_node.name, "myintlist")

    def test_choices_int(self):
        lines = [" - myintchoices:int<1,2,3>",
                 ":param int<1,2,3> myintchoices: my integer choices"]

        for line in lines:
            schema_node = schema_node_for_line(line)

            self.assertIsInstance(schema_node, colander.SchemaNode)
            self.assertIsInstance(schema_node.typ, colander.Int)
            self.assertIsInstance(schema_node.validator, colander.OneOf)
            self.assertEqual(schema_node.validator.choices, [1, 2, 3])
            self.assertEqual(schema_node.name, "myintchoices")

    def test_choices_str(self):
        lines = [" - mystrchoices:str<foo, bar, baz>",
                 ":param str<foo, bar, baz> mystrchoices: my string choices"]

        for line in lines:
            schema_node = schema_node_for_line(line)

            self.assertIsInstance(schema_node, colander.SchemaNode)
            self.assertIsInstance(schema_node.typ, colander.Str)
            self.assertIsInstance(schema_node.validator, colander.OneOf)
            self.assertEqual(schema_node.validator.choices, ['foo', 'bar', 'baz'])
            self.assertEqual(schema_node.name, "mystrchoices")

    def test_choices_float(self):
        lines = [" - myfloatchoices:float<42.42, 39.39, 52.52>",
                 ":param float<42.42, 39.39, 52.52> myfloatchoices: my float choices"]

        for line in lines:
            schema_node = schema_node_for_line(line)

            self.assertIsInstance(schema_node, colander.SchemaNode)
            self.assertIsInstance(schema_node.typ, colander.Float)
            self.assertIsInstance(schema_node.validator, colander.OneOf)
            self.assertEqual(schema_node.validator.choices, [42.42, 39.39, 52.52])
            self.assertEqual(schema_node.name, "myfloatchoices")


def stub_view(self):
    """This is my docstring."""


class TestDecorators(unittest.TestCase):

    def test_name_preserved(self):
        decorated_view = docrequest_django(stub_view)
        self.assertEqual(decorated_view.__name__, stub_view.__name__)

    def test_docstring_preserved(self):
        decorated_view = docrequest_django(stub_view)
        self.assertEqual(decorated_view.__doc__, stub_view.__doc__)


if __name__ == "__main__":
    unittest.main()
