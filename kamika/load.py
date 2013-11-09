# -*- coding: utf-8 -*-

import mmap
import os
import struct
import glob
import numpy as np
from collections import namedtuple
from datetime import datetime, time, date

KamikaFile = namedtuple('KamikaFile', ['data', 'date', 'start', 'stop'])


class KamikaLoader(object):

    def __init__(self, dirs_to_load = []):
        dates = []
        data = []

        for dir in dirs_to_load:
            self._load_directory(dir, dates, data)

        self.data = np.asanyarray(data)
        self.dates = np.asanyarray(dates)

    @classmethod
    def _load_directory(cls, dirname, date_list, data_list):


        for file in glob.glob(dirname + "/*MD1"):
            opened = cls._load_file_data(os.path.join(dirname, file))
            data_list.append(opened.data)
            date_list.append(cls._measurement_date(opened))

    @classmethod
    def _load_file_data(cls, filename):

        if not filename.endswith('MD1'):
            raise ValueError("Kamika file name should end witg *MD1 extension")

        with open(filename, 'r+b') as f:
            data = mmap.mmap(f.fileno(), 0)

            result = struct.unpack_from(cls.FORMAT, data[:])
            print("Loaded: "  +filename)
            return KamikaFile(data=result[:-4], date=result[-3].decode('utf-8'), start=result[-2].decode('utf-8'), stop=result[-1].decode('utf-8'))

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


    FORMAT = {
        'suckction_speed': (0x5d6, '<L'),
        'wind_speed': ('0x5d6', '<L', lambda x: x/4.0),
        'data' : (0x80a, '<256L'),

    }


    FORMAT = '< 2058x 256L 1787x 10s 194x 8s 60x 8s'
    """
    256 channels
    Measurement date
    Measurement start
    Mesaurement end
    """

    TIME_FORMAT = '%H:%M:%S'

    DATE_FORMAT = '%Y-%m-%d'






