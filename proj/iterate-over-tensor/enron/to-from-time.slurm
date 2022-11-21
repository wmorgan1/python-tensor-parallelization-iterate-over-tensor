#!/bin/bash
#SBATCH --job-name=altEnron
#SBATCH --output=/home/wmorgan1/cmarron_user/thesis/proj/iterate-over-tensor/enron/to-from-time.out
#SBATCH --error=/home/wmorgan1/cmarron_user/thesis/proj/iterate-over-tensor/enron/to-from-time.err
#SBATCH --partition=batch
#SBATCH --qos=medium
#SBATCH --constraint=hpcf2013
#SBATCH --nodes=1
#SBATCH --exclusive

export KMP_AFFINITY="verbose,compact"
export OMP_NUM_THREADS=16

srun /home/wmorgan1/cmarron_user/thesis/proj/iterate-over-tensor/pls -s .00000000000001 -n -c 1 -f /home/wmorgan1/cmarron_user/thesis/testData/to-from-time.txt -v &&

srun /home/wmorgan1/cmarron_user/thesis/proj/iterate-over-tensor/pls -s .00000000000001 -n -c 1 -f /home/wmorgan1/cmarron_user/thesis/testData/to-from-time.txt -v &&

srun /home/wmorgan1/cmarron_user/thesis/proj/iterate-over-tensor/pls -s .00000000000001 -n -c 1 -f /home/wmorgan1/cmarron_user/thesis/testData/to-from-time.txt -v &&

srun /home/wmorgan1/cmarron_user/thesis/proj/iterate-over-tensor/pls -s .00000000000001 -n -c 1 -f /home/wmorgan1/cmarron_user/thesis/testData/to-from-time.txt -v &&

srun /home/wmorgan1/cmarron_user/thesis/proj/iterate-over-tensor/pls -s .00000000000001 -n -c 1 -f /home/wmorgan1/cmarron_user/thesis/testData/to-from-time.txt -v