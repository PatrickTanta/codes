import firedrake as fd
import numpy as np
from slepc4py import SLEPc
from firedrake.petsc import PETSc

Lx = 1.
Ly = Lx/2.
Lz = Lx/3.
mesh = fd.utility_meshes.RectangleMesh(nx=30, ny=15, Lx=Lx, Ly=Ly,
                                       quadrilateral=True)
nz = 10
mesh = fd.ExtrudedMesh(mesh, layers=nz, layer_height=Lz/nz)

# We need to decide on the function space in which we'd like to solve the
# problem. Let's use piecewise linear functions continuous between
# elements::

V = fd.FunctionSpace(mesh, "CG", 1)
W = fd.TensorFunctionSpace(mesh, "CG", 1)

# We'll also need the test and trial functions corresponding to this
# function space::

u = fd.TrialFunction(V)
v = fd.TestFunction(V)

# We declare a function over our function space and give it the
# value of our right hand side function::


# Permeability tensor
# Homogeneous
one = fd.Constant(1.0)
zero = fd.Constant(0.0)
Khom = fd.interpolate(one, V)
Khom.rename('K', 'Permeability')

# Heterogeneous
x, y, z = fd.SpatialCoordinate(W.mesh()) 
fx = fd.pi/Lx/2
fy = fd.pi/Ly/2
fz = fd.pi/Lz

Khet = fd.as_tensor(((1.0 + x, 0, 0), 
                      (0, 1.0+y, 0),
                       (0, 0, 1.0+z)))

#Khet = fd.as_tensor(((1,0,0),(0,1,0),(0,0,1)))
#Khet = fd.as_tensor(((1,0),(0,1)))
Khet = fd.Function(W).interpolate(Khet)
Khet.rename('K', 'Permeability')

# Porosity
por = fd.Constant(1.0)

# We can now define the bilinear and linear forms for the left and right
# hand sides of our equation respectively::
dx = fd.dx
a = (fd.dot(Khet * fd.grad(u), fd.grad(v))) * dx
m = u * v * por * dx

# Defining the eigenvalue problem

petsc_a = fd.assemble(a).M.handle
petsc_m = fd.assemble(m).M.handle

num_eigenvalues = 20

# Set solver options
opts = PETSc.Options()
opts.setValue("eps_gen_hermitian", None)
#opts.setValue("st_pc_factor_shift_type", "NONZERO")
opts.setValue("eps_type", "krylovschur")
#opts.setValue("eps_smallest_magnitude", None)
opts.setValue("eps_target_magnitude", None)
opts.setValue("eps_target", 1e-8)
opts.setValue("eps_tol", 1e-10)

# Solve for eigenvalues
es = SLEPc.EPS().create()
es.setDimensions(num_eigenvalues)
es.setOperators(petsc_a, petsc_m)
es.setFromOptions()
es.solve()

# Number of converged eigenvalues
nconv = es.getConverged()
eigvecs = []
for i in range(nconv):
    print(es.getEigenvalue(i).real)
    
    vr, vi = petsc_a.getVecs()
    lam = es.getEigenpair(i, vr, vi)
    
    eigvecs.append(fd.Function(V))
    eigvecs[-1].vector()[:] = vr
    eigvecs[-1].rename('eigvec'+str('{:2d}').format(i))

Print = PETSc.Sys.Print

Print()
Print("******************************")
Print("*** SLEPc Solution Results ***")
Print("******************************")
Print()

its = es.getIterationNumber()
Print("Number of iterations of the method: %d" % its)

eps_type = es.getType()
Print("Solution method: %s" % eps_type)

nev, ncv, mpd = es.getDimensions()
Print("Number of requested eigenvalues: %d" % nev)

tol, maxit = es.getTolerances()
Print("Stopping condition: tol=%.4g, maxit=%d" % (tol, maxit))

# For more details on how to specify solver parameters, see the section
# of the manual on :doc:`solving PDEs <../solving-interface>`.
#
# Next, we might want to look at the result, so we output our solution
# to a file::

fd.File("helmholtz.pvd").write(Khet, *eigvecs)
