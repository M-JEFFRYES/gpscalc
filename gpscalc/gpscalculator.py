import json
import os
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt


class calculateGPS:
    def __init__(self, referenceKinematics: dict, subjectKinematics: dict):

        self.refKins = referenceKinematics
        self.subKins = subjectKinematics

        self.gps = {}
        self.calculateGPS()
        return

    def RMS(self, reference, subject):
        """
        """ 
        ref = np.array(reference)
        sub = np.array(subject)
        ss = np.sum((ref-sub)**2)
        rms = np.sqrt(ss/len(ref))
        return rms

    def calculateGPS(self):
        """
        """
        l_var,  r_var, var = [], [], []
        for key, value in self.refKins.items():
            rms = self.RMS(value, self.subKins[key])
            self.gps[key] = rms 
            var.append(rms)
            if "Left" in key:
                l_var.append(rms)
            elif "Right" in key:
                r_var.append(rms)
            else:
                pass

        self.gps["GPS Left"] = np.mean(l_var)
        self.gps["GPS Right"] = np.mean(r_var)
        self.gps["GPS"] = np.mean(var)
        return
    
class refernceGroup:

    def __init__(self):
        self.initInputDatasets()
        return
    
    def initInputDatasets(self):
        self.variables = ['Pelvic Tilt Left', 'Pelvic Tilt Right', 'Hip Flexion Left', 
        'Hip Flexion Right', 'Knee Flexion Left', 'Knee Flexion Right', 
        'Ankle Dorsiflexion Left', 'Ankle Dorsiflexion Right', 
        'Pelvic Obliquity Left', 'Pelvic Obliquity Right', 'Hip Abduction Left', 
        'Hip Abduction Right', 'Pelvic Rotation Left', 'Pelvic Rotation Right', 
        'Hip Rotation Left', 'Hip Rotation Right', 'Foot Progression Left', 
        'Foot Progression Right']

        self.inputKinematics = []
        return

    def checkInputKins(self, inputKins: dict):
        checksum = 0 
        keys = list(inputKins.keys())

        for key in keys:
            if key in self.variables:
                checksum = checksum+1
            else:
                print("New key found: {}".format(key))
                return False
        
        if checksum==len(self.variables):
            return True
        else:
            return False

    def loadKinematics(self, jsonPath: str):
        with open(jsonPath,'rb') as f:
            kinematics = json.load(f)
        
        if self.checkInputKins(kinematics):
            return kinematics
        else:
            print("Check input data from: {}".format(jsonPath))
            return 0

    def addInputKinematics(self, jsonPath: dict):
        self.inputKinematics.append(self.loadKinematics(jsonPath))
        return

    def loadInputDataFromList(self, inputPaths: list):
        for path in inputPaths:
            self.addInputKinematics(path)
        return
    
    def averageVariable(self, groupKinematics: list):
        data = np.array(groupKinematics)
        avg = np.mean(np.array(data), axis=0)
        return avg

    def calculateAverageKinematics(self):
        self.avgKinematics = {}
        for var in self.variables:
            varData = []
            for i, kinematics in enumerate(self.inputKinematics):
                varData.append(kinematics[var])    
            varAvg = self.averageVariable(varData)
            self.avgKinematics[var] = varAvg
        return

    def calculateGroupGPS(self):
        cols = self.variables
        cols.append("GPS Left")
        cols.append("GPS Right")
        cols.append("GPS")
        self.groupGPS = pd.DataFrame(columns=cols, data=None)
        for i, subjectKinematics in enumerate(self.inputKinematics):
            subGPS = calculateGPS(self.avgKinematics, subjectKinematics).gps
            self.groupGPS = self.groupGPS.append(subGPS, ignore_index=True)
        return 

    def averageReferenceGPS(self):
        avgRef={}

        for col in self.groupGPS:
            avgRef[col] = self.groupGPS[col].mean()
        
        self.avgRefGPS ={}
        self.avgRefGPS['GPS'] = avgRef['GPS']

        keys = ['Pelvic Tilt', 'Hip Flexion', 'Knee Flexion', 'Ankle Dorsiflexion', 'Pelvic Obliquity',
        'Hip Abduction', 'Hip Abduction', 'Pelvic Rotation', 'Hip Rotation', 'Foot Progression']
        for key in keys:
            left = "{} Left".format(key)
            right = "{} Right".format(key)

            self.avgRefGPS[key] = (avgRef[left] +avgRef[right] )/2
        return

    def processGroupData(self, inputPaths: list):

        self.loadInputDataFromList(inputPaths)
        self.calculateAverageKinematics()
        self.calculateGroupGPS()
        self.averageReferenceGPS()
        return

