#!/usr/bin/python
import sys
import unittest
from StringIO import StringIO
import wine_allocator


class Tee(object):
    def __init__(self):
        self.saved_stdout = sys.stdout
        self.stdout = StringIO()
        sys.stdout = self

    def close_and_get_output(self):
        sys.stdout = self.saved_stdout
        output = self.stdout.getvalue().strip()
        self.stdout.close()
        return output

    def write(self, data):
        self.stdout.write(data)
        self.saved_stdout.write(data)


class TestWineAllocation(unittest.TestCase):
    def setUp(self):
        self.tee = Tee()

    def get_stdout(self):
        return self.tee.close_and_get_output().splitlines()

    def perform_test_and_verify_result(self, lines, num_out_lines):
        allocator = wine_allocator.WineAllocator()
        allocator.process(lines)
        out_lines = self.get_stdout()
        self.assertEqual(str(num_out_lines), out_lines[0])
        self.assertEqual(int(out_lines[0]), len(out_lines)-1)
        self.assertTrue(set(out_lines[1:]).issubset(set(lines)))
        # The next test asserts the results contain non-repeating wines
        # and that there are no more than 3 instances of the same person.
        wine_allocator.verify_result_file()

    def test_no_contention(self):
        lines = ("p1\tw1",
                 "p1\tw2",
                 "p1\tw3",
                 "p1\tw4",
                 "p1\tw5",
                 "p2\tw6",
                 "p2\tw7",
                 "p3\tw8",
                 "p4\tw9",
                 "p5\tw10",
                 )
        self.perform_test_and_verify_result(lines, 8)

    def test_contention_for_one(self):
        lines = ("p1\tw1",
                 "p1\tw2",
                 "p1\tw3",
                 "p1\tw4",
                 "p1\tw5",
                 "p2\tw1",
                 "p2\tw6",
                 )
        self.perform_test_and_verify_result(lines, 5)

    def test_simple_contention_for_two(self):
        lines = ("p1\tw1",
                 "p2\tw1",
                 "p3\tw1",
                 "p4\tw2",
                 "p5\tw2",
                 )
        self.perform_test_and_verify_result(lines, 2)

    def test_only_quad_contention(self):
        lines = ("p0\tw1",
                 "p0\tw2",
                 "p0\tw3",
                 "p0\tw4",
                 "p1\tw1",
                 "p1\tw2",
                 "p1\tw3",
                 "p1\tw4",
                 "p2\tw1",
                 "p2\tw2",
                 "p2\tw3",
                 "p2\tw4",
                 "p3\tw1",
                 "p3\tw2",
                 )
        self.perform_test_and_verify_result(lines, 4)

    def test_cant_sell_all(self):
        lines = ("p0\tw1",
                 "p0\tw2",
                 "p0\tw3",
                 "p0\tw4",
                 "p0\tw5",
                 "p0\tw6",
                 "p0\tw7",
                 "p1\tw1",
                 "p1\tw2",
                 "p1\tw3",
                 "p1\tw4",
                 "p1\tw5",
                 "p1\tw6",
                 "p1\tw7",
                 )
        self.perform_test_and_verify_result(lines, 6)

    def test_adhoc_contention(self):
        lines = ("p0\tw1",
                 "p0\tw2",
                 "p1\tw1",
                 "p1\tw2",
                 "p1\tw3",
                 "p1\tw4",
                 "p1\tw5",
                 "p2\tw0",
                 "p2\tw7",
                 "p3\tw8",
                 "p4\tw9",
                 "p5\tw10",
                 )
        self.perform_test_and_verify_result(lines, 10)

if __name__ == '__main__':
    unittest.main()
