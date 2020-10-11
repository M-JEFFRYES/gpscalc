from gpscalculator import load_kinematic_data, group_average_kinematics, group_kinematics_stdev
from gpscalculator import calculate_GPS, plot_GPS
from gpscalculator import GPSData
from calculations import get_dir_filepaths

import unittest

class gpsCalcTest(unittest.TestCase):

    def setUp(self):
        self._refdirpath = "exampledata\\reference"
        self._subdirpath = "exampledata\\subject"

        self._reffilepaths = get_dir_filepaths(self._refdirpath)
        self._subfilepaths = get_dir_filepaths(self._subdirpath)

    def test_load_kinematic_data(self):

        kinematic_data = load_kinematic_data(self._reffilepaths[0])

    def test_group_average_stdev(self):
        
        _AVG_KINEMATICS = group_average_kinematics(self._refdirpath)

    def test_group_kinematics_stdev(self):
        
        __AVG_KINEMATICS = group_average_kinematics(self._refdirpath)

        __STDEV_GPS = group_kinematics_stdev(self._refdirpath, __AVG_KINEMATICS)

    def test_calculate_GPS(self):

        __AVG_KINEMATICS = group_average_kinematics(self._refdirpath)

        __SUB_GPS = calculate_GPS(self._subfilepaths[0], __AVG_KINEMATICS)

    def test_plot_GPS(self):
        
        __AVG_KINEMATICS = group_average_kinematics(self._refdirpath)

        __SUB_GPS = calculate_GPS(self._subfilepaths[0], __AVG_KINEMATICS)

        __STDEV_GPS = group_kinematics_stdev(self._refdirpath, __AVG_KINEMATICS)

        plot_GPS("Testing", __SUB_GPS, __STDEV_GPS, "testplots")


class GPSDataTest(unittest.TestCase):

    def setUp(self):
        
        self._refdirpath = "exampledata\\reference"
        self._subdirpath = "exampledata\\subject"

        self._reffilepaths = get_dir_filepaths(self._refdirpath)
        self._subfilepaths = get_dir_filepaths(self._subdirpath)
    
    def test_Calculator(self):

        GPS_data = GPSData(self._subfilepaths[0], self._refdirpath)
    
    def test_plot_data(self):
        
        GPS_data = GPSData(self._subfilepaths[0], self._refdirpath)

        GPS_data.plot_data("unittest", "testplots")


    
if __name__=="__main__":
    unittest.main()