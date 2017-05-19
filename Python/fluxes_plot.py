##############################################################################
## Plots the released, entrained and relative entraind mass for the         ##
## FLEXPART released species. Saved in ./Figures/Entrainment.               ##
## Creation: Februar 2016 - Sarah Gjermo - University of Oslo               ##
##############################################################################
# REMEMBER!!!!!!!   
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

	# reading information in to lists
	input_parentdir = "/uio/hume/student-u17/sarahgj/Master/Data/VSLS_measurements/Fluxes/"
	flux = read_file(input_parentdir + "fluxes_%s.dat" % name)
	lat = read_file(input_parentdir + "all_lats_%s.dat" % name)

	# arranging lists according to lat
	lat_arr = [x for (x,y) in sorted(zip(lat,flux), key=lambda pair: pair[0])]
	flux_arr = [y for (x,y) in sorted(zip(lat,flux), key=lambda pair: pair[0])]

	# reading dates to list
	with open(input_parentdir + "all_dates_%s.dat" % name, 'r') as myfile:
		dates_string = myfile.readlines()
		dates_string = [x.strip() for x in dates_string] 
	datetimes = []
	for x in dates_string:
		datetimes.append(datetime.datetime.strptime(x,'%Y%m%dT%H%M%S'))
	dates = mpl.dates.date2num(datetimes)

	# make date figure
        fig, host = lp.newfig(1)
        host.plot(dates,flux)
	plt.axhspan(min(flux), 0, facecolor='r', alpha=0.3)
       	host.set_ylim(min(flux),max(flux)*(1+0.1))

        host.set_title(cruise + ": " + substance)
        host.set_xlabel("Cruise")
        host.set_ylabel("Flux [pmol/(m**{2*}hr)]")

	daymonthFmt = mdates.DateFormatter('%d/%m')
	host.xaxis.set_major_formatter(daymonthFmt)

	# save date figure
	destination_folder = "/uio/hume/student-u17/sarahgj/Master/Figures/VSLS/Fluxes/"
	filename = destination_folder + "date_fluxes_%s" % name
	plt.savefig('{}.pdf'.format(filename))
	plt.savefig('{}.pgf'.format(filename))

	# make lat figure
        fig, host = lp.newfig(1)
        host.plot(lat_arr,flux_arr,'b')
	plt.axhspan(min(flux_arr), 0, facecolor='r', alpha=0.3)
       	host.set_ylim(min(flux_arr),max(flux_arr)*(1+0.1))

        host.set_title(cruise + ": " + substance)
        host.set_xlabel("Latitude")
        host.set_ylabel("Flux [pmol/(m$^{2*}$hr)]")

	# save lat figure
	destination_folder = "/uio/hume/student-u17/sarahgj/Master/Figures/VSLS/Fluxes/"
	filename = destination_folder + "lat_fluxes_%s" % name
	plt.savefig('{}.pdf'.format(filename))
	plt.savefig('{}.pgf'.format(filename))

	plt.show()
if __name__ == "__main__":
    main()
