# Gait Profile Score Calculator

## Calculate
'''python
from gpscalculator import GPSData

subpath = "path to subject kinematics json"
refdir = "path to directory of referecne kinematics jsons"

GPS = GPSData(subpath, refdir)

# Print GPS data for subject relative to the reference group
print(GPS.GPS_SCORE)

# Plot and save the Movement Analysis Profile
subjname = "name or reference for the subject"
outputdir = "path to directory where the plot is to be saved"

GPS.plot_data(subjname, outputdir)
'''
## Check required json structure for kinematics
'''python
from gpscalculator import create_example_kinematicsJSON

Creates a json file in the correct format locally
create_example_kinematicsJSON()
'''
## Check the kinematics variable labels used
'''python
from gpscalculator import check_variable_names

# Prints the kinematic variable labeles used and returns a list of them
check_variable_names()
'''