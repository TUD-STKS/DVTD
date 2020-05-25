# DVTD
Dresden Vocal Tract Dataset - supplemental code

The scripts in this repository are supplemental code to the Dresden Vocal Tract Dataset published on figshare.

## Requirements
For the MATLAB scripts, you theoretically need the Bioinformatics Toolbox. However, only the helper function suptitle() in line 232 is not a built-in function, so if you do not own that Toolbox you can comment that line out and should be fine.

The Python scripts were written using Python 3. You can install the dependencies using pip install requirements.txt

## Installing
Simply download or clone the files from the repository and **move them to their own subfolder in the DVTD directory** (e.g., DVTD/scripts). If the scripts are not run from a subfolder of the DVTD at the same depth as the subject data, you will get "file not found" error and need to either adjust the path to the subject data in the scripts or move the scripts to the correct location. 

## File description
- ``display_data.m``: Script to display the measured and simulated transfer functions of all models (MATLAB version)
- ``display_data.py``: Script to display the measured and simulated transfer functions of all models (Python 3 version)

