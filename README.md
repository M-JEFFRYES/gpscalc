# Welcome to Gait Profile Score Calculator’s documentation!

# How to use the GPS Calculator

**gpscalc** is a package that can be used to calculate the gait profile score as stated in Baker et al. 2009. The package requires the gait trials kinematic data to be stored in a json file using specific variable names.
(Baker, R. et al., 2009. The Gait Profile Score and Movement Analysis Profile. Gait and Posture, 30(1), pp. 265-269.)
Kinematic gait data has to be in a specific format for the calculation, the specifics of the format required can be seen using the functions below to create example JSON files.

## Package Installation

```
pip install gait-profile-score
```

## Processing the reference group data

```
from gpscalculator import referenceGroup

# List of paths to the reference group kinematics JSON files
referencePaths = [...]

referenceData = refernceGroupKinematics()
referenceData.processGroupData(referencePaths)

# The average of the reference kinematic variables over the gait cycle
referenceKinematics = referenceData.avgKinematics

# The average GPS scores of the reference group relative to the average kinematics
referenceGPS = referenceData.avgRefGPS
```

## Calculation of GPS for a single subject

```
from gpscalculator import calculateGPS

# The kinematic data for the selected subject
subjectKinematics = {kinematic data}

# GPS scores for the subject relative to the reference group average kinematics
subjectGPS = calculateGPS(referenceKinematics, subjectKinematics).gps
```

## Plotting the GPS diagram

```
from gpscalculator import plotGPS

plot = plotGPS(referenceGPS, subjectGPS, saveplot="test_gps_plot.png")
```

## Processessing the GPS scores for a subject group

```
from gpscalculator import batchGPS

# List of paths to the subject group kinematics JSON files
subjectPaths = [...]

subjectGroup = batchGPS()
subjectGroup.loadReferenceGroup(referencePaths)
subjectGroup.processSubjectGroup(subjectPaths)

# Print the dataframe containing the subject group GPS data
print(subjectGroup.batchData)
```
