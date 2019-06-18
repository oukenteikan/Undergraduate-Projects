#!/usr/bin/env sh

now=$(date +"%Y%m%d_%H%M%S")

PART=Test
logfile=log/train-${now}.log

GLOG_vmodule=MemcachedClient=-1 OMP_NUM_THREADS=1 srun \
 --partition=${PART} \
 --mpi=pmi2 \
 --kill-on-bad-exit=1 \
 --gres=gpu:4 -n4 --tasks-per-node=4 \
 python p3d_main.py ucf101 RGB video_list/train_02.lst video_list/test_02.lst \
   --arch BNInception --num_segments 4 \
   --gd 20 --lr 0.001 --lr_steps 30 60 --epochs 80 \
   -b 8 -j 4 --dropout 0.8 \
   --snapshot_pref snapshot/ucf101_bninception_
 2>&1 | tee ${logfile} &
