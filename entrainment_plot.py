# 
# Creation: Februar 2016 - Sarah Gjermo - University of Oslo 
#

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
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA


def main():


	def read_file(infile):
            with open(infile) as f:
                lines = f.readlines()
                # you may also want to remove whitespace characters like `\n` at the end of each line
                numbers = [float(line.rstrip('\n')) for line in lines]
            return numbers

        print """usage: %prog cruice (ASTRA or M91)"""

	import sys
	cruice = sys.argv[1]
        substance = "Methyliodide"

        if cruice == "ASTRA":
            entrained_mass =  read_file("/projects/NS1004K/Sarahgj/Data/VSLS_measurements/Entrained_Flex/entrained_methyliodide_ASTRA_mass.dat")
            released_mass = read_file("/projects/NS1004K/Sarahgj/Data/VSLS_measurements/Released_Flex/released_methyliodide_ASTRA.dat")
        elif cruice == "M91":
            entrained_mass =  read_file("/projects/NS1004K/Sarahgj/Data/VSLS_measurements/Entrained_Flex/entrained_methyliodide_M91_mass.dat")
            released_mass = read_file("/projects/NS1004K/Sarahgj/Data/VSLS_measurements/Released_Flex/released_methyliodide_M91.dat")

        x = range(len(entrained_mass))
        percentage = [entrained_mass[i]/released_mass[i]*100 for i in x]

	micro = 1e-6
        nano = 1e-9
	molm = 0.14194 # Methyliodide, Molare Masse [kg/mol]

        entrained_mass = [x/(nano*molm) for x in entrained_mass]
        released_mass = [x/(micro*molm) for x in released_mass]

        plt.figure(figsize=(15, 10)) 
        host = host_subplot(111, axes_class=AA.Axes)
        plt.subplots_adjust(right=0.75)

        par1 = host.twinx()
        par2 = host.twinx()

        offset = 60
        new_fixed_axis = par2.get_grid_helper().new_fixed_axis
        par2.axis["right"] = new_fixed_axis(loc="right",axes=par2,offset=(offset, 0))

        par2.axis["right"].toggle(all=True)

        host.set_xlim(0, len(entrained_mass))
        #host.set_ylim(0, 2)

        host.set_title(cruice + ": " + substance)
        host.set_xlabel("Cruice")
        host.set_ylabel("released mass [$\mu$mol]")
        par1.set_ylabel("entraines mass [nmol]")
        par2.set_ylabel("relative entrained [%]")

        p1, = host.plot(released_mass, "k")
        p2, = par1.plot(entrained_mass, "r")
        p3, = par2.plot(percentage, "b." )

        #par1.set_ylim(0, 4)
        #par2.set_ylim(1, 65)

        host.legend()

        host.axis["left"].label.set_color(p1.get_color())
        par1.axis["right"].label.set_color(p2.get_color())
        par2.axis["right"].label.set_color(p3.get_color())

        plt.draw()

	save = raw_input("Would you like to save the figure (enter or no)?")
        if save is not "no":
            destination_folder = "/projects/NS1004K/Sarahgj/Figures/Entrainment/"
            plt.savefig('%s.pdf'%(destination_folder + "entrainment_" + cruice + "_" + substance))
            plt.savefig('%s.png'%(destination_folder + "entrainment_" + cruice + "_" + substance))
            plt.savefig('%s.eps'%(destination_folder + "entrainment_" + cruice + "_" + substance))

        plt.show()


if __name__ == "__main__":
    main()
