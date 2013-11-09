# -*- coding: utf-8 -*-

import mmap
from operator import itemgetter, methodcaller, attrgetter
import os
import struct
import glob
import numpy as np
from collections import namedtuple, OrderedDict
from datetime import datetime, time, date


noop = lambda x: x

class KamikaLoader(object):

    def __init__(self, dirs_to_load = tuple()):
        dates = []
        data = []

        for dir in dirs_to_load:
            self._load_directory(dir, dates, data)

        self.data = np.asanyarray(map(attrgetter('data'), data))
        self.dates = np.asanyarray(dates)
        self.files = data

    @classmethod
    def _load_directory(cls, dirname, date_list, data_list):


        for file in sorted(glob.glob(dirname + "/*MD1")):
            opened = cls._load_file_data(os.path.join(dirname, file))
            data_list.append(opened)
            date_list.append(cls._measurement_date(opened))

    @classmethod
    def _load_file_data(cls, filename):

        if not filename.endswith('MD1'):
            raise ValueError("Kamika file name should end witg *MD1 extension")

        with open(filename, 'r+b') as f:
            data = mmap.mmap(f.fileno(), 0)
            result = {}
            for name, (offset, format, operation) in cls.FORMAT.items():

                result[name] = operation(struct.unpack_from(format, data, offset))

            file = cls.KamikaFile(**result)
            return file

    @classmethod
    def _measurement_date(cls, file):
        """
        >>> file = KamikaFile(date='2001-01-01', start='00:00:00', stop='00:00:10', data=None)
        >>> KamikaLoader._measurement_date(file)
        datetime.datetime(2001, 1, 1, 0, 0, 5)
        """
        date = datetime.strptime(file.date, cls.DATE_FORMAT).date()
        start = datetime.strptime(file.start, cls.TIME_FORMAT)
        stop = datetime.strptime(file.stop, cls.TIME_FORMAT)

        meas_len = (stop - start)/2

        return datetime.combine(date, (start + meas_len).time())

    __decode_utf8 = lambda x: x[0].decode('utf-8')

    FORMAT = OrderedDict()
    
    FORMAT.update((
        ('suckction_speed', (0x5d6, '<L', itemgetter(0))),
        ('data' , (0x80a, '<255L', noop)),
        ('date' , (0x1305, '<10s', __decode_utf8)),
        ('start' , (0x13d1, '<8s', __decode_utf8)),
        ('stop' , (0x1415, '<8s', __decode_utf8)),
        ('wind_speed', (0x5d6, '<L', lambda x: x[0]/4.0)),
        ('humidity', (0x204, '<L', lambda x:x[0]/3501.0*100)),
        ('wind_direction', (0x91, '<L', itemgetter(0)))
    ))

    KamikaFile = namedtuple('KamikaFile', FORMAT.keys())


    TIME_FORMAT = '%H:%M:%S'

    DATE_FORMAT = '%Y-%m-%d'






