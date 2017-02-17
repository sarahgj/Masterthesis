#!/bin/bash
# Job name:
#SBATCH --job-name=running_flexpart#
# Project (to be changed if you have nortur allocations):
#SBATCH --account=nn1000k
#
# Wall clock limit (to be adjusted depending on your needs)
#SBATCH --time=60:00:0
#
# Max memory usage per core (MB):
#SBATCH --mem-per-cpu=30G
#
#
## Set up Abel job environment

source /cluster/bin/jobsetup


### Set up your environment for FLEXPART on Abel

module load flexpart/9.2.2

### Run FLEXPART (see tutorials/examples) in a temporary directory

# copy pathnames in your working directory

#for ((i=1;i<=2;i++))
for i in {1..24}; do
#for i in $(seq 3 1 N); do
  cp pathnames/pathnames-$i /work/users/sarahgj/pathnames
  #rm /work/users/sarahgj/outputs-$i/*
  cd /work/users/sarahgj
  FLEXPART
  cd /usit/abel/u1/sarahgj/Flexpart/Runs/M91/Bromoform_F92
done

# Please note that your output results are in a temporary directory!
# copy them back to your local workstation using rsync

# Run:
#  sbatch jobfile.sh 

# Monitor:
#  squeue --job JOBID
#  scontrol show job JOBID
#  squeue -u sarahgj

# Cancel:
#  scancel JOBID