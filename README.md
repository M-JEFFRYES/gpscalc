# Gait Profile Score Calculator

gpscalc is a package that can be used to calculate the gait profile score as stated in Baker et al. 2009. The package requires the gait trials kinematic data to be stored in a json file using specific variable names.

(Baker, R. et al., 2009. The Gait Profile Score and Movement Analysis Profile. Gait and Posture, 30(1), pp. 265-269.)

Kinematic gait data has to be in a specific format for the calculation, the specifics of the format required can be seen using the functions below to create example JSON files. 

# Using gpscalculator

## Installation

pip install gait-profile-score

## Check the json format required for the gait trial kinematics

from gpscalculator import create_example_kinematicsJSON, check_variable_names

create_example_kinematicsJSON()

check_variable_names()


## Calculate GPS

from gpscalculator import GPSData

subpath = "path to subject kinematics json"

refdir = "path to directory of referecne kinematics jsons"

GPS = GPSData(subpath, refdir)

### Print GPS data for subject relative to the reference group 
print(GPS.GPS_SCORE)

### Plot and save the Movement Analysis Profile
subjname = "name or reference for the subject"

outputdir = "path to directory where the plot is to be saved"

GPS.plot_data(subjname, outputdir) 

## Calculate the GPS for a group of subjects

from gpscalculator import GPSDataBatch

subdir = "path to directory contain the subject groups kinematics json files"

refdir = "path to directory of referecne kinematics jsons"

subjgroup = "name or reference for the subject group"

outputDIR = "path to directory where the subject groups GPS data is to be saved"

SubjectGroup_GPS = GPSDataBatch(subDIR, refDIR, outputDIR, subjectgroup)