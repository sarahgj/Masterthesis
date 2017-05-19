import latex_plots as lp # Must be on top!
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import specify as sp
import datetime
import matplotlib.dates as mdates
import statsmodels.api as sm

def main():
	def read_file(infile):
            with open(infile) as f:
                lines = f.readlines()
                # you may also want to remove whitespace characters like `\n` at the end of each line
                numbers = [float(line.rstrip('\n')) for line in lines]
            return numbers

	substance, period, cruise, name, N = sp.specify()

	input_parentdir = "/uio/hume/student-u17/sarahgj/Master/Data/VSLS_measurements/"
	entrained_mass = read_file(input_parentdir + "Entrained/" + "entrained_mass_%s.dat" % name)
	entrained_traj = read_file(input_parentdir + "Entrained/" + "entrained_traj_%s.dat" % name)
	released_mass = read_file(input_parentdir + "Released/" + "released_%s.dat" % name)


        x = range(len(entrained_mass))
	micro = 1e-6
        nano = 1e-9
	molm = 0.14194 # Methyliodide, Molare Masse [kg/mol]

        entrained_mass = [x/(nano*molm) for x in entrained_mass]
        released_mass = [x/(micro*molm) for x in released_mass]

        corr = np.corrcoef(entrained_mass,released_mass)
        print corr
        
        #scatter plot
        fig = lp.newfig(1)
        plt.scatter(entrained_mass,released_mass)
        
        #add correlation line
        axes = plt.gca()
        m, b = np.polyfit(entrained_mass,released_mass, 1)
        X_plot = np.linspace(axes.get_xlim()[0],axes.get_xlim()[1],100)
        plt.plot(X_plot, m*X_plot + b, '-')

        #title etc
        plt.title(cruise + ": " + substance + ", correlation %.2f" %corr[0,1])
        plt.xlabel("Entrained mass [nmol]")
        plt.ylabel("Released mass [$\mu$mol]")

	destination_folder = "/uio/hume/student-u17/sarahgj/Master/Figures/VSLS/Entrainment/"
	filename = destination_folder + "entrained__released_corr%s" % name
	plt.savefig('{}.pdf'.format(filename))
	plt.savefig('{}.pgf'.format(filename))

        plt.show()


if __name__ == "__main__":
    main()
