import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def get_dir_filepaths(directorypath):
    """
    This function appends the absolute file paths from within a directory.

        Args:
            directorypath(string): Path to the directory
        Returns:
            dirpaths(list): List of file paths from within the directory 
    """

    paths = os.listdir(directorypath)
    dirpaths = []

    for path in paths:
        dirpaths.append("{}\\{}".format(directorypath, path))
    return dirpaths

def blankKinematicsDict():
    """ Returns a dictionary template for the kinematic variables, with 100 samples. """

    blankKINS = {
            'Pelvic Tilt Left': [0]*100, 
            'Pelvic Tilt Right': [0]*100, 
            'Hip Flexion Left': [0]*100, 
            'Hip Flexion Right': [0]*100, 
            'Knee Flexion Left': [0]*100, 
            'Knee Flexion Right': [0]*100, 
            'Ankle Dorsiflexion Left': [0]*100, 
            'Ankle Dorsiflexion Right': [0]*100, 
            'Pelvic Obliquity Left': [0]*100, 
            'Pelvic Obliquity Right': [0]*100, 
            'Hip Abduction Left': [0]*100, 
            'Hip Abduction Right': [0]*100, 
            'Pelvic Rotation Left': [0]*100, 
            'Pelvic Rotation Right': [0]*100, 
            'Hip Rotation Left': [0]*100, 
            'Hip Rotation Right': [0]*100, 
            'Foot Progression Left': [0]*100, 
            'Foot Progression Right': [0]*100
        }
    return blankKINS

def blankGPSdict():
    blankGPS = {
            'Pelvic Tilt Left': 0, 
            'Pelvic Tilt Right': 0, 
            'Hip Flexion Left': 0, 
            'Hip Flexion Right': 0, 
            'Knee Flexion Left': 0, 
            'Knee Flexion Right': 0, 
            'Ankle Dorsiflexion Left': 0, 
            'Ankle Dorsiflexion Right': 0, 
            'Pelvic Obliquity Left': 0, 
            'Pelvic Obliquity Right': 0, 
            'Hip Abduction Left': 0, 
            'Hip Abduction Right': 0, 
            'Pelvic Rotation Left': 0, 
            'Pelvic Rotation Right': 0, 
            'Hip Rotation Left': 0, 
            'Hip Rotation Right': 0, 
            'Foot Progression Left': 0, 
            'Foot Progression Right': 0,
            'GPS': 0,
            'GPS Left': 0,
            'GPS Right': 0
        }
    return blankGPS

def rootMeanSquare(reference, subject):
    """ Calculates the root mean square of two list. """

    sumSquares = 0
    for i in range(len(reference)):
        sumSquares += (reference[i]-subject[i])**2
    
    rmsVal = (sumSquares/len(reference))**0.5
    return rmsVal

def calculateGPSvalues(reference_dataset, subject_dataset):
    """ Calculates the GPS and MAP of a subjects kinematics relative to a reference kinematics. """

    gpsValues = {}
    for key in reference_dataset:
        gpsValues[key] = rootMeanSquare(reference_dataset[key], subject_dataset[key])
    
    gps = 0
    gpsL = 0
    gpsR = 0

    for key in gpsValues:
        gps +=  gpsValues[key]

        if "Left" in key:
            gpsL +=  gpsValues[key]
        elif "Right" in key:
            gpsR +=  gpsValues[key]
        else:
            pass
    
    gpsValues["GPS"] = gps/len(reference_dataset)
    gpsValues["GPS Left"] = gpsL/(len(reference_dataset)/2)
    gpsValues["GPS Right"] = gpsR/(len(reference_dataset)/2)
    return gpsValues

def check_variable_names():
    kin_vars = [
        'Pelvic Tilt Left','Pelvic Tilt Right', 'Hip Flexion Left','Hip Flexion Right', 
        'Knee Flexion Left','Knee Flexion Right', 'Ankle Dorsiflexion Left','Ankle Dorsiflexion Right', 
        'Pelvic Obliquity Left','Pelvic Obliquity Right','Hip Abduction Left','Hip Abduction Right','Pelvic Rotation Left', 
        'Pelvic Rotation Right','Hip Rotation Left','Hip Rotation Right','Foot Progression Left','Foot Progression Right']

    for var in kin_vars:
        print(var)
    return kin_vars

def create_example_kinematicsJSON():
    """
    This function produces a json in format required for the GPS calculator, use the same variable headings.  
    """

    kin_vars = [
        'Pelvic Tilt Left','Pelvic Tilt Right', 'Hip Flexion Left','Hip Flexion Right', 
        'Knee Flexion Left','Knee Flexion Right', 'Ankle Dorsiflexion Left','Ankle Dorsiflexion Right', 
        'Pelvic Obliquity Left','Pelvic Obliquity Right','Hip Abduction Left','Hip Abduction Right','Pelvic Rotation Left', 
        'Pelvic Rotation Right','Hip Rotation Left','Hip Rotation Right','Foot Progression Left','Foot Progression Right']

    KINEMATICS = {}

    for var in kin_vars:
        KINEMATICS[var] = list(np.sin(np.arange(0,100,1)))
    
    with open('example_kinematics.json', 'w') as fp:
        json.dump(KINEMATICS, fp)
    return 

def __check_KINEMATICS_dict(KINEMATICS):
    """
    This fucntion checks the KINEMATICS dictionary object to ensure it has the correct data.

        Args:

        Returns:
            (Boolean): True if datas correct, False if there is more/less data than required 
    """
    kin_vars = [
        'Pelvic Tilt Left','Pelvic Tilt Right', 'Hip Flexion Left','Hip Flexion Right', 
        'Knee Flexion Left','Knee Flexion Right', 'Ankle Dorsiflexion Left','Ankle Dorsiflexion Right', 
        'Pelvic Obliquity Left','Pelvic Obliquity Right','Hip Abduction Left','Hip Abduction Right','Pelvic Rotation Left', 
        'Pelvic Rotation Right','Hip Rotation Left','Hip Rotation Right','Foot Progression Left','Foot Progression Right']
    
    # Check there are all the kinematic variables
    if len(KINEMATICS)==18:
        for key in KINEMATICS:
            # Check there are 100 data points for each variable
            if len(KINEMATICS[key])!=100:
                print("Variable {} has {} datapoints".format(key, len(KINEMATICS[key])))
                print("Check input data file!")
                return False
            else:
                pass
        return True
    else: 
        print("Kinematic dictionary has {} variables".format(len(KINEMATICS)))
        print("Check input data file!")
        return False
    
def load_kinematic_data(filepath):
    """
    This function opens a JSON file and returns a dictionary containing the kinematic data from a single cycle of a gait trial.
        The file should store a dictionary containing the 18 kinematic variables required - 
            ['Pelvic Tilt Left','Pelvic Tilt Right','Hip Flexion Left','Hip Flexion Right',
            'Knee Flexion Left','Knee Flexion Right','Ankle Dorsiflexion Left',
            'Ankle Dorsiflexion Right','Pelvic Obliquity Left','Pelvic Obliquity Right',
            'Hip Abduction Left','Hip Abduction Right','Pelvic Rotation Left',
            'Pelvic Rotation Right','Hip Rotation Left','Hip Rotation Right',
            'Foot Progression Left','Foot Progression Right'] 
            
            Each variable should have 100 data points sampled throughout the gait cycle (1% intervals).

        Args:
            filepath(string): Absolute or relative path to the kinematic data JSON file.
        Returns:
            KINEMATICS(dictionary): Kinematic data required to calculate the GPS
    """

    with open(filepath) as f:
        KINEMATICS = json.load(f)
    
    # Check dictionary
    if (__check_KINEMATICS_dict(KINEMATICS)==True):
        return KINEMATICS
    else:
        print("Check input data file!")
        return

def group_average_kinematics(directorypath):
    """
    This function calculates the mean value for each datapoint of each kinematic variable.
    All files within the directory are used to form the avergage.

        Args:
            directorypath(string): Path to the group directory
        Returns:
            AVG_KINEMATICS(dictionary): Dictionary containing the average values for each datapoint of the kinematic variables
    """
    directorypaths = get_dir_filepaths(directorypath)

    AVG_KINEMATICS = blankKinematicsDict()

    # Cycle through files in reference directory folder
    for filepath in directorypaths:
        kinematic_data = load_kinematic_data(filepath)

        # Add the value at each sample point to the reference set
        for key, value in kinematic_data.items():
            for i in range(len(value)):
                AVG_KINEMATICS[key][i] += value[i]
    
    for key, value in AVG_KINEMATICS.items():
        for i in range(len(value)):
            AVG_KINEMATICS[key][i] = value[i]/len(directorypaths)
    return AVG_KINEMATICS

def group_kinematics_stdev(directorypath, AVG_KINEMATICS):
    """
    This function calculates the average of the standard deviation of the kinematics of the reference group relative to the average of the reference group.
    All files within the directory are used to form the average of the standard deviation.

        Args:
            directorypath(string): Path to the group directory
        Returns:
            REF_GPS(dictionary): Dictionary containing the average standard deviation of the kinematic variables 
    """

    directorypaths = get_dir_filepaths(directorypath)

    STDEV_GPS = blankGPSdict()

    # Cycle through list of reference file paths
    for path in directorypaths:
        kinematics = load_kinematic_data(path)

        # Calculate GPS
        gpsValues = calculateGPSvalues(AVG_KINEMATICS, kinematics)

        # Add GPS to STDEV_GPS
        for key in gpsValues:
            tot_gps_val = STDEV_GPS[key]+gpsValues[key]
            STDEV_GPS[key] = tot_gps_val
    
    # average stdevGPS
    for key, value in gpsValues.items():
        STDEV_GPS[key] = (value/len(directorypaths))

    REF_GPS = {}
    REF_GPS['Pelvic Tilt'] = np.round((STDEV_GPS['Pelvic Tilt Left'] + STDEV_GPS['Pelvic Tilt Right'])/2, 3) 
    REF_GPS['Hip Flexion'] = np.round((STDEV_GPS['Hip Flexion Left'] + STDEV_GPS['Hip Flexion Right'])/2, 3) 
    REF_GPS['Knee Flexion'] = np.round((STDEV_GPS['Knee Flexion Left'] + STDEV_GPS['Knee Flexion Right'])/2 , 3)
    REF_GPS['Ankle Dorsiflexion'] = np.round((STDEV_GPS['Ankle Dorsiflexion Left'] + STDEV_GPS['Ankle Dorsiflexion Right'])/2, 3) 
    REF_GPS['Pelvic Obliquity'] = np.round((STDEV_GPS['Pelvic Obliquity Left'] + STDEV_GPS['Pelvic Obliquity Right'])/2 , 3)
    REF_GPS['Hip Abduction'] = np.round((STDEV_GPS['Hip Abduction Left'] + STDEV_GPS['Hip Abduction Right'])/2 , 3)
    REF_GPS['Pelvic Rotation'] = np.round((STDEV_GPS['Pelvic Rotation Left'] + STDEV_GPS['Pelvic Rotation Right'])/2 , 3)
    REF_GPS['Hip Rotation'] = np.round((STDEV_GPS['Hip Rotation Left'] + STDEV_GPS['Hip Rotation Right'])/2, 3)
    REF_GPS['Foot Progression']  = np.round((STDEV_GPS['Foot Progression Left'] + STDEV_GPS['Foot Progression Right'])/2, 3)
    REF_GPS['GPS']  = np.round((STDEV_GPS['GPS']), 3)

    return REF_GPS

def calculate_GPS(subjectpath, AVG_KINEMATICS):
    """
    This fucntion calculates the GPS and MAP values for a subject, producing a dictionary.

        Args:
            subjectpath(string): The path to the subject kinematics JSON.
            AVG_KINEMATICS(dictionary): The dictionary containing the average kinematic data for the reference group
        Returns:
            SUB_GPS(dictionary): The dictionary containing the subjects GPS values calculated relative to the reference group
    """
    
    sub_kinematics = load_kinematic_data(subjectpath)
    SUB_GPS = calculateGPSvalues(sub_kinematics, AVG_KINEMATICS)

    return SUB_GPS

def plot_GPS(sub_name, SUB_GPS, REF_GPS, output_directory):
    """
    This function plots the GPS and MAP for the subject relative to the reference group.

        Args:
            sub_name(string): Name of the subject (or subject reference)
            SUB_GPS(dictionary): The dictionary containing the subjects GPS values
            REF_GPS(dictionary): The dictionary containing the standard deviation of the GPS values of the reference group
            output_directory(string): The path to the folder where the plot is to be saved

        Returns:
            None
    """
    filename = "{}\\{}_gps_plot.png".format(output_directory, sub_name)

    ticks = ['Pel tilt', 'Hip flex', 'Knee flex', 'Ank dors', 'Pel obl', 'Hip abd', 'Pel rot', 'Hip rot', 'Foot prog', None,  'GPS']

    left_vals = [SUB_GPS['Pelvic Tilt Left'], SUB_GPS['Hip Flexion Left'], SUB_GPS['Knee Flexion Left'], SUB_GPS['Ankle Dorsiflexion Left'], SUB_GPS['Pelvic Obliquity Left'], SUB_GPS['Hip Abduction Left'], SUB_GPS['Pelvic Rotation Left'], SUB_GPS['Hip Rotation Left'], SUB_GPS['Foot Progression Left'], 0, SUB_GPS['GPS Left']]
    right_vals = [SUB_GPS['Pelvic Tilt Right'], SUB_GPS['Hip Flexion Right'], SUB_GPS['Knee Flexion Right'], SUB_GPS['Ankle Dorsiflexion Right'], SUB_GPS['Pelvic Obliquity Right'], SUB_GPS['Hip Abduction Right'], SUB_GPS['Pelvic Rotation Right'], SUB_GPS['Hip Rotation Right'], SUB_GPS['Foot Progression Right'], 0, SUB_GPS['GPS Right']]
    ref_vals =  [REF_GPS['Pelvic Tilt'], REF_GPS['Hip Flexion'], REF_GPS['Knee Flexion'], REF_GPS['Ankle Dorsiflexion'], REF_GPS['Pelvic Obliquity'], REF_GPS['Hip Abduction'], REF_GPS['Pelvic Rotation'], REF_GPS['Hip Rotation'], REF_GPS['Foot Progression'], 0, REF_GPS['GPS']]

    # First number sets the width of the left/right bars
    width = 0.35
    ref_widths, widths, pos_l, pos_r = [], [] , [], []
    x = np.arange(len(left_vals))

    # Set widths and positions for GVS vars
    for i in range(len(x)-1):
        widths.append(width)
        ref_widths.append(2*width)
        pos_l.append(x[i]-width/2)
        pos_r.append(x[i]+width/2)
    
    # Set width and position for GPS vars
    widths.append((width*2)/3)
    pos_l.append(x[-1]-(width*2)/3)
    pos_r.append(x[-1])

    ref_widths.append(width*2)
    
    # value, width, position for overall gps 
    overall_gps = [SUB_GPS['GPS'], (width*2)/3, x[-1]+(width*2)/3]

    fig, ax = plt.subplots()

    rects1 = ax.bar(pos_l, height=left_vals, width=widths, label='Left')
    rects2 = ax.bar(pos_r, height=right_vals, width=widths, label='Right')
    rectsOVR = ax.bar(overall_gps[2], height=overall_gps[0], width=overall_gps[1], label="Overall")
    rectsREF = ax.bar(x, height=ref_vals, width=ref_widths, label='No pathology', zorder=1)

    ax.set_ylabel('RMS difference (deg)')
    ax.set_title('{} Gait Profile Score'.format(sub_name))
    ax.set_xticks(x)
    ax.set_xticklabels(ticks, rotation=45, ha='right')
    ax.legend()
    fig.show()

    fig.savefig(filename)
    return

class GPSData:

    def __init__(self,subjectpath, directorypath):
        """
        The directory path is used to collect the kinemtatics from the reference group, subject and calculate the GPS.
        """
        self.subjectpath = subjectpath
        self.directorypath = directorypath

        self.get_subject_gps()

    def get_subject_gps(self):
        """
        This function calculates the average kinematics of the reference group, the average standard deviation of the reference group relative to the average kinematics.
        The GPS score for the subject is calculated
        """

        self.AVG_KINEMATICS = group_average_kinematics(self.directorypath)

        self.REF_GPS = group_kinematics_stdev(self.directorypath, self.AVG_KINEMATICS)

        self.GPS_SCORE = calculate_GPS(self.subjectpath, self.AVG_KINEMATICS)

    def plot_data(self, subjectname, outputdirectory):
        """
        The subjects GPS and MAP is plotted against the average of the reference group
        """
        plot_GPS(subjectname, self.GPS_SCORE, self.REF_GPS, outputdirectory)

    def GPSData_to_JSON(self, subjectname, outputdirectory):

        self.GPS_SCORE["Subject_path"] = self.subjectpath
        self.GPS_SCORE["Subject_name"] = subjectname

        with open("{}\\{}_GPS.json".format(outputdirectory, subjectname), 'w') as f:
            json.dump(self.GPS_SCORE, f)
        return


class GPSDataBatch:

    def __init__(self,subjectdirectorypath, referencedirectorypath, outputdirectory, subjectgroup="Subjects"):

        self.subjectDIR = subjectdirectorypath
        self.referenceDIR = referencedirectorypath
        self.outputdirectory = outputdirectory
        self.subjectgroup = subjectgroup

        self.subjectPATHS = get_dir_filepaths(self.subjectDIR)

        # Calculate the average kinematics and the standard deviation of the reference group relative to the average kinematics
        self.process_reference_group()

        self.calculate_subject_group_GPS()

        return

    def process_reference_group(self):
        """
        This method calculates the average kinematics of the reference group and the standard deviation of the reference group relative to the average kinematics
        """
        self.AVG_KINEMATICS = group_average_kinematics(self.referenceDIR)

        self.REF_GPS = group_kinematics_stdev(self.referenceDIR, self.AVG_KINEMATICS)
        return
    
    def calculate_subject_group_GPS(self):

        cols = ['Subject_path','Subject', 'Pelvic Tilt Left', 'Pelvic Tilt Right', 'Hip Flexion Left', 'Hip Flexion Right', 'Knee Flexion Left', 'Knee Flexion Right', 'Ankle Dorsiflexion Left', 'Ankle Dorsiflexion Right', 'Pelvic Obliquity Left', 'Pelvic Obliquity Right', 'Hip Abduction Left',  'Hip Abduction Right', 
            'Pelvic Rotation Left', 'Pelvic Rotation Right', 'Hip Rotation Left', 'Hip Rotation Right', 'Foot Progression Left', 'Foot Progression Right', 'GPS','GPS Left', 'GPS Right']

        self.GPS_batch = pd.DataFrame(data=None, columns=cols)

        for i, subjectPATH in enumerate(self.subjectPATHS):

            gps_data = calculate_GPS(subjectPATH, self.AVG_KINEMATICS)

            gps_data["Subject_path"] = subjectPATH
            gps_data["Subject"] = (subjectPATH.split("\\")[-1]).split(".")[0]

            self.GPS_batch = self.GPS_batch.append(gps_data, ignore_index=True)
        return
    
    def save_batch_data(self):
        """
        This method saves the 
        """

        self.GPS_batch.to_csv("{}\\{}_GPS_Data.csv".format(self.outputdirectory, self.subjectgroup), index=False)
        return


        
