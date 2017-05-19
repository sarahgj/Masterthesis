##############################################################################
## Plots the released, entrained and relative entraind mass for the         ##
## FLEXPART released species. Saved in ./Figures/Entrainment.               ##
## Creation: Februar 2016 - Sarah Gjermo - University of Oslo               ##
##############################################################################
# REMEMBER!!!!!!!   
# >> module use --append /projects/NS1000K/modulefiles
# >> module load python/anaconda
# >> module load python

import latex_plots as lp # Must be on top!
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import specify as sp
import datetime
import matplotlib.dates as mdates



def main():
	def read_file(infile):
            with open(infile) as f:
                lines = f.readlines()
                # you may also want to remove whitespace characters like `\n` at the end of each line
                numbers = [float(line.rstrip('\n')) for line in lines]
            return numbers

	substance, period, cruise, name, N = sp.specify()

	# read information to lists
	input_parentdir = "/uio/hume/student-u17/sarahgj/Master/Data/VSLS_measurements/"
	entrained_mass = read_file(input_parentdir + "Entrained/" + "entrained_mass_%s.dat" % name)
	entrained_traj = read_file(input_parentdir + "Entrained/" + "entrained_traj_%s.dat" % name)
	released_mass = read_file(input_parentdir + "Released/" + "released_%s.dat" % name)
	lat = read_file(input_parentdir + "Released/" + "lats_%s.dat" % name)
	
	#read date information to list
	with open(input_parentdir + "Released/" + "dates_%s.dat" % name, 'r') as myfile:
		dates_string = myfile.readlines()
		dates_string = [x.strip() for x in dates_string] 
	datetimes = []
	for x in dates_string:
		datetimes.append(datetime.datetime.strptime(x,'%Y%m%dT%H%M%S'))
	dates = mpl.dates.date2num(datetimes)

        x = range(len(entrained_mass))
        percentage = [entrained_mass[i]/released_mass[i]*100 for i in x]

	micro = 1e-6
        nano = 1e-9
	molm = 0.14194 # Methyliodide, Molare Masse [kg/mol]

        entrained_mass = [x/(nano*molm) for x in entrained_mass]
        released_mass = [x/(micro*molm) for x in released_mass]

	# make date plot
	fig, host, par1, par2 = lp.subplot(1)

        host.set_title(cruise + ": " + substance)
        host.set_xlabel("Cruise")
        host.set_ylabel("Released mass [$\mu$mol]")
        par1.set_ylabel("Entrained mass [nmol]")
        par2.set_ylabel("Relative entrained [%]")

        p1, = host.plot(dates,released_mass, "k")
        p2, = par1.plot(dates,entrained_mass, "r")
        p3, = par2.plot(dates,percentage, "b." )

	# define axis limits
	if substance == "Methyliodide":
		host.set_ylim(0,3)
		par1.set_ylim(0,3)
		par2.set_ylim(0,0.35)
	elif substance == "Bromoform":
		par2.set_ylim(0,2.25)
	elif substance == "Dibromomethane":
		host.set_ylim(0,1.8)
		par1.set_ylim(0,180)
		par2.set_ylim(7,24)

	# make dates on x-axis
	daymonthFmt = mdates.DateFormatter('%d/%m')
	host.xaxis.set_major_formatter(daymonthFmt)

	# legend
        host.legend()
        host.axis["left"].label.set_color(p1.get_color())
        par1.axis["right"].label.set_color(p2.get_color())
        par2.axis["right"].label.set_color(p3.get_color())
        plt.draw()

	# save date plot
	destination_folder = "/uio/hume/student-u17/sarahgj/Master/Figures/VSLS/Entrainment/"
	filename = destination_folder + "date_mass_entrainment_%s" % name
	plt.savefig('{}.pdf'.format(filename))
	plt.savefig('{}.pgf'.format(filename))
        plt.show()


	# make lat plot
	fig, host, par1, par2 = lp.subplot(1)

	# arrange lists according to lat
	lat_arr = [x for (x,y,z,p) in sorted(zip(lat,entrained_mass, released_mass, percentage), key=lambda pair: pair[0])]
	entrained_mass_arr = [y for (x,y,z,p) in sorted(zip(lat,entrained_mass, released_mass, percentage), key=lambda pair: pair[0])]
	released_mass_arr = [z for (x,y,z,p) in sorted(zip(lat,entrained_mass, released_mass, percentage), key=lambda pair: pair[0])]
	percentage_arr = [p for (x,y,z,p) in sorted(zip(lat,entrained_mass, released_mass, percentage), key=lambda pair: pair[0])]

        host.set_title(cruise + ": " + substance)
        host.set_xlabel("Latitude")
        host.set_ylabel("Released mass [$\mu$mol]")
        par1.set_ylabel("Entrained mass [nmol]")
        par2.set_ylabel("Relative entrained [%]")

        p1, = host.plot(lat_arr,released_mass_arr, "k")
        p2, = par1.plot(lat_arr,entrained_mass_arr, "r")
        p3, = par2.plot(lat_arr,percentage_arr, "b." )

	# define axis limits
	if substance == "Methyliodide":
		host.set_ylim(0,3)
		par1.set_ylim(0,3)
		par2.set_ylim(0,0.35)
	elif substance == "Bromoform":
		par2.set_ylim(0.5,2)
	elif substance == "Dibromomethane":
		host.set_ylim(0,1.8)
		par1.set_ylim(0,180)
		par2.set_ylim(7,24)

	# legend
        host.legend()
        host.axis["left"].label.set_color(p1.get_color())
        par1.axis["right"].label.set_color(p2.get_color())
        par2.axis["right"].label.set_color(p3.get_color())
        plt.draw()

	# save date plot
	destination_folder = "/uio/hume/student-u17/sarahgj/Master/Figures/VSLS/Entrainment/"
	filename = destination_folder + "lat_mass_entrainment_%s" % name
	plt.savefig('{}.pdf'.format(filename))
	plt.savefig('{}.pgf'.format(filename))
        plt.show()


if __name__ == "__main__":
    main()
