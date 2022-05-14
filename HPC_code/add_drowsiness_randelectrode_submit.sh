#!/bin/bash
#SBATCH -p icelake-himem
#SBATCH -t 10:00:00
#SBATCH --array=1-100
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
matlab -nodesktop -nosplash -r "add_drowsiness_randelectrode(${SLURM_ARRAY_TASK_ID}, 100, '', '/rds/user/ae431/hpc-work/PhiID_results/', '/rds/project/tb419/rds-tb419-bekinschtein/Yanzhi/EXP_1_Masking/Analysis_Micromeasures/iaf/', '/rds/user/ae431/hpc-work/PhiID_results/exp_1/perf_drow_data/','performance_data_cross'); quit"

