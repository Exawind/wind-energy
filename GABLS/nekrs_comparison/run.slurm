#!/bin/bash
#BSUB -P CFD116
#BSUB -W 0:30
#BSUB -nnodes 8 
#BSUB -alloc_flags gpumps
#BSUB -J RunSim123
#BSUB -o RunSim123.%J
#BSUB -e RunSim123.%J

module load gcc
module load cuda
module load cmake
module load netcdf-c

jsrun -n 48 -a 1 -c 1 -g 1 -r 6 -l CPU-CPU -d packed -b packed:1 ./amr-wind/build/amr_wind input.i  > log


