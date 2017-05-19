################################################################################ Plots the released, entrained and relative entraind mass for the         #### FLEXPART released species. Saved in ./Figures/Entrainment.               #### Creation: Februar 2016 - Sarah Gjermo - University of Oslo               ################################################################################# REMEMBER!!!!!!!   # >> module use --append /projects/NS1000K/modulefiles# >> module load python/anacondaimport latex_plots as lp # Must be on top!import matplotlib as mplimport numpy as npimport matplotlib.pyplot as pltfrom mpl_toolkits.axes_grid1 import host_subplotimport mpl_toolkits.axisartist as AAimport specify as spimport datetimeimport matplotlib.dates as mdatesfrom matplotlib.dates import YearLocator, MonthLocator, DateFormatterimport pylabdef main():	def read_file(infile):            with open(infile) as f:                lines = f.readlines()                # you may also want to remove whitespace characters like `\n` at the end of each line                numbers = [float(line.rstrip('\n')) for line in lines]            return numbers			fig, ax  = lp.newfig(0.49)	substance, period, cruise, name, N = sp.specify()	input_parentdir = "/uio/hume/student-u17/sarahgj/Master/Data/VSLS_measurements/"	entrained_mass = read_file(input_parentdir + "Entrained/" + "entrained_mass_%s.dat" % name)	entrained_traj = read_file(input_parentdir + "Entrained/" + "entrained_traj_%s.dat" % name)	released_mass = read_file(input_parentdir + "Released/" + "released_%s.dat" % name)	with open(input_parentdir + "Released/" + "dates_%s.dat" % name, 'r') as myfile:		dates_string = myfile.readlines()		dates_string = [x.strip() for x in dates_string] 	datetimes = []	for x in dates_string:		datetimes.append(datetime.datetime.strptime(x,'%Y%m%dT%H%M%S'))	print datetimes[1]	dates = mpl.dates.date2num(datetimes)	print dates[1]        x = range(len(entrained_mass))        percentage = [entrained_mass[i]/released_mass[i]*100 for i in x]	micro = 1e-6        nano = 1e-9	molm = 0.14194 # Methyliodide, Molare Masse [kg/mol]        entrained_mass = [x/(nano*molm) for x in entrained_mass]        released_mass = [x/(micro*molm) for x in released_mass]	fig, ax  = lp.newfig(0.49)        plt.plot_date(dates,released_mass,"k",label="Released mass [$\mu$mol]", tz=None, xdate=True)        plt.plot_date(dates,entrained_mass,"r",label="Entrained mass [nmol]", tz=None, xdate=True)        plt.plot_date(dates,percentage,"b.",label="Relative mass [%]", tz=None, xdate=True)        fig.autofmt_xdate()	daymonthFmt = mdates.DateFormatter('%d/%m')	ax.xaxis.set_major_formatter(daymonthFmt)	ax.grid(True)	#pylab.legend(loc=9, bbox_to_anchor=(0.5, -0.1), ncol=3,frameon=False)	destination_folder = "/uio/hume/student-u17/sarahgj/Master/Figures/VSLS/Entrainment/"	filename = destination_folder + "mass_entrainment_%s" % name	legendfigname = destination_folder  + "mass_entrainment_legend"	plt.savefig('{}.pdf'.format(filename))	plt.savefig('{}.pgf'.format(filename))#	legendfig = pylab.figure()#	pylab.legend(loc=9, bbox_to_anchor=(0.5, 1), ncol=3)#	plt.figlegend([a,b,c],["Released mass [$\mu$mol]","Entraines mass [nmol]","Relative entrained [%]"], 'center')#	legendfig.savefig('{}.pdf'.format(legendfigname))#	legendfig.savefig('{}.pgf'.format(legendfigname))if __name__ == "__main__":    main()