''' purpose: Definition of subject and model name (strictly dependent on the paths in the DVTD folder!)
    author: Mario Fleischer, mario.fleischer@charite.de

    remarks: coordinates in brackets were taken from the center of the lip opening area by picking manually using ParaView (www.paraview.org)
'''

# load externally defined dictionary
info="./model_names.py" # should be in the root directory (otherwise change path)
exec(open(info).read())

# =====================================================================
# =====================================================================

# choose subject and model wanted to analyze
subject = list(MODEL_NAME)[0] # see ./model_names.py for possible IDs
model_name = list(MODEL_NAME[subject])[0] # see ./model_names.py for possible IDs
print(f'model to be solved: {subject}, {model_name}')

# define frequency on which solution is requested
freqmin = 0.0 # minimal frequency in kHz
freqincr = 0.000961304 # frequency increment in kHz
freqmax = 10. # maximum frequency in kHz

# Material property values at 22°C
c = 345.0 # speed of sound in m/s
rho = 1.18 # density of air in kg/m^3

# boundary condition values at the glottis
V0_r  = -1.0 # real part of particle velocity at glottis ('minus' means invard)
V0_i  =  0.0 # imaginary part of particle velocity at glottis

# boundary condition values at vocal tract wall
Zwall_r  = 500.0*c*rho # real part, taken from Fleischer et al. (2018), PLoS ONE
Zwall_i  = 0.0 # imaginary part
# =====================================================================
# =====================================================================
