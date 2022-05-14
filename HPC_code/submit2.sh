#!/bin/bash
#SBATCH -p icelake-himem
#SBATCH -t 01:00:00
#SBATCH --array=1
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
matlab -nodesktop -nosplash -r "supermain([20, 21], 'AuMa_9_filtd_avgd_epochd_importID_epdeleted_ICA_pruned_interp_avgd.set', '/rds/project/tb419/rds-tb419-bekinschtein/Yanzhi/EXP_1_Masking/'); quit"

