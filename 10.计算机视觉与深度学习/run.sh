PART=Pose1

GLOG_vmodule=MemcachedClient=-1 OMP_NUM_THREADS=1 srun \
 --partition=${PART} \
 --mpi=pmi2 \
 --kill-on-bad-exit=1 \
 --gres=gpu:1 -n1 --tasks-per-node=1 \
 /usr/bin/python train.py \
 --features=/mnt/lustre/share/huangrenze/THUMOS2014/feature \
 2>&1
