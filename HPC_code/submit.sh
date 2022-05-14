#!/bin/bash
#SBATCH -p icelake
#SBATCH -t 00:01:00
#SBATCH --array=1-20
#SBATCH -J PhiID
#SBATCH -o logs/PhiID_%A_%a.out
#SBATCH -e logs/PhiID_%A_%a.err

###############################
#  DO NOT CHANGE THESE LINES
module purge
module load rhel7/default-peta4
###############################

module load matlab
cd /home/ae431/elph/PhiID
matlab -nodesktop -nosplash -r "supermain(${1}, ${2}, ${3}); quit"

