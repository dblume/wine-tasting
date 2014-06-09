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
        allocator = wine_allocator.WineAllocator()
        allocator.process(lines)
        out_lines = self.get_stdout()
        self.assertEqual("8", out_lines[0])
        self.assertEqual(int(out_lines[0]), len(out_lines)-1)
        self.assertTrue("p5\tw10" in out_lines)
        self.assertTrue("p1\tw3" in out_lines)
        wine_allocator.verify_result_file()

    def test_contention_for_one(self):
        lines = ("p1\tw1",
                 "p1\tw2",
                 "p1\tw3",
                 "p1\tw4",
                 "p1\tw5",
                 "p2\tw1",
                 "p2\tw6",
                 )
        allocator = wine_allocator.WineAllocator()
        allocator.process(lines)
        out_lines = self.get_stdout()
        self.assertEqual("5", out_lines[0])
        self.assertTrue("p2\tw6" in out_lines)
        self.assertTrue("p1\tw3" in out_lines)
        self.assertEqual(int(out_lines[0]), len(out_lines)-1)
        wine_allocator.verify_result_file()

    def test_simple_contention_for_two(self):
        lines = ("p1\tw1",
                 "p2\tw1",
                 "p3\tw1",
                 "p4\tw2",
                 "p5\tw2",
                 )
        allocator = wine_allocator.WineAllocator()
        allocator.process(lines)
        out_lines = self.get_stdout()
        self.assertEqual("2", out_lines[0])
        self.assertEqual(int(out_lines[0]), len(out_lines)-1)
        self.assertTrue("p2\tw1" in out_lines)
        self.assertTrue("p4\tw2" in out_lines)
        wine_allocator.verify_result_file()

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
        allocator = wine_allocator.WineAllocator()
        allocator.process(lines)
        out_lines = self.get_stdout()
        self.assertEqual("4", out_lines[0])
        self.assertEqual(int(out_lines[0]), len(out_lines)-1)
        wine_allocator.verify_result_file()

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
        allocator = wine_allocator.WineAllocator()
        allocator.process(lines)
        out_lines = self.get_stdout()
        self.assertEqual("6", out_lines[0])
        self.assertEqual(int(out_lines[0]), len(out_lines)-1)
        wine_allocator.verify_result_file()

    def test_tricky_contention(self):
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
        allocator = wine_allocator.WineAllocator()
        allocator.process(lines)
        out_lines = self.get_stdout()
        self.assertEqual("10", out_lines[0])
        self.assertEqual(int(out_lines[0]), len(out_lines)-1)
        self.assertTrue("p2\tw7" in out_lines)
        self.assertTrue("p1\tw3" in out_lines)
        wine_allocator.verify_result_file()

if __name__ == '__main__':
    unittest.main()
