#!/bin/bash

#SBATCH --job-name=unstableabl
#SBATCH --account=hfm
#SBATCH --nodes=16
#SBATCH --time=23:59:59
#SBATCH --partition=standard
#SBATCH -o %x.o%j
## #SBATCH -o output1

#SBATCH --mail-user=lcheung@sandia.gov # email address
#SBATCH --mail-type=ALL               # email all notifications  

module purge
#source /nopt/nrel/ecom/exawind/exawind/scripts/exawind-env-gcc.sh
#exawind_load_deps netcdf-c
source /projects/hfm/lcheung/spack-manager/environments/test2/load.sh


ranks_per_node=36
mpi_ranks=$(expr $SLURM_JOB_NUM_NODES \* $ranks_per_node)
export OMP_NUM_THREADS=1  # Max hardware threads = 4
export OMP_PLACES=threads
export OMP_PROC_BIND=spread


EXE=amr_wind
exawind_exec=`which $EXE`
CONFFILE=ATLVINEYARD_test1.inp

#exawind_exec=`which amr_wind`
#${HOME}/exawind/source/exawind-driver/build/exawind

echo "Job name       = $SLURM_JOB_NAME"
echo "Num. nodes     = $SLURM_JOB_NUM_NODES"
echo "Num. MPI Ranks = $mpi_ranks"
echo "Num. threads   = $OMP_NUM_THREADS"
echo "Working dir    = $PWD"
echo "EXE            = $exawind_exec"

#cp ${exawind_exec} $(pwd)
srun -n ${mpi_ranks} -c 1  --cpu_bind=cores ${exawind_exec} ${CONFFILE}
#srun -n ${mpi_ranks} -c 1 --cpu_bind=cores $(pwd)/exawind --awind 18 --nwind 18 exwsim.yaml