class plotGPS:

    def __init__(self, referenceGPS: dict, subjectGPS: dict , subjectname=None, saveplot=None):
        self.ref = referenceGPS
        self.subject = subjectGPS

        if subjectname!=None:
            self.plotTitle = "{} Gait Profile Score".format(subjectname)
        else:
            self.plotTitle = "Gait Profile Score"

        self.plot()

        if saveplot!=None:
            self.fig.savefig(saveplot)
        return

    def separateVariables(self):
        self.left_vars = [self.subject['Pelvic Tilt Left'], self.subject['Hip Flexion Left'], self.subject['Knee Flexion Left'], self.subject['Ankle Dorsiflexion Left'], self.subject['Pelvic Obliquity Left'], self.subject['Hip Abduction Left'], self.subject['Pelvic Rotation Left'], self.subject['Hip Rotation Left'], self.subject['Foot Progression Left'], 0, self.subject['GPS Left']]
        self.right_vars = [self.subject['Pelvic Tilt Right'], self.subject['Hip Flexion Right'], self.subject['Knee Flexion Right'], self.subject['Ankle Dorsiflexion Right'], self.subject['Pelvic Obliquity Right'], self.subject['Hip Abduction Right'], self.subject['Pelvic Rotation Right'], self.subject['Hip Rotation Right'], self.subject['Foot Progression Right'], 0, self.subject['GPS Right']]
        self.ref_vars =  [self.ref['Pelvic Tilt'], self.ref['Hip Flexion'], self.ref['Knee Flexion'], self.ref['Ankle Dorsiflexion'], self.ref['Pelvic Obliquity'], self.ref['Hip Abduction'], self.ref['Pelvic Rotation'], self.ref['Hip Rotation'], self.ref['Foot Progression'], 0, self.ref['GPS']]
        return
    
    def calculateBars(self):
        # First number sets the width of the left/right bars
        self.width = 0.35
        self.ref_widths, self.widths, self.pos_l, self.pos_r = [], [] , [], []
        self.xTicks = np.arange(len(self.left_vars))

        for i in range(len(self.xTicks)-1):
            self.widths.append(self.width)
            self.ref_widths.append(2*self.width)
            self.pos_l.append(self.xTicks[i]-self.width/2)
            self.pos_r.append(self.xTicks[i]+self.width/2)
    
        # Set width and position for GPS vars
        self.widths.append((self.width*2)/3)
        self.pos_l.append(self.xTicks[-1]-(self.width*2)/3)
        self.pos_r.append(self.xTicks[-1])

        self.ref_widths.append(self.width*2)
        
        # value, width, position for overall gps 
        self.overall_gps = [self.subject['GPS'], (self.width*2)/3, self.xTicks[-1]+(self.width*2)/3]
        return   

    def plot(self):

        ticks = ['Pel tilt', 'Hip flex', 'Knee flex', 'Ank dors', 'Pel obl', 'Hip abd', 'Pel rot', 'Hip rot', 'Foot prog', None,  'GPS']

        self.separateVariables()

        self.calculateBars()

        self.fig, ax = plt.subplots()

        rects1 = ax.bar(self.pos_l, height=self.left_vars, width=self.widths, label='Left')
        rects2 = ax.bar(self.pos_r, height=self.right_vars, width=self.widths, label='Right')
        rectsOVR = ax.bar(self.overall_gps[2], height=self.overall_gps[0], width=self.overall_gps[1], label="Overall")
        rectsREF = ax.bar(self.xTicks, height=self.ref_vars, width=self.ref_widths, label='No pathology', zorder=1)

        ax.set_ylabel('RMS difference (deg)')
        ax.set_title(self.plotTitle)
        ax.set_xticks(self.xTicks)
        ax.set_xticklabels(ticks, rotation=45, ha='right')
        ax.legend()
        self.fig.show()
        return
    
