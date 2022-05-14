#!/bin/bash
#SBATCH -p icelake-himem
#SBATCH -t 02:00:00
#SBATCH --array=1-30
#SBATCH -J PhiID
#SBATCH -o logs/PhiID_%A_%a.out
#SBATCH -e logs/PhiID_%A_%a.err
#SBATCH --cpus-per-task 1

###############################
#  DO NOT CHANGE THESE LINES
module purge
module load rhel7/default-peta4
###############################

module load matlab
cd /home/ae431/elph/PhiID
matlab -nodesktop -nosplash -r "main_crosspart(50, (50 + ${SLURM_ARRAY_TASK_ID}),'/rds/project/tb419/rds-tb419-bekinschtein/Yanzhi/EXP_1_Masking/', [1:60]); quit"

