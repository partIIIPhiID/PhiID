#!/bin/bash
#SBATCH -p icelake-himem
#SBATCH -t 04:00:00
#SBATCH --array=1-16
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
matlab -nodesktop -nosplash -r "automate_csv_heatmap('/rds/user/ae431/hpc-work/PhiID_results/', '/rds/user/ae431/hpc-work/PhiID_results/exp_1/csv_for_heatmap/',65, 80, 'post2', ${SLURM_ARRAY_TASK_ID}); quit"

