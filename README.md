# Gait Profile Score Calculator

gpscalc is a package that can be used to calculate the gait profile score as stated in Baker et al. 2009. The package requires the gait trials kinematic data to be stored in a json file using specific variable names.

(Baker, R. et al., 2009. The Gait Profile Score and Movement Analysis Profile. Gait and Posture, 30(1), pp. 265-269.)

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

## Check required json structure for kinematics
from gpscalculator import create_example_kinematicsJSON

Creates a json file in the correct format locally
create_example_kinematicsJSON()

## Check the kinematics variable labels used
from gpscalculator import check_variable_names

### Prints the kinematic variable labeles used and returns a list of them
check_variable_names()
