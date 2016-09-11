#!/usr/bin/env python
from pylab import *
import os

f=open('blockMeshDict','w')
f.write('/*---------------------------------------------------------------------------*\ \n')
f.write('| =========                 |                                                 | \n')
f.write('| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           | \n')
f.write('|  \\    /   O peration     | Version:  1.4                                   | \n')
f.write('|   \\  /    A nd           | Web:      http://www.openfoam.org               | \n')
f.write('|    \\/     M anipulation  |                                                 | \n')
f.write('\*---------------------------------------------------------------------------*/ \n')
f.write('\n')
f.write('FoamFile \n')
f.write('{')
f.write('    version         2.0; \n')
f.write('    format          ascii; \n')
f.write('\n')
f.write('    root            "";\n')
f.write('    case            "";\n')
f.write('    instance        "";\n')
f.write('    local           "";\n')
f.write('\n')
f.write('    class           dictionary; \n')
f.write('    object          blockMeshDict;\n')
f.write('}\n')
f.write('\n')
f.write('// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * // \n')

f.write('\n')
f.write('convertToMeters 1;\n')
f.write('\n')
f.write('vertices (')

wedge=pi/180.*5.
x0=0.25

# fine mesh
nx=250
ny=20
xGrad=1
yGrad=1

r1=0.005

vertices=[]
#central point
vertices.append([0,0,0])#0
vertices.append([0,r1*cos(wedge/2.),r1*sin(-wedge/2.)])#1
vertices.append([x0,r1*cos(wedge/2.),r1*sin(-wedge/2.)])#2
vertices.append([x0,0,0])#3
vertices.append([0,r1*cos(wedge/2.),r1*sin(wedge/2.)])#4
vertices.append([x0,r1*cos(wedge/2.),r1*sin(wedge/2.)])#5

for v in vertices:
	f.write('\n\t('+str(v[0])+' '+str(v[1])+' '+str(v[2])+')')


f.write('\n);')
f.write('\n\n blocks (')
#inlet
f.write('\n\t hex (0 3 2 1 0 3 5 4) ('+str(nx)+' '+str(ny)+' 1) simpleGrading ('+str(xGrad)+' 1 1)')

f.write('\n);')

f.write('\n\nedges (')

f.write('\n\t arc 1 4 (0 '+str(r1)+' 0)')
f.write('\n\t arc 2 5 ('+str(x0)+' '+str(r1)+' 0)')

f.write('\n);')

# patches
f.write('\n\npatches\n(')
# inlet
f.write('\n\t patch nozzle (')
f.write('\n\t\t (0 4 1 0)')
f.write('\n\t )')
# walls
f.write('\n\t wall walls (')
f.write('\n\t\t (1 4 5 2)')
f.write('\n\t )')

# wedge front and back
f.write('\n\t wedge back (')
f.write('\n\t\t (0 1 2 3)')
f.write('\n\t )')
f.write('\n\t wedge front (')
f.write('\n\t\t (0 3 5 4)')
f.write('\n\t )')
# outlet
f.write('\n\t patch outlet (')
f.write('\n\t\t (3 2 5 3)')
f.write('\n\t )')
f.write('\n);')
# --

f.write('\n\n mergePatchPairs\n(\n);')

f.write('\n\n// ************************************************************************* // ')
f.close()
#os.system('xterm -hold -e \'source ~/.cshrc ;  blockMesh\'')











