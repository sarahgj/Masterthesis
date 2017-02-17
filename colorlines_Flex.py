#!/usr/bin/env python
#
# (C) Copyright 2016 UIO.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0. 
# 
# Creation: October 2016 - Anne Fouilloux - University of Oslo
# Modified: Sarah

# REMEMBER!!!!!!!   
#

import os
import calendar
import shutil
import datetime
import time
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
from glob import glob
from optparse import OptionParser
from FlexParticle import FlexParticle
import pylab as pl
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.collections import LineCollection


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


	def make_map(title):
		fig = plt.figure(1,figsize=(15,12))
		m = Basemap(projection='lcc',resolution='l',width=10000000,height=8000000,lon_0=-78.75,lat_0=-11.,urcrnrlat=2.) 
		#m.shadedrelief()
		m.drawcountries(linewidth=1.2, linestyle='solid', color='k', antialiased=1, ax=None, zorder=None)
		m.drawcoastlines()
		#m.drawrivers(linewidth=0.2, linestyle='solid', color='b', antialiased=1, ax=None, zorder=None)
		#m.drawgreatcircle(lon1=0, lat1=0, lon2=-150, lat2=0, del_s=100.0, linewidth=2, color='w')
		m.drawparallels(np.arange(int(-50.),int(50.),15),labels=[1,0,0,0], linewidth=0.0, size = 18)
		m.drawmeridians(np.arange(int(-120.),int(0.),15),labels=[0,0,0,1], linewidth=0.0, size = 18)
		m.drawmapboundary(fill_color='white')
		#plt.title(title)
		return m, fig

	#=============================================================================================================#
	
	def plot_on_map(p, m, fig):
		#print maxheight
		#x_start,y_start = m(-80.1991,-9.9159) 
		maxheight= p.heights.max()
		print p.lons[1,1], p.lats[1,1]
		x,y = m(p.lons[:,:], p.lats[:,:])   # Transforms the data into the map's
		Ntime = len(x[:,1]) #i
		Ntraj = len(x[1,:]) #j
		if variable == "height":
			var = p.heights
		if variable == "mass":
			var = p.xmass
		#---------------------------------------------------------------------------------------------------------#		
	       	for j in range(0,Ntraj-1):
       			#for i in range(Ntime-1):
       			#if np.max(var[:,j]) >= 17000:
       				points = np.array([x[:,j], y[:,j]]).T.reshape(-1, 1, 2)
			       	segments = np.concatenate([points[:-1], points[1:]], axis=1)
		       		lc = LineCollection(segments, cmap=plt.get_cmap('jet'), norm=plt.Normalize(np.min(var),np.max(var)))
	       			lc.set_array(var[:,j])
       				lc.set_linewidth(1)						      			
				plt.gca().add_collection(lc)
				return lc			


	#=============================================================================================================#
	#=============================================================================================================#
	#=============================================================================================================#


	#var = raw_input("Please enter something: ")
	#print "you entered", var
	
	print """usage: %prog cruice (ASTRA or M91) variable (height or mass) every* trajectory (number or TTP)"""

	import sys
	cruise = sys.argv[1]
	variable = sys.argv[2]
	num_traj = sys.argv[3]

	if raw_input("Would you like more options (yes or enter)?"):
		calc_entrained = raw_input("Calculate entrained mass and trajectories (yes or enter)?")
	else:
		print "continuing"

	micro = 1e-6
	molm = 0.14194 # Methyliodide, Molare Masse [kg/mol]

	if cruise == "M91":
		N = 102
	       	input_parentdir = "/projects/NS1004K/Sarahgj/Flexpart/M91/Methyliodide/"
		m, fig = make_map(title="Methyliodide, M91")
		if num_traj == "TTP":
			name = "methyliodide17km_M91"
		else:
			name = "methyliodide_M91"
		released_mass = 41.776958*micro*molm 

	if cruise == "ASTRA":
		N = 85
		input_parentdir = "/projects/NS1004K/Sarahgj/Flexpart/ASTRA/Methyliodide_F10/"
		m,fig = make_map(title="Methyliodide, ASTRA")
		if num_traj == "TTP":
			name = "methyliodide17km_ASTRA"
		else:
			name = "methyliodide_ASTRA"
		released_mass = 15.3880322*micro*molm 

	print "map done"
	entrained_mass = [] 
	entrained_traj = []
	for i in range(1,N+1):
		print "Working on file nr. %i" %i
		p = read_input(input_parentdir + "outputs-%i/" % i)
		print i,"opened"
		lc = plot_on_map(p, m, fig)
		#mass,traj = calc_amounts_17km(p)
		#entrained_mass.append(mass)
		#entrained_traj.append(traj)
		#print "Amount of trajectories reaching 17 km is: ", entrained_traj[i-1]
		#print "Amount of mass reaching 17 km is: ", entrained_mass[i-1]

	if variable == "height":
		axcb = fig.colorbar(lc, ticks=[0,2000,4000,6000,8000,10000,12000,14000,16000,18000,20000])
		axcb.set_label('Height [m]', fontsize=18)
	if variable == "mass":
		axcb = fig.colorbar(lc)
		axcb.set_label('mass [?]', fontsize=18)
	axcb.ax.tick_params(labelsize=18)
	
	#percent_traj = sum(entrained_traj)*100/(10000.0*N)
	#percent_mass = (sum(entrained_mass)/released_mass)*100
	#print "The percentage of trajectories reaching 17 km for all releases is: ", percent_traj
	#print "The percentage of mass reaching 17 km for all releases is: ", percent_mass

	save = raw_input("Would you like to save the figure (enter or no)?")
	if save is not "no"
		destination_folder = "/projects/NS1004K/Sarahgj/Figures/Flexpart/"
		outputplot = destination_folder + name
		plt.savefig('%s.pdf'%(outputplot))
		plt.savefig('%s.png'%(outputplot))
		plt.savefig('%s.eps'%(outputplot))

	plt.show()


	
if __name__ == "__main__":
    main()
