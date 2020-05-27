''' purpose: Converts a FEniCS model from *.xml to *.h5
    author: Mario Fleischer, mario.fleischer@charite.de

    remarks: 1) output (*.h5) is essential for parallel run using mpirun
'''


from dolfin import *
import sys

model_name = sys.argv[1] # taken from shell argument

mesh = Mesh(model_name+".xml") # loading *.xml-model
boundaries = MeshFunction("size_t", mesh, model_name+ "_facet_region.xml") # read boundaries
subdomains  = MeshFunction("size_t", mesh, model_name+"_physical_region.xml") # read subdomains
hdf = HDF5File(mesh.mpi_comm(), model_name+".h5", "w") # open *.h5-file
hdf.write(mesh, "/mesh") # write mesh
hdf.write(subdomains, "/subdomains") # write subdomain(s)
hdf.write(boundaries, "/boundaries") # write boundaries
