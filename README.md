# Gait Profile Score Calculator

gpscalc is a package that can be used to calculate the gait profile score as stated in Baker et al. 2009. The package requires the gait trials kinematic data to be stored in a json file using specific variable names.

(Baker, R. et al., 2009. The Gait Profile Score and Movement Analysis Profile. Gait and Posture, 30(1), pp. 265-269.)

Kinematic gait data has to be in a specific format for the calculation, the specifics of the format required can be seen using the functions below to create example JSON files. 

# Using gpscalculator

## Installation

pip install gait-profile-score


## Process reference group data
from gpscalculator import referenceGroup

refPaths = "List of paths to the reference group kinematics JSON files

referenceData = refernceGroupKinematics()
referenceData.processGroupData(refkinematics)

referenceKinematics = referenceData.avgKinematics
referenceGPS = referenceData.avgRefGPS

## Calculate the GPS of a single subject
from gpscalculator import calculateGPS

subjectKinematics = "dictionary of the kinematic data"

subjectGPS = calculateGPS(referenceKinematics, subjectKinematics).gps

## Plot and save the GPS figure

from gpscalculator import plotGPS

plot = plotGPS(referenceGPS, subjectGPS, saveplot="test_gps_plot.png") 


## Batch process a subject group

from gpscalculator import batchGPS

groupPaths = "List of paths to the subject group kinematics JSON files

subjectGroup = batchGPS()
subjectGroup.loadReferenceGroup(refPaths)
subjectGroup.processSubjectGroup()

print(subjectGroup.batchData) # prints the dataframe containing the subject group GPS data
