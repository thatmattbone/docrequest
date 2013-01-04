"""
Tests.
"""
import unittest

from docrequest import schema_node_for_line

import colander

class TestSchemaGeneration(unittest.TestCase):
    
    def test_schema_node_for_line_failure(self):
        line = "invalid"
        self.assertRaises(Exception, lambda: schema_node_for_line(line))


    def test_schema_node_for_line_missing_mapping(self):
        line = "  - foobar:fizzle"
        
        self.assertRaises(Exception, lambda: schema_node_for_line(line))


    def test_schema_node_for_line_int(self):
        line = "  - value1:int"
        schema_node = schema_node_for_line(line)

        self.assertIsInstance(schema_node, colander.SchemaNode)
        self.assertIsInstance(schema_node.typ, colander.Int)


    def test_schema_node_for_line_str(self):
        line = "  - value2:str"
        schema_node = schema_node_for_line(line)

        self.assertIsInstance(schema_node, colander.SchemaNode)
        self.assertIsInstance(schema_node.typ, colander.Str)


if __name__ == "__main__":
    unittest.main()
