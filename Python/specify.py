print """usage: %prog cruise (ASTRA or M91) (M, B or D)"""

def specify():
	#Import options in parameters
	import sys
	cruice = sys.argv[1]
	substance = sys.argv[2]

	if substance == "M":
		substance = "Methyliodide"
		period = "F10"
	if substance == "B":
		substance = "Bromoform"
		period = "F92"
	if substance == "D":
		substance = "Dibromomethane"
		if cruice == "ASTRA":
			period = "F437"
		else:
			period = "F548"

	name = "%s_%s_%s"%(substance,cruice,period)

	#Specify number of files to read
	if cruice == "M91" and  substance == "Methyliodide":
		N_releases = 102

	if cruice == "ASTRA" and substance == "Methyliodide":
		N_releases = 85

	if cruice == "M91" and substance == "Bromoform":
		N_releases = 24

	if cruice == "ASTRA" and substance == "Bromoform":
		N_releases = 81

	if cruice == "M91" and substance == "Dibromomethane":
		N_releases = 42

	if cruice == "ASTRA" and substance == "Dibromomethane":
		N_releases = 87
	
	return substance, period, cruice, name, N_releases
