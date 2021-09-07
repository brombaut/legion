#!/bin/sh
#SBATCH --constraint=gpu
#SBATCH --time=00:30:00
#SBATCH --mail-type=ALL
#SBATCH -A d108

root_dir="$PWD"

export LD_LIBRARY_PATH="$PWD"

ulimit -S -c 0 # disable core dumps

export GASNET_PHYSMEM_MAX=16G # hack for some reason this seems to be necessary on Piz Daint now

if [[ ! -d paint ]]; then mkdir paint; fi
pushd paint

for n in $SLURM_JOB_NUM_NODES; do
  for r in 0 1 2 3 4; do
    echo "Running $n""x1_r$r"
    srun -n $n -N $n --ntasks-per-node 1 --cpu_bind none "$root_dir/circuit.idx" -npp 5000 -wpp 20000 -l 50 -p $(( $n * 10 )) -pps 10 -prune 30 -hl:sched 1024 -ll:gpu 1 -ll:util 2 -ll:bgwork 2 -ll:csize 15000 -ll:fsize 15000 -ll:zsize 2048 -ll:rsize 512 -ll:gsize 0 -level 5 -dm:replicate 1 -dm:same_address_space | tee out_"$n"x1_r"$r".log
    #  -dm:memoize -lg:no_fence_elision -lg:parallel_replay 2
  done
done

popd