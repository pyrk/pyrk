# From http://sankhamukherjee.blogspot.com/

######################################
# This program is used for calculating
# the bravis lattice points of a unit
# cell, and displaying the results in
# 3D. 
#
# Note that, since the mathematics of
# the bravis lattices are so uniform,
# it is relatively easy to calculate
# the positions of the positions of 
# all atoms, given a particular basis
######################################


##### Functions for doing the physics ##########

#-----------------------------------------------
# This function iterates over all lattice points
# and produces a list of 3D lattice points
#
# Input: 
#    N - the number of points in each dimension
# Output:
#    a [3 by (N+1)^3] matrix containing all
# the lattice points. Thus, for N = 1, returned
# points are,
# [[0,0,0], [0,0,1], [0,1,0], [0,1,1], [1,0,0], 
#  [1,0,1], [1,1,0], [1,1,1]]
#-----------------------------------------------
def lattice_points(N):
 lattice = []
 for i in range(N+1):
  for j in range(N+1):
   for k in range(N+1):
    lattice.append([i, j, k])
    lattice.append([i,j,k])
 return lattice
  
#----------------------------------------------
# This function returns the unit vectors in the 
# three different directions, for each of the 
# basis atoms. This function is generally so 
# simple that in most situatons, it may be 
# defined by hand. Maybe a class is in order?
#
# Shown below is the unit vectors for a BCC 
# lattice, with lattice size 'distance'.
# Notice that BCC has 2 atoms in its unit cell.
# Thus you only provide only 2 atoms. 
#----------------------------------------------
def unit_vectors_BCC(distance):
 a = distance; 
 point1 = [a, a, a]
 point2 = [a/2, a/2, a/2]
 return [point1, point2]

#----------------------------------------------
# This function returns a list of coordinates
# for each basis, given the basis, and the 
# lattice points. 
#----------------------------------------------
def atom_locations(basis, lattice):
 
 # Atom definitions
 atom1 = []
 atom2 = []
 
 # Basis vectors
 a1, a2, a3 = basis[0]
 b1, b2, b3 = basis[1]
 
 print a1, a2, a3
 print b1, b2, b3
 
 for n1, n2, n3 in lattice:
  atom1.append( [n1*a1, n2*a2, n3*a3] )
  atom2.append( [n1*a1 + b1, n2*a2 + b2, n3*a3 + b3] )
  
 return [atom1, atom2]
 
 
