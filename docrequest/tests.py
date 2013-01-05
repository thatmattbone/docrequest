"""
Tests.
"""
import unittest

from docrequest import schema_node_for_line

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


if __name__ == "__main__":
    unittest.main()
