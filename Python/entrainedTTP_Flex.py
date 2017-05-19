# 
# Creation: Februar 2016 - Sarah Gjermo - University of Oslo 
#
# REMEMBER!!!!!!!   
# >> module use --append /projects/NS1000K/modulefiles
# >> module load python/anaconda

#import os
#import calendar
#import shutil
#import datetime
#import time
import numpy as np
#from glob import glob
#from optparse import OptionParser
from FlexParticle import FlexParticle
#import pylab as pl
import matplotlib.pyplot as plt
#from mpl_toolkits.axes_grid1 import host_subplot
#import mpl_toolkits.axisartist as AA
import specify as sp

def main():

	#=============================================================================================================#

	def read_input(inputdir):
		p = FlexParticle(inputdir)
		return p	
	
	def calc_amounts_17km(p):
		## Calculates the number of trajectories that passes the 17 km TOA boundary (also if they drop back down again).
		Ntime = len(p.heights[:,1]) #i
		Ntraj = len(p.heights[1,:]) #j
		entrained_mass = 0
		entrained_traj = 0
		for i in range(Ntime-1):
			for j in range(Ntraj-1):
				if np.asarray(p.heights[i,j]) > 17000:
					entrained_mass += p.xmass[i,j]
					entrained_traj += 1
					break
		return entrained_mass, entrained_traj

	def write_outfile(what, outfile):
            f = open(outfile, 'w')
            for item in what:
                f.write('%.8e \n' %item)
            print "wrote file to: ", outfile

	#=============================================================================================================#

	substance, period, cruise, name, N_releases = sp.specify()
	print substance

	#Set name of input parent directory, title, and name of file
	input_parentdir = "/projects/NS1004K/sarahgj/Flexpart/%s/%s_%s/"%(cruise,substance,period)

	entrained_mass = [] 
	entrained_traj = []
#        N = 2
	print "Starting job for %s" % name
	print "number of releases:", N_releases
	for i in range(1,N_releases+1):
		print "Working on file nr. %i" %i
		if substance == "Dibromomethane":
			p = read_input(input_parentdir + "run-%i/outputs-%i/" % (i,i))
		else:
			p = read_input(input_parentdir + "outputs-%i/" % i)	
		print i,"opened"
		mass,traj = calc_amounts_17km(p)
		entrained_mass.append(mass)
		entrained_traj.append(traj)
		print "Amount of trajectories reaching 17 km is: ", entrained_traj[i-1]
		print "Amount of mass reaching 17 km is: ", entrained_mass[i-1]

        write_outfile(entrained_mass, "/projects/NS1004K/sarahgj/Data/VSLS_measurements/Entrained_Flex/entrained_mass_%s.dat" % name)
        write_outfile(entrained_traj, "/projects/NS1004K/sarahgj/Data/VSLS_measurements/Entrained_Flex/entrained_traj_%s.dat" % name)
	
	print "Finished job for %s" % name

if __name__ == "__main__":
    main()
