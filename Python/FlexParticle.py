#
# (C) Copyright 2016 UIO.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0. 
# 
# 
# Creation: October 2016 - Anne Fouilloux - University of Oslo
#
#
# FlexParticle
# Usage:
#        p = FlexParticle("outputs")
# where outputs is the output directory for Flexpart simulation
#        p is then an object with:
#          p.lons longitudes for each date and particle
#          p.lats latitudes  for each particle
#          p.heights  heights in m for each particle
#          p.topo   topography heigth in m
#          p.pvi    potential vorticity
#          p.qvi    humidity
#          p.rhoi   air density
#          p.hmixi  'PBL' heigth in m
#          p.tri    tropopause heigth in m
#          p.tti    temperature
#          p.xmass  particle mass (for nspec species)
#
import os
import struct
import numpy as np
import time

class FlexParticle:
   'class to handle flexpart particle output files'
   def __init__(self, dirname):
      self.dirname=dirname
      self.nspec=1
       # go through all the files and read
      self.listdates=[]
      fin = open(self.dirname+'/dates') 
      for line in fin.xreadlines():
         self.listdates.append(line.strip())
      fin.close()
      
      self.datetime = []
      self.outheader = []
      self.numpart= -1
      ndates = len(self.listdates)
      idate=0
      for flexdate in self.listdates:
# get number of particles (once only as we assume it does not change)
        if self.numpart == -1:
           self.getnumpart(flexdate)
           # define lats, lons and heights as arrays
           # lats latitudes in degrees
           self.lats = np.zeros((ndates,self.numpart), dtype=np.float)
           # lons longitudes in degrees 
           self.lons = np.zeros((ndates,self.numpart), dtype=np.float)
           # particle heights in m
           self.heights = np.zeros((ndates,self.numpart), dtype=np.float)
           # release identifier (ID-number) when you hav emore than 1 release
           self.releaseIDs = np.zeros((ndates,self.numpart))
           # relase times of each particle 
           self.releaseTimes = np.zeros((ndates,self.numpart))
           # particle mass (for nspec species)
           self.xmass = np.zeros((ndates, self.numpart,self.nspec),dtype=np.float)
           # topography height in m
           self.topo = np.zeros((ndates, self.numpart), dtype=np.float)
           # potential vorticity
           self.pvi = np.zeros((ndates, self.numpart), dtype=np.float)
           # humidity
           self.qvi = np.zeros((ndates, self.numpart), dtype=np.float)
           # air density
           self.rhoi = np.zeros((ndates, self.numpart), dtype=np.float)
           # 'PBL' heigth in m
           self.hmixi = np.zeros((ndates, self.numpart), dtype=np.float)
           # tropopause heigth in m
           self.tri = np.zeros((ndates, self.numpart), dtype=np.float)
           # temperature
           self.tti = np.zeros((ndates, self.numpart), dtype=np.float)

           if self.numpart < 0:
                # no data so skip this date
		continue

# read particle file
        self.readpart(flexdate, idate)
        struct_time = time.strptime(flexdate, "%Y%m%d%H%M%S")
        self.datetime.append(struct_time)
        idate = idate + 1

   def getnumpart(self, flexdate):
      fname = self.dirname + 'partposit_' + flexdate
           
# get file size info
      nbytes = os.path.getsize(fname)
      # assuming the file has the exact format written in partoutput.f90 of Flexpart v. 9.02,
      # the size of the file is exactly 4 * [3 + (numpart+1)*(14+nspec)] bytes.
      self.numpart = int(round((nbytes/4+3)/(14+self.nspec)-1));

   def readpart(self, flexdate, idate):
      fname = self.dirname + 'partposit_' + flexdate
           
      fin = open(fname,  'rb')
      # read time record
      tmp = fin.read(4)
      tmp = fin.read(4)
      self.outheader.append(struct.unpack('<l',tmp)[0])
      # jump header
      fin.seek(24)
      # FLEXPART writes the output as:
      #      write(unitpartout) npoint(i),xlon,ylat,ztra1(i),
      # +    itramem(i),topo,pvi,qvi,rhoi,hmixi,tri,tti,
      # +    (xmass1(i,j),j=1,nspec)
      # as 4byte numbers, with an empty 4byte value before and afterwards
      # -> thus, the number of 4byte values read for each trajectory is 14+nspec

      nvals = 14 + self.nspec 
      fmt = '<llffflffffffff'
      for i in range(0,self.nspec):
         fmt = fmt + 'f' 
      for i in range(0,self.numpart):
         tmp = struct.unpack(fmt,fin.read(nvals*4))
         self.releaseIDs[idate, i] = tmp[1] 
         self.lons[idate, i] = tmp[2]
         self.lats[idate, i] = tmp[3]
         self.heights[idate, i] = tmp[4]
# release time for each particle
         self.releaseTimes[idate, i] = tmp[5]
         self.topo[idate, i] = tmp[6]
         self.pvi[idate, i] = tmp[7]
         self.qvi[idate, i] = tmp[8]
         self.rhoi[idate, i] = tmp[9]
         self.hmixi[idate, i] = tmp[10]
         self.tri[idate, i] = tmp[11]
         self.tti[idate, i] = tmp[12]
         self.xmass[idate, i,:] = tmp[13:13+self.nspec]

      fin.close()