class batchGPS:
    def __init__(self):
        self.variables = ['Pelvic Tilt Left', 'Pelvic Tilt Right', 'Hip Flexion Left', 
        'Hip Flexion Right', 'Knee Flexion Left', 'Knee Flexion Right', 
        'Ankle Dorsiflexion Left', 'Ankle Dorsiflexion Right', 
        'Pelvic Obliquity Left', 'Pelvic Obliquity Right', 'Hip Abduction Left', 
        'Hip Abduction Right', 'Pelvic Rotation Left', 'Pelvic Rotation Right', 
        'Hip Rotation Left', 'Hip Rotation Right', 'Foot Progression Left', 
        'Foot Progression Right', 'GPSRight', 'GPS Left', 'GPS']

        self.batchData = pd.DataFrame(data=None, columns=self.variables)
        return

    def addRefGroup(self):

        refdata = {'Pelvic Tilt Left':self.referenceGPS['Pelvic Tilt'], 
        'Pelvic Tilt Right':self.referenceGPS['Pelvic Tilt'], 
        'Hip Flexion Left':self.referenceGPS['Hip Flexion'], 
        'Hip Flexion Right':self.referenceGPS['Hip Flexion'], 
        'Knee Flexion Left':self.referenceGPS['Knee Flexion'], 
        'Knee Flexion Right':self.referenceGPS['Knee Flexion'], 
        'Ankle Dorsiflexion Left':self.referenceGPS['Ankle Dorsiflexion'], 
        'Ankle Dorsiflexion Right':self.referenceGPS['Ankle Dorsiflexion'], 
        'Pelvic Obliquity Left':self.referenceGPS['Pelvic Obliquity'], 
        'Pelvic Obliquity Right':self.referenceGPS['Pelvic Obliquity'], 
        'Hip Abduction Left':self.referenceGPS['Hip Abduction'], 
        'Hip Abduction Right':self.referenceGPS['Hip Abduction'], 
        'Pelvic Rotation Left':self.referenceGPS['Pelvic Rotation'], 
        'Pelvic Rotation Right':self.referenceGPS['Pelvic Rotation'], 
        'Hip Rotation Left':self.referenceGPS['Hip Rotation'], 
        'Hip Rotation Right':self.referenceGPS['Hip Rotation'], 
        'Foot Progression Left':self.referenceGPS['Foot Progression'], 
        'Foot Progression Right':self.referenceGPS['Foot Progression'], 
        'GPSRight':self.referenceGPS['GPS'], 
        'GPS Left':self.referenceGPS['GPS'], 
        'GPS':self.referenceGPS['GPS']
        }
        self.batchData.loc["REF_GROUP"] = refdata
        return

    def loadReferenceGroup(self, inputPaths):
        refGroup = refernceGroup()
        refGroup.processGroupData(inputPaths)
        self.referenceAvgKins = refGroup.avgKinematics
        self.referenceGPS = refGroup.avgRefGPS
        self.addRefGroup()
        return 
    
    def processSubjectGroup(self, inputPaths: list, inputReferences=None):

        if inputReferences==None:
            inputReferences=[]
            for i in range(len(inputPaths)):
                inputReferences.append("SUB_{}".format(i+1))

        for index, path in enumerate(inputPaths):

            with open(path,'rb') as f:
                subjectKins = json.load(f)
            gps = calculateGPS(self.referenceAvgKins, subjectKins).gps

            self.batchData.loc[inputReferences[index]] = gps

        return 


##################

def test():

    refpath = "..\\tests\\exampledata\\reference"
    refkinematics = []
    for filename in os.listdir(refpath):
        if ".json" in filename:
            refkinematics.append(os.path.join(refpath, filename))
    
    subpath = "..\\tests\\exampledata\\subject"
    subkinematics = []
    for filename in os.listdir(subpath):
        if ".json" in filename:
            subkinematics.append(os.path.join(subpath, filename))

    x = refernceGroup()
    x.processGroupData(refkinematics)

    with open(subkinematics[0],'rb') as f:
        subKins = json.load(f)

    sub = calculateGPS(x.avgKinematics,subKins).gps

    p = plotGPS(x.avgRefGPS, sub, subjectname="test", saveplot="..\\tests\\testplots\\test_gps.png")

    b = batchGPS()
    b.loadReferenceGroup(refkinematics)
    b.processSubjectGroup(subkinematics)

    return

#test()