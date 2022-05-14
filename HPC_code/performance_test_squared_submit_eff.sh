#!/bin/bash
#SBATCH -p icelake-himem
#SBATCH -t 10:00:00
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
matlab -nodesktop -nosplash -r "mass_performance_test_squared_eff(${SLURM_ARRAY_TASK_ID}, 9, 20, [68, 69, 70, 71, 72, 73, 74, 75, 76], 'AuMa_26_filtd_avgd_epochd_importID_epdeleted_ICA_pruned_interp_avgd.set', '/rds/project/tb419/rds-tb419-bekinschtein/Yanzhi/EXP_1_Masking/', '/rds/project/tb419/rds-tb419-bekinschtein/Yanzhi/EXP_1_Masking/', 'Original_epochs_pilot_26'); quit"

