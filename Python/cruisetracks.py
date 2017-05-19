#############################################################
##CODE to plot cruicetracks with dates, using DSHIP data.  ##
##No running mean included		                   ##	
## REMEMBER!!!!!!!   	                                   ##
## >> module load python		                   ##
##Creation: Mars 2017 - Sarah Gjermo - University of Oslo  ##
#############################################################

import latex_plots as lp
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from math import *
from dship import read_M91, read_ASTRA
import numpy as np

def make_map():
       	m = Basemap(projection='lcc',resolution='l',width=2500000,height=3200000,lon_0=-78.70,lat_0=-11.,urcrnrlat=2.) 
       	m.shadedrelief()
       	m.drawcountries(linewidth=0.6, linestyle='solid', color='k', antialiased=1, ax=None, zorder=None)
       	m.drawrivers(linewidth=0.1, linestyle='solid', color='b', antialiased=1, ax=None, zorder=None)
       	m.drawgreatcircle(lon1=0, lat1=0, lon2=-100, lat2=0, del_s=100.0, linewidth=1, color='w')
       	m.drawparallels(np.arange(int(-50.),int(50.),10),labels=[1,0,0,0], linewidth=0.0, size = 8)
       	m.drawmeridians(np.arange(int(-100.),int(-50.),10),labels=[0,0,0,1], linewidth=0.0, size = 8)
	return m

def plot_cruisetrack(data, m, col):
	x,y = m(data[1],data[0])
	m.plot(x,y,linewidth=3, color=col)
	#for i in range(1,len(data[5]),780):
	#	x_spot,y_spot = m(data[1][i],data[0][i])
	#	date = "%s/%s"%(str(data[4][i]),str(data[5][i]))
	#	print(date)
	#	plt.text(x_spot,y_spot,date,weight='bold')
       	return

def main():
	astra  = read_ASTRA()	#[0]=latitude, [1]=longitude, [2]=SST, [3]=T
	print "Done reading one"
	m91 = data = read_M91() #[0]=latitude, [1]=longitude, [2]=SST, [3]=T
	print "Done reading two"

	fig  = lp.newfig(1)
	m = make_map()
	plot_cruisetrack(astra, m, 'r')
	plot_cruisetrack(m91, m, 'b')
  
    	destination_folder = "/uio/hume/student-u17/sarahgj/Master/Figures/DSHIP/"
       	filename = destination_folder + "/cruisetrack" 
	plt.savefig('{}.pgf'.format(filename))
	plt.savefig('{}.pdf'.format(filename))

if __name__ == "__main__":
    main()
