''' purpose: Solving the Helmholtz equation with FEniCS
    author: Mario Fleischer, mario.fleischer@charite.de
    
    remarks:    1) python 3.6 or higher is needed
                      2) fenics 2017.2 or higher is needed
''' 
# loading python modules
import numpy as np
import os
from packaging import version
import time


from dolfin import *
import dolfin
import modules # user defined moduls shipped from authors (should be in the root directory, otherwise change path)


# load externally user defined values
definitions = "./definitions.py" # should be in the root directory (otherwise change path)
exec(open(definitions).read())


# check dolfin verion and ensure version independence
if version.parse(dolfin.__version__) < version.parse('2018.1.0'):
    set_log_level(ERROR)
    rank = mpi_comm_world().rank
elif version.parse(dolfin.__version__) >= version.parse('2018.1.0'):
    set_log_level(LogLevel.ERROR)
    rank = MPI.comm_world.rank

# read coordinates of the point centered at the lip opening
point_at_lips = MODEL_NAME[subject][model_name]

# define working directory
subdir_name = f'/../{subject}/{model_name}'
wdir = os.getcwd()+subdir_name
print(f'{wdir}')

# create numpy array for the frequencies based on initially defined values
frequencies = (np.arange(1+np.int(freqmax/freqincr))+1)*freqincr
index = (np.abs(frequencies-freqmin)).argmin()
frequencies = frequencies[index::]
frequencies = np.append(1e-10, frequencies)

# load H5-version of the model
mesh, ds, dx = modules.l_model_h5(f'{wdir}/{model_name}')

# calculate geometry values and write to file
Alips = assemble(1.0*ds(3)) # lip opening area in mm^2
Aglottis = assemble(1.0*ds(1)) # glottal area in mm^2
Awall = assemble(1.0*ds(2)) # wall area in mm^2
if subject != 'tube':
    Rlips = np.sqrt(Alips/(2.*np.pi)) # radius of a half-sphere with area Alips in mm
elif subject == 'tube':
    Rlips = np.sqrt(Alips/np.pi)

Vmodel = assemble(1.0*dx(1)) # Volume of the VT-cavity in mm^3
np.savetxt(f'{wdir}/geometrical_entities.dat', 
        np.transpose(np.vstack([Alips, Aglottis, Awall, Rlips, Vmodel])),
        fmt='%.18e', delimiter=' ', newline='\n',
        header='lip opening area in mm^2; glottal area in mm^2; wall area in mm^2; lip radius in mm; volume in mm^3')

# calculate element characteristics and write to file
elemsize = [c.h() for c in cells(mesh)]
np.savetxt(f'{wdir}/element_characteristics.dat',
        np.transpose(np.vstack([
                np.min(elemsize), 
                np.max(elemsize), 
                np.median(elemsize), 
                np.mean(elemsize)
                              ])),
        fmt='%.18e', delimiter=' ', newline='\n', 
        header='min elem size in mm; max elem size in mm; median elem size in mm, mean elem size in mm')


# define function space and polynomial degree of shape functions and write DOF to file
poly = 1 # polynomial degree of shape functions
V, p_r, p_i, q_r, q_i, pres = modules.h_fs(mesh, poly) # functions space
np.savetxt(f'{wdir}/dof.dat',
        [V.dim()], fmt='%i', delimiter=' ', newline='\n', header=f'degree of freedom')


# get node-ID at lip area depending on coordinates defined in 'point'
V_ind_xyz_1 = modules.fnnm(mesh, V, point_at_lips, 2.3, rank)
if V_ind_xyz_1 != []:
    p_ind = V_ind_xyz_1[0][0]


# initialisation of certain variables needed during run
Vlips = []
Vlips_phase = []

# calculate complex valued impedance boundary conditions at lips opening
k = (2*np.pi*frequencies)/float(c) # array of wave numbers
Zlips_r, Zlips_i = modules.wedge(float(c), 
                                    float(rho), 
                                    k, 
                                    Rlips) # array of impedance boundary conditions at lip opening (real and imaginary part)


# start timer
t0 = time.time()

# check wether resulting file exists (preventing overwriting previous results)
jj = 0   
if not os.path.exists(f'{wdir}/{model_name}-vvtf-calculated_{jj}.txt'):
    filID = jj
else:   
    while os.path.exists(f'{wdir}/{model_name}-vvtf-calculated_{jj}.txt'):
        jj=jj+1
        if not os.path.exists(f'{wdir}/{model_name}-vvtf-calculated_{jj}.txt'):
            filID = jj
            break


# iterate solution
for ii, freq in enumerate(frequencies):

    aH = modules.h_domain(k[ii],q_r,q_i,p_r,p_i) * dx(1) # bilinear form (Helmholtz equation)
    aWall = modules.h_imp(k[ii],
                          Constant(c),
                          Constant(rho),
                          Constant(Zwall_r), 
                          Constant(Zwall_i), 
                          q_r, q_i, p_r, p_i) * ds(2) # bilinear form (impedance boundary conditions at the wall)
    aLips = modules.h_imp(k[ii], 
                          Constant(c), 
                          Constant(rho), 
                          Constant(Zlips_r[ii]), 
                          Constant(Zlips_i[ii]), 
                          q_r, q_i, p_r, p_i) * ds(3) # bilinear form (impedance boundary conditions at the lip opening)
    
    a = aH+aWall+aLips # bilinear form
    

    L = (2.*np.pi*freq*Constant(rho)*Constant(V0_i)*q_r*ds(1) 
      - 2.*np.pi*freq*Constant(rho)*Constant(V0_r)*q_i*ds(1)) # linear form (considering particle velocity at glottal area)

    
    solve(a == L, pres,
          solver_parameters=dict(linear_solver='mumps', preconditioner='amg'))

    
    print(f'Process {rank}: solution time: {time.time() - t0} s (substep {ii+1}/{np.shape(frequencies)[0]})')

    pres_r, pres_i = pres.split(deepcopy=True) # split solution into real and imaginary part

    
    if 'p_ind' in locals():   
        pres_r_point = pres_r.vector().get_local()[p_ind] # pressure at 'point' (real part)
        pres_i_point = pres_i.vector().get_local()[p_ind] # pressure at 'point' (imaginary part)

        pres_point = complex(pres_r_point ,  pres_i_point) # complex valued pressure at 'point'
        Zlips = complex(float(Zlips_r[ii]), float(Zlips_i[ii])) # complex valued impedance at lips
                
        Vlips.append(np.absolute(pres_point/Zlips))
        Vlips_phase.append(np.angle(pres_point/Zlips))


#        writing VVTF
        np.savetxt(f'{wdir}/{model_name}-vvtf-calculated_{jj}.txt', 
            np.transpose(np.vstack([1e3*frequencies[:ii+1], 
                                    np.array(Vlips)/Vlips[0],
                                    np.array(Vlips_phase)
                                    ])),
            fmt='%.6f', delimiter=' ', newline='\n',
            header='freq_Hz magnitude phase_rad')






