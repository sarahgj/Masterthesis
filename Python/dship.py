#############################################################
##CODE TO READ DSHIPdata.py 	                           ##
##No running mean included		                   ##	
## REMEMBER!!!!!!!   	                                   ##
## >> module load python		                   ##
##Creation: Mars 2017 - Sarah Gjermo - University of Oslo  ##
#############################################################

import numpy as np
from math import *


def read_M91(input_parentdir="/uio/hume/student-u17/sarahgj/Master/Data/DSHIP/"):
       	## OPEN INFILE ##
       	filename = input_parentdir + "DSHIP_M91.dat"
       	infile = open(filename, 'r')

       	## INITIALIZING DATA LISTS FOR READING ##
       	year = []
       	month = []
       	day = []
       	hour = []
       	minute = []
       	#seconds is always 0
       	course = [] # [deg]
       	latitude = [] # latitude S
       	longitude = [] # longitude W
       	SST = [] # [deg celcius], sea surface temperature
       	T = [] # [deg celcius], air temperature
       	p = [] # [hPa], barometric pressure
       	p_norm = [] # [hPa], barometric pressure normalized
       	humidity = [] # [%]
       	winddir  = [] # [deg]
       	windspeed = [] # [m/s]

       	## READ FILE ##
       	for line in infile:
       		if line.startswith('2'):
       			part = line.split("\t")
       			if part[6] != "            " and part[26] != '      ':
       				#year.append(int(part[0]))
       				month.append(int(part[1]))
       				day.append(int(part[2]))
       				#hour.append(int(part[3]))
       				#minute.append(int(part[4]))
       				#course.append(float(part[9]))
       				latitude.append(float(part[6]))
       				longitude.append(float(part[7]))
       				#print part[6], part[7], part[26], part[13]			
       				SST.append(float(part[26]))
       				SST = [np.nan if x >= 	50 else x for x in SST]
       				T.append(float(part[13]))
       				T = [np.nan if x >= 50 else x for x in T]
       				#p.append(float(part[16]))
       				#p_norm.append(float(part[17]))
       				#humidity.append(float(part[19]))
       				#winddir.append(float(part[23]))
       				#winddir = [np.nan if x >= 360 else x for x in winddir]    
       				#windspeed.append(float(part[24]))
       				#windspeed = [np.nan if x >= 50 else x for x in windspeed]
       		else:
       			pass
       	infile.close()  
       	return latitude, longitude, SST, T, month, day


def read_ASTRA(input_parentdir="/uio/hume/student-u17/sarahgj/Master/Data/DSHIP/"):
       	## OPEN INFILE ##
       	filename = input_parentdir + "DSHIP_ASTRA.dat"
       	infile = open(filename, 'r')

       	## INITIALIZING DATA LISTS FOR READING ##
       	year = []
       	month = []
       	day = []
      	hour = []
       	minute = []
       	#seconds is always 0
       	course = [] # [deg]
       	latitude = [] # latitude S
       	longitude = [] # longitude W
       	SST = [] # [deg celcius], sea surface temperature
       	T = [] # [deg celcius], air temperature
       	p = [] # [hPa], barometric pressure
       	p_norm = [] # [hPa], barometric pressure normalized
       	humidity = [] # [%]
       	winddir  = [] # [deg]
       	windspeed = [] # [m/s]

       	## READ FILE ##
       	for line in infile:
       		if line.startswith('2'):
       			part = line.split("\t")
       			#year.append(int(part[0]))
       			month.append(int(part[1]))
      			day.append(int(part[2]))
       			#hour.append(int(part[3]))
       			#minute.append(int(part[4]))
       			#course.append(float(part[9]))

       			word = part[10].split()
       			if word[2] == 'S':
       				latitude.append(-float(word[0])-float(word[1])/60)
       			else:
       				latitude.append(float(word[0])+float(word[1])/60)

       			word = part[11].split()
       			if word[2] == 'W':
	       			longitude.append(-float(word[0])-float(word[1])/60)
	       		else:
		       		longitude.append(float(word[0])+float(word[1])/60)

	       		SST.append(float(part[14]))
	       		SST = [np.nan if x >= 50 else x for x in SST]
	       		T.append(float(part[15]))
	       		T = [np.nan if x >= 50 else x for x in T]
	       		#p.append(float(part[16]))
	       		#p_norm.append(float(part[17]))
	       		#humidity.append(float(part[19]))
	       		#winddir.append(float(part[23]))
	       		#winddir = [np.nan if x >= 360 else x for x in winddir]    
	       		#windspeed.append(float(part[24]))
	       		#windspeed = [np.nan if x >= 50 else x for x in windspeed]
	       	else:
	       		pass

        infile.close()  
       	return latitude, longitude, SST, T, month, day
