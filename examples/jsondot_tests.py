import unittest
from unittest.mock import MagicMock, patch

import json
from typing import Optional, Union

from jsondot.jsondot import JsonDot, Dot


class TestDot(unittest.TestCase):

    def test_format_json(self):
        dot = Dot()
        self.assertEqual(dot.format_json("{'key': 'value'}"), '{"key": "value"}')

    def test_process_list_for_bumps(self):
        dot1 = Dot()
        dot2 = Dot()

        l = [dot1, [dot2]]
        expected_output1 = ["{}", ["{}"]]
        
        self.assertEqual(dot1.process_list_for_bumps(l), expected_output1)

    def test_dumps(self):
        dot1 = Dot()
        dot1.add_field('name', 'John')
        dot1.add_field('age', 30)

        expected_output2 = '{"name": "John", "age": 30}'
        
        self.assertEqual(dot1.dumps(), expected_output2)

    def test_dump_and_load(self):
        dot1 = Dot()
        dot1.add_field('name', 'John')
        dot1.add_field('surname', 'Smith')
        dot1.add_field('job', 'Pilot')
        
        file_path = 'test.json'
        
        # Write data to file
        dot1.dump(file_path)
        
        # Read data from file using JsonDot
        json_dot = JsonDot().load(file_path)
        
        # Check if the loaded data is correct
        expected_output3 = '{"name": "John"}'
        
        jdd = json_dot.dumps()
        
        print(jdd)
        
        
        
        self.assertEqual(json_dot.dumps, expected_output3)


if __name__ == '__main__':
    unittest.main()