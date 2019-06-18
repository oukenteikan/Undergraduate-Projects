# To train a new model, use the main.py script.
#
# The command to reproduce the original TSN experiments of RGB modality on UCF101 can be

python main.py ucf101 RGB train_01.lst test_01.lst \
   --arch BNInception --num_segments 3 \
   --gd 20 --lr 0.001 --lr_steps 30 60 --epochs 80 \
   -b 128 -j 8 --dropout 0.8 \
   --snapshot_pref ucf101_bninception_

# For flow models:

#python main.py ucf101 Flow <ucf101_flow_train_list> <ucf101_flow_val_list> \
#   --arch BNInception --num_segments 3 \
#   --gd 20 --lr 0.001 --lr_steps 190 300 --epochs 340 \
#   -b 128 -j 8 --dropout 0.7 \
#   --snapshot_pref ucf101_bninception_ --flow_pref flow_

# For RGB-diff models:

# python main.py ucf101 RGBDiff <ucf101_rgb_train_list> <ucf101_rgb_val_list> \
#   --arch BNInception --num_segments 7 \
#   --gd 40 --lr 0.001 --lr_steps 80 160 --epochs 180 \
#   -b 128 -j 8 --dropout 0.8 \
#   --snapshot_pref ucf101_bninception_
