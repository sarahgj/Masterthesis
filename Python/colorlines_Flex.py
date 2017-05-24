##########################################################################################################
# This program plots the particle trajectories from Flexpart on a map with a colored third variable.
# 
# REMEMBER!!!!!!!   
# >> module use --append /projects/NS1000K/modulefiles
# >> module load python/anaconda

import latex_plots as lp # Must be on top!
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
import fnmatch
import specify as sp


def main():

	#=============================================================================================================#

	def read_input(inputdir):
		##Reads the Flexpart output files, and chunkes all data into p, each file at a time.##
		p = FlexParticle(inputdir)
		return p	
	
	def calc_amounts_17km(p):
		## Calculates the number of trajectories that passes the 17 km TOA boundary (also if they drop back down again).##
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
		##Sets up a nice map for the figure, and adds a title.##
		#fig = plt.figure(1,figsize=(20,15))
		fig, ax  = lp.newfig(1)
		m = Basemap(projection='lcc',resolution='l',width=10000000,height=8000000,lon_0=-78.75,lat_0=-11.,urcrnrlat=2.) 	      
		m.drawparallels(np.arange(int(-50.),int(50.),15),labels=[1,0,0,0], linewidth=0.0)
		m.drawmeridians(np.arange(int(-120.),int(0.),15),labels=[0,0,0,1], linewidth=0.0)
		#m = Basemap(projection='lcc',resolution='l',width=30000000,height=15000000,lon_0=-78.75,lat_0=-11.,urcrnrlat=2.) 
		#The whole world:
		#m = Basemap(llcrnrlon=-180,llcrnrlat=-80,urcrnrlon=180,urcrnrlat=80,projection='mill')
                #m.drawparallels(np.arange(-80,81,20),labels=[1,1,0,0])
		#m.drawmeridians(np.arange(0,360,60),labels=[0,0,0,1])
		
		#m.shadedrelief()
		m.drawcountries(linewidth=1.2, linestyle='solid', color='k', antialiased=1, ax=None, zorder=None)
		m.drawcoastlines()
		#m.drawrivers(linewidth=0.2, linestyle='solid', color='b', antialiased=1, ax=None, zorder=None)
		#m.drawgreatcircle(lon1=0, lat1=0, lon2=-150, lat2=0, del_s=100.0, linewidth=1.5, color='r')
		m.drawmapboundary(fill_color='white')
		plt.title(title)
		return m, fig
	
	def plot_on_map(p, m, fig, variable, who, everyN):
		##Does the plotting, each file at a time.##
		x,y = m(p.lons[:,:], p.lats[:,:])   # Transforms the data into the map's coordinates
		Ntraj = len(x[1,:]) #j, number of trajectiories
		Ntime = len(x[:,1]) #number of timestamps
		if variable == "h":
			var = p.heights
		if variable == "m":
			var = p.xmass
		lc = False
		#---------------------------------------------------------------------------------------------------------#	
	
		if who  == "TTP":
			for j in range(0,Ntraj-1,int(everyN)):
				if np.max(var[:,j]) >= 17000:
					points = np.array([x[:,j], y[:,j]]).T.reshape(-1, 1, 2)
					segments = np.concatenate([points[:-1], points[1:]], axis=1)
					lc = LineCollection(segments, cmap=plt.get_cmap('jet'), norm=plt.Normalize(np.min(var),np.max(var)))
					lc.set_array(var[:,j])
					lc.set_linewidth(1)						      			
					plt.gca().add_collection(lc)

		elif who == "avTTP":
			n = 0
			lons = np.zeros(Ntime)
			lats = np.zeros(Ntime)
			variable = np.zeros(Ntime)
			for j in range(0,Ntraj-1):
				if np.max(var[:,j]) >= 17000:
					lons = lons + x[:,j]
					lats = lats + y[:,j]
					variable = variable + var[:,j]
					n = n + 1
			lons = lons/n
			lats = lats/n
			variable = variable/n
       	       		points = np.array([lons, lats]).T.reshape(-1, 1, 2)
       	       		segments = np.concatenate([points[:-1], points[1:]], axis=1)
       	       		lc = LineCollection(segments, cmap=plt.get_cmap('jet'), norm=plt.Normalize(np.min(variable),np.max(variable)))
	       		lc.set_array(variable)
			lc.set_linewidth(1)						      			
			plt.gca().add_collection(lc)

		else:
			for j in range(0,Ntraj-1,int(everyN)):
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
	

	#Import options in parameters
	substance, period, cruise, name, N_releases = sp.specify()
	print """variable:h(height)/m(mass) who:all/TTP/avTTP everyN:(number of trajectories) test:y/n"""
	import sys
	variable = sys.argv[3]
	who = sys.argv[4]
	everyN = sys.argv[5]
	test = sys.argv[6]

	if who == "TTP":
		name2 = "_17km"
	elif who == "avTTP":
		name2 = "_av17km"
	else:
		name2 = "_every%straj" % everyN
	if test == "y":
		name3 = "_test"
	else:
		name3 = ""
	name = name + '_' + variable + name2 + name3

	#Set name of input parent directory, title, and name of file
	input_parentdir = "/projects/NS1004K/sarahgj/Flexpart/%s/%s_%s/"%(cruise,substance,period)
	title = "%s, %s"%(substance, cruise)

	#Make the map
	m,fig = make_map(title) #Title not included????
	print "map done"

	colorbar = False

	if test == "y":
		#Read input and plot on map
		for i in range(1,N_releases+1,40):
			print "Working on file nr. %i" %i
			p = read_input(input_parentdir + "outputs-%i/" % i)
			print i,"opened"
			lc = plot_on_map(p, m, fig, variable, who, everyN)
			if lc != False and colorbar == False:
				#Make colorbar 
				if variable == "h":
					axcb = fig.colorbar(lc, ticks=[0,2000,4000,6000,8000,10000,12000,14000,16000,18000,20000])
					axcb.set_label('Height [m]')
				elif variable == "m":
				       	axcb = fig.colorbar(lc)
				       	axcb.set_label('mass [?]')
				axcb.ax.tick_params()
				colorbar = True
				print 'made colorbar'


	else:
		#Read input and plot on map
		for i in range(1,N_releases+1):
			print "Working on file nr. %i" %i
			p = read_input(input_parentdir + "outputs-%i/" % i)
			print i,"opened"
			lc = plot_on_map(p, m, fig, variable, who, everyN)
			if lc != False and colorbar == False:
				#Make colorbar 
				if variable == "h":
					axcb = fig.colorbar(lc, ticks=[0,2000,4000,6000,8000,10000,12000,14000,16000,18000,20000])
					axcb.set_label('Height [m]')
				elif variable == "m":
				       	axcb = fig.colorbar(lc)
				       	axcb.set_label('mass [?]')
				axcb.ax.tick_params()
				colorbar = True
				print 'made colorbar'

	plt.show(fig)

	#Saving the figure
	#save = raw_input("Would you like to save the figure (enter or no)?")
	#if save is not "no":
	destination_folder = "/projects/NS1004K/sarahgj/Figures/Flexpart/"
	#if test == 'y':
	#	destination_folder = destination_folder + 'Tests/'
	outputplot = destination_folder + name
	#plt.savefig('{}.eps'.format(outputplot))
	#plt.savefig('{}.pdf'.format(outputplot))
	plt.savefig('%s.png' % outputplot)
	plt.savefig('%s.pdf' % outputplot)

	print "Figures saved as %s" % outputplot



	
if __name__ == "__main__":
    main()
