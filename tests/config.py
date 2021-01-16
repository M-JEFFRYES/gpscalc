import json
import numpy as np

referenceDataDirectory = "tests\\exampledata\\reference"
subjectDataDirectory = "tests\\exampledata\\subject"
testPlotDirectory = "tests\\testplots"

# create example data
def createExampleKinematics(value, length, outputpath):
    variables = ['Pelvic Tilt Left', 'Pelvic Tilt Right', 'Hip Flexion Left', 
        'Hip Flexion Right', 'Knee Flexion Left', 'Knee Flexion Right', 
        'Ankle Dorsiflexion Left', 'Ankle Dorsiflexion Right', 
        'Pelvic Obliquity Left', 'Pelvic Obliquity Right', 'Hip Abduction Left', 
        'Hip Abduction Right', 'Pelvic Rotation Left', 'Pelvic Rotation Right', 
        'Hip Rotation Left', 'Hip Rotation Right', 'Foot Progression Left', 
        'Foot Progression Right']
    
    kinematics = {}
    for key in variables:
        kinematics[key] = [value]*length
    
    with open(outputpath, 'w') as f:
        json.dump(kinematics, f)
    return

def createExampleDatasets():
    arrLength = 50
    
    refValues = np.arange(4,6.2, .2)
    for i, value in  enumerate(refValues):
        outputpath = "exampledata\\reference\\reference_{}.json".format(i+1)
        createExampleKinematics(value, arrLength, outputpath)
    
    subValues = np.arange(4,8.4, .4)
    for i, value in  enumerate(subValues):
        outputpath = "exampledata\\subject\\subject_{}.json".format(i+1)
        createExampleKinematics(value, arrLength, outputpath)
    return

#createExampleDatasets()
