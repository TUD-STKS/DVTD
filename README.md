# DVTD
Dresden Vocal Tract Dataset - supplemental code

The scripts in this repository are supplemental code to the [Dresden Vocal Tract Dataset published on figshare](https://figshare.com/s/5b81026892f7b39b429e).

## Requirements
For the MATLAB scripts, you theoretically need the Bioinformatics Toolbox. However, only the helper function suptitle() in line 232 is not a built-in function, so if you do not own that Toolbox you can comment that line out and should be fine.

The Python scripts were written using Python 3. To run ``display_data.py``, you will only need numpy and matplotlib. To perform FEM simulations, please refer to the installation instructions in the paper Birkholz *et al.*: "Printable 3D vocal tract shapes from MRI data and their acoustic and aerodynamic properties." 

## Installing
Simply download or clone the files from the repository and **move them to their own subfolder in the DVTD directory** (e.g., ``DVTD/misc``). If the scripts are not run from a subfolder of the DVTD at the same depth as the subject data, you will get "file not found" errors and need to either adjust the path to the subject data in the scripts or move the scripts to the correct location. 

## File description
- ``display_data.m``: Script to display the measured and simulated transfer functions of all models (MATLAB version)
- ``display_data.py``: Script to display the measured and simulated transfer functions of all models (Python 3 version)
- ``definitions.py``: Definition of subject and model name (strictly dependent on the paths in the DVTD folder!)
- ``fem_run.py``: Solving the Helmholtz equation with FEniCS
- ``model_names.py``: Subject and model IDs (strictly dependent on the paths in the DVTD folder!)
- ``modules.py``: Modules called by ``fem_rum.py``
- ``to_h5_module.py``: Converts a FEniCS model from ``*.xml`` to ``*.h5``
