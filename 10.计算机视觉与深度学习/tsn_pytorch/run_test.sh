#!/usr/bin/env sh

now=$(date +"%Y%m%d_%H%M%S")

PART=Pose1
logfile=log/test-${now}.log

GLOG_vmodule=MemcachedClient=-1 OMP_NUM_THREADS=1 srun \
 --partition=${PART} \
 --mpi=pmi2 \
 --kill-on-bad-exit=1 \
 --gres=gpu:4 -n4 --tasks-per-node=4 \
 python test_models.py ucf101 RGB video_list/test_02.lst snapshot/ucf101_bninception__rgb_checkpoint.pth.tar \
   --arch BNInception --save_scores score/score_${now}.txt
 2>&1 | tee ${logfile} &
