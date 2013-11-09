# -*- coding: utf-8 -*-

import os
import unittest

from kamika.load import KamikaLoader

ROOT_DIR = os.path.split(os.path.dirname(__file__))[0]

class TestLoadFile(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.file = KamikaLoader._load_file_data(os.path.join(ROOT_DIR, 'data', '2dc0001.MD1'))

    def test_loader_histogram(self):
        self.assertTrue(self.file is not None)
        self.assertEqual(self.file.data, self.EXPECTED_DATA)

    def test_loader_date(self):
        self.assertTrue(self.file is not None)
        self.assertEqual(self.file.date, '2013-10-16')

    def test_loader_end(self):
        self.assertTrue(self.file is not None)
        self.assertEqual(self.file.stop, '18:52:51')

    def test_loader_start(self):
        self.assertTrue(self.file is not None)
        self.assertEqual(self.file.start, '18:34:47')



    EXPECTED_DATA = (3106, 3406, 3388, 3271, 2837, 2259, 1772, 1216,  863,  563,  366,
        195,  124,   66,   35,   18,   11,   17,   10,    9,    9,    9,
         13,    7,    7,    8,    3,    5,    4,    5,    5,    3,    3,
          3,    6,    2,    3,    6,    2,    1,    0,    1,    1,    3,
          0,    1,    1,    2,    1,    1,    2,    1,    1,    1,    0,
          0,    2,    2,    0,    0,    0,    0,    0,    0,    0,    0,
          0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
          0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
          0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
          0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
          0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
          0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
          0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
          0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
          0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
          0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
          0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
          0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
          0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
          0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
          0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
          0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
          0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
          0,    0)

class TestLoadDir(unittest.TestCase):
    def setUp(self):
        self.dates = []
        self.data = []

        KamikaLoader._load_directory(os.path.join(ROOT_DIR, 'data'), self.dates, self.data)

    def test_equal_len(self):

        self.assertEqual(len(self.data), len(self.dates))

