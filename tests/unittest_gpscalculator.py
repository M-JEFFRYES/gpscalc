import sys, os
testdir = os.path.dirname(__file__)
srcdir = '../gpscalc'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

from gpscalculator import loadKinematicsJSON, calculateGPS, referenceGroup, plotGPS, batchGPS, exampleInputData

from config import referenceDataDirectory, subjectDataDirectory

import unittest

class exampleInputDataTest(unittest.TestCase):
    def setUp(self):
        self.example = exampleInputData()

        return
    
    def test_kinematicVariables(self):
        self.example.kinematicVariables()
        return
    def test_kinematics(self):
        self.example.kinematics()
        return
    def test_kinematicsJSON(self):
        self.example.kinematicsJSON("tests\\exampledata\\")
        return



class loadKinematicsJSONTest(unittest.TestCase):
    def setUp(self):
        self.refdirpath = referenceDataDirectory
        self.refpaths = []

        for path in os.listdir(self.refdirpath):
            self.refpaths.append(os.path.join(self.refdirpath, path))
        
    def test_loadKinematicsJSON(self):
        self.__kinematics = loadKinematicsJSON(self.refpaths[0])

class calculateGPSTest(unittest.TestCase):
    def setUp(self):
        self.referenceArray = [5]*101 
        self.subjectArray = [10]*101
        
        self.referenceKinematics = {}
        self.subjectKinematics = {}

        self.variables = ['Pelvic Tilt Left', 'Pelvic Tilt Right', 'Hip Flexion Left', 
        'Hip Flexion Right', 'Knee Flexion Left', 'Knee Flexion Right', 
        'Ankle Dorsiflexion Left', 'Ankle Dorsiflexion Right', 
        'Pelvic Obliquity Left', 'Pelvic Obliquity Right', 'Hip Abduction Left', 
        'Hip Abduction Right', 'Pelvic Rotation Left', 'Pelvic Rotation Right', 
        'Hip Rotation Left', 'Hip Rotation Right', 'Foot Progression Left', 
        'Foot Progression Right']

        for key in self.variables:
            self.referenceKinematics[key] = self.referenceArray 
            self.subjectKinematics[key] = self.subjectArray 

    def test_calculateGPS(self):
        self.__calculator = calculateGPS(self.referenceKinematics, self.subjectKinematics)

        errMSG = "Incorrect GPS variable value calculated"

        self.assertEqual(self.__calculator.gps[self.variables[0]], 5, errMSG)
        self.assertEqual(self.__calculator.gps["GPS"], 5, errMSG)
        self.assertEqual(self.__calculator.gps["GPS Left"], 5, errMSG)
        self.assertEqual(self.__calculator.gps["GPS Right"], 5, errMSG)
    
    def test_RMS(self):
        self.__calculator = calculateGPS(self.referenceKinematics, self.subjectKinematics)
        self.__RMS = self.__calculator.RMS([10]*20, [20]*20)

        errMSG = "Incorrect RMS value calculated"

        self.assertEqual(self.__RMS, 10, errMSG)
    
class referenceGroupTest(unittest.TestCase):
    def setUp(self):
        self.refdirpath = referenceDataDirectory

        self.refpaths = []
        for path in os.listdir(self.refdirpath):
            self.refpaths.append(os.path.join(self.refdirpath, path))

    def test_referenceGroup(self):
        self.__referenceGroup = referenceGroup()
        self.__referenceGroup.processGroupData(self.refpaths)

        errMSG = "Incorrect calculated average GPS variable"
        self.assertAlmostEqual(self.__referenceGroup.avgRefGPS["GPS"], 0.55)#,errMSG)

        #errMSG = "Incorrect calculated average kinematics variable "
        self.assertAlmostEqual(self.__referenceGroup.avgKinematics["Pelvic Tilt Left"][0], 5.075)#, errMSG)

class plotGPSTest(unittest.TestCase):
    def setUp(self):
        self.refdirpath = referenceDataDirectory
        self.subdirpath = subjectDataDirectory

        self.refpaths = []
        for path in os.listdir(self.refdirpath):
            self.refpaths.append(os.path.join(self.refdirpath, path))

        self.subpaths = []
        for path in os.listdir(self.subdirpath):
            self.subpaths.append(os.path.join(self.subdirpath, path))

        self.referenceGroup = referenceGroup()
        self.referenceGroup.processGroupData(self.refpaths)
        self.__referenceGPS = self.referenceGroup.avgRefGPS

        self.subjectKinematics = loadKinematicsJSON(self.subpaths[0])
        self.__subjectGPS = calculateGPS(self.referenceGroup.avgKinematics, self.subjectKinematics).gps

    def test_plotGPS(self):
        self.__plot = plotGPS(self.__referenceGPS, self.__subjectGPS, saveplot="tests\\exampledata\\unittest_gps_plot.png") 
        return
    
class batchGPSTest(unittest.TestCase):
    def setUp(self):
        self.refdirpath = referenceDataDirectory
        self.subdirpath = subjectDataDirectory

        self.refpaths = []
        for path in os.listdir(self.refdirpath):
            self.refpaths.append(os.path.join(self.refdirpath, path))

        self.subpaths = []
        for path in os.listdir(self.subdirpath):
            self.subpaths.append(os.path.join(self.subdirpath, path))
    
    def test_batchGPS(self):
        self.__subjectGroup = batchGPS()
        self.__subjectGroup.loadReferenceGroup(self.refpaths)
        self.__subjectGroup.processSubjectGroup(self.subpaths)

        refs = self.__subjectGroup.batchData.loc['REF_GROUP']
        #errMSG = "Incorrect calculated reference GPS value"
        self.assertAlmostEqual(refs["GPS"], 0.55)#, errMSG)

        sub1 = self.__subjectGroup.batchData.loc['SUB_1']
        #errMSG = "Incorrect calculated GPS value for first subject"
        self.assertAlmostEqual(sub1["GPS"], 1.075)#, errMSG)
        return

if __name__=="__main__":
    unittest.main()