##############################################################################
## Plots the lifetime profile used in FLEXPART for Bromoform and            ##
## dibromomethane.                                                          ##
## Creation: Mars 2016 - Sarah Gjermo - University of Oslo                  ##
##############################################################################

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import numpy as np
import latex_plots as lp


# Raw input in seconds
dibromomethane = [3293000.0,3293000.0,3892000.0,4491000.0,5089000.0,5688000.0,6886000.0,8383000.0,10478000.0,11975000.0,14370000.0,17364000.0,20657000.0,23950000.0,26944000.0,29938000.0,28141000.0,23950000.0,20058000.0,13173000.0,8383000.0]
bromoform = [958003.2, 958003.2,1017878.4,1017878.4,1017878.4,1017878.4,1257379.2,1257379.2,1257379.2,1257379.2,1257379.2,1257379.2,1736380.8,1736380.8,1736380.8,1736380.8,1736380.8,1736380.8,1556755.2,1556755.2,1556755.2]

# Conversion to days #
brom_mean = []
dibrom_mean = []
for i in range(0,21):
    dibromomethane[i]= dibromomethane[i]/(24*60*60)
    bromoform[i]= bromoform[i]/(24*60*60)


print(np.mean(dibromomethane), np.mean(bromoform))

# Making a hight list
hight = range(0,21)

## PLOTTING ##
lp.newfig(0.8)
host = host_subplot(111, axes_class=AA.Axes)
plt.subplots_adjust(right=0.75)

par1 = host.twinx()

#host.set_title("Lifetime Profiles", size=20)
host.set_xlabel("Height")
host.set_ylabel("Bromoform [days]")
par1.set_ylabel("Dibromomethane [days]")

p1, = host.plot(hight, bromoform, "k")
p2, = par1.plot(hight, dibromomethane, "b")

host.axis["left"].label.set_color(p1.get_color())
par1.axis["right"].label.set_color(p2.get_color())

plt.draw()

destination_folder = "/uio/hume/student-u17/sarahgj/Master/Figures/VSLS/Lifetime_profiles/"
filename = destination_folder + "lifetime_profiles_latex"
plt.savefig('{}.pdf'.format(filename))
plt.savefig('{}.pgf'.format(filename))
plt.show()
