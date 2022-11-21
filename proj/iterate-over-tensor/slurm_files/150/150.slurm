#!/bin/bash
#SBATCH --job-name=150iterate-over-tensor
#SBATCH --output=/home/wmorgan1/cmarron_user/thesis/proj/iterate-over-tensor/150/150.out
#SBATCH --error=/home/wmorgan1/cmarron_user/thesis/proj/iterate-over-tensor/150/150.err
#SBATCH --partition=batch
#SBATCH --qos=medium
#SBATCH --constraint=hpcf2013
#SBATCH --exclusive
#SBATCH --cpus-per-task=16
#SBATCH --nodes=1

export KMP_AFFINITY="verbose,compact"
export OMP_NUM_THREADS=16
srun /home/wmorgan1/cmarron_user/thesis/proj/iterate-over-tensor/pls -s .00000000000001 -n -c 1 -f /home/wmorgan1/cmarron_user/thesis/testData/150x3.txt -v &&

srun /home/wmorgan1/cmarron_user/thesis/proj/iterate-over-tensor/pls -s .00000000000001 -n -c 1 -f /home/wmorgan1/cmarron_user/thesis/testData/150x3.txt -v &&

srun /home/wmorgan1/cmarron_user/thesis/proj/iterate-over-tensor/pls -s .00000000000001 -n -c 1 -f /home/wmorgan1/cmarron_user/thesis/testData/150x3.txt -v &&

srun /home/wmorgan1/cmarron_user/thesis/proj/iterate-over-tensor/pls -s .00000000000001 -n -c 1 -f /home/wmorgan1/cmarron_user/thesis/testData/150x3.txt -v &&

srun /home/wmorgan1/cmarron_user/thesis/proj/iterate-over-tensor/pls -s .00000000000001 -n -c 1 -f /home/wmorgan1/cmarron_user/thesis/testData/150x3.txt -v