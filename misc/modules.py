''' Modules called by fem_run.py
    author: Mario Fleischer, mario.fleischer@charite.de
    
    remarks:    1) fenics 2017.2 or higher is needed
''' 

from dolfin import *
import numpy as np
from scipy import spatial

# ==========================================================================================
def l_model_h5(model_name): 
#    purpose: loading *.hf model into working space and reading IDs for further processing
#    input: model_name (string, filname of the *.h5 model WITHOUT file extensions)
#    output: mesh (mesh object)
#            ds (IDs of surface areas (originally defined in *.geo)
#            dx (IDs of domains (originally defined in *.geo)
#    see https://fenicsproject.org/tutorial/ for deeper insides    
    mesh = Mesh()
    hdf = HDF5File(mesh.mpi_comm(), model_name+".h5", "r")
    hdf.read(mesh, "/mesh", False)
    subdomains = MeshFunction("size_t", mesh, mesh.topology().dim())
    hdf.read(subdomains, "/subdomains")
    boundary = MeshFunction('size_t', mesh, mesh.topology().dim() - 1)
    hdf.read(boundary, "/boundaries")
    ds = Measure("ds", domain=mesh, subdomain_data=boundary)
    dx = Measure("dx", domain=mesh, subdomain_data=subdomains)
    return mesh, ds, dx
# ==========================================================================================

# ==========================================================================================
def h_fs(mesh, deg):
#    purpose: creating function space, test- and trialfunctions
#    input: mesh (mesh-object; coming from module l_model_h5)
#            deg (integer; polynomial degree for shape functions)
#    output: V (scalar valued mixed function space for real and imaginary part seperately)
#            p_r, p_i (trial functions for acoustic pressure, real and imaginary part)
#            q_r, q_i (test functions for acoustic pressure, real and imaginary part)
#            pres ()
#    see https://fenicsproject.org/tutorial/ for deeper insides
    el = FiniteElement("CG", mesh.ufl_cell(), deg) # Continous Galerkin element of dimension 'mesh.ufl_cell()' and degree 'deg'
    V = FunctionSpace(mesh, MixedElement([el,el])) # Hybrid functionsspace containing the real and imaginary part of the solution
    p_r, p_i = TrialFunctions(V)
    q_r, q_i = TestFunctions(V)
    pres = Function(V)
    return V, p_r, p_i, q_r, q_i, pres
# ==========================================================================================

# ==========================================================================================
def h_domain(k,q_r,q_i,p_r,p_i):
#    purpose: defining the weak form of the Helmholtz-Equation (domain)
#    input: k (float, wave number)
#           p_r, p_i (trial functions from module h_fs)
#           q_r, q_i (test functions from module h_fs)
#    output: hd (weak form)
    ksqr = Constant(k**2)
    hd = (-ksqr * (inner(q_r, p_r) + inner(q_i, p_i)) + \
    	  inner(nabla_grad(q_r), nabla_grad(p_r)) + \
    	  inner(nabla_grad(q_i), nabla_grad(p_i))
    )
    return hd
# ==========================================================================================

# ==========================================================================================
def wedge(c, rho, k, a):
#    purpose: calculating real & imaginary part of impedance boundary conditions capable to force spherical waves be absorpted
#    input: k (float, wave number)
#           c (float, speed of sound in m/s)
#           rho (float, density of air in kg/m^3)
#           a (float, radius of the sphere)
#    output: z_r, z_i (floats, real & imaginary part of impedance b.c.)
    ka = k*a
    z_r = rho*c * ((ka**2)/(1+(ka)**2))
    z_i = rho*c * (ka/(1+(ka)**2))
    return z_r, z_i
# ==========================================================================================
   
# ==========================================================================================
def h_imp(k, c, rho, zr, zi, q_r, q_i, p_r, p_i):
#    purpose: defining the weak form of impedance boundary conditions
#    input: k (float, wave number)
#           c (float, speed of sound in m/s)
#           rho (float, density in kg/m^3)
#           z_r, z_i (floats, impedance boundary conditions; real & imaginary part, taken from module 'wedge')
#           p_r, p_i (trial functions from module h_fs)
#           q_r, q_i (test functions from module h_fs)           
#    output: himp (weak form)
    if zr == 0.0 and zi == 0.0:
        const = Constant(0.0)
    elif zr != 0.0 or zi != 0.0:
        const = Constant(k*c*rho/(zr**2+zi**2))
    himp = const * \
            (zr * (inner(q_i, p_r) - inner(q_r, p_i)) + \
             zi * (inner(q_r, p_r) + inner(q_i, p_i)) \
        )
    return himp
# ========================================================================================== 
    

# ==========================================================================================
def fnnm(mesh, V, XYZ, tol, rank):
#    purpose: find nearest node to a given array of coordinates (generic function)
#    input: mesh (mesh-object; coming from module l_model_h5)
#           V (function space; from module h_fs)
#           XYZ (array containing triple of coordinates; defined in model_names.py)
#           tol (float, defining the maximal searching distance)
#           rank (integer, sub-process of parallel run)
#    output: V_ind_xyz (array containing index of node (integer) & array of coordinates of nearest node (float); for all sub-spaces seperately determined)
    V_dofs = V.tabulate_dof_coordinates().reshape(-1,mesh.geometry().dim()) # coordinates of all nodes in discrete function space
    V_len = len(V.split()) # number of function spaces defined
    p = 0
    sp_dofs = []  
    V_ind_xyz = []
    startindizes = []
    if len(list(range(V_len))) > 0: 
        for n in range(V_len): # scanning sub-spaces individually
            if V.sub(n).num_sub_spaces() == 0:  # only scalar valued function spaces will be analyzed
                p += 1
                sp_dofs_sp = V.sub(n).dofmap().dofs() # all DOFs of sub-space
                startindizes.append(np.min(sp_dofs_sp)) # find smallest DOF
                sp_dofs.append(sp_dofs_sp) # DOFs for all sub-spaces in ascending order

        startindex = np.min(startindizes) # smallest index, NOT zero by using mpirun
        for nnn in range(np.shape(sp_dofs)[0]):
            sp_dofs[nnn] = sp_dofs[nnn]-startindex # shifting DOFs (needed for mpirun)
            distance, index = spatial.KDTree(V_dofs[sp_dofs[nnn], :]).query(XYZ) # find closest node
            if distance <= tol: # check if distance is lower than tolerance
                V_ind_xyz.append([index, V_dofs[sp_dofs[nnn], :][index]]) # write coordinates
    return V_ind_xyz
# ==========================================================================================    
