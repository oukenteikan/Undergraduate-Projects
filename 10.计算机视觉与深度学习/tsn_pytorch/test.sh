# After training, there will checkpoints saved by pytorch, for example ucf101_bninception_rgb_checkpoint.pth.
#
# Use the following command to test its performance in the standard TSN testing protocol:

python test_models.py ucf101 RGB <ucf101_rgb_val_list> ucf101_bninception_rgb_checkpoint.pth \
   --arch BNInception --save_scores <score_file_name>

# Or for flow models:

#python test_models.py ucf101 Flow <ucf101_rgb_val_list> ucf101_bninception_flow_checkpoint.pth \
#   --arch BNInception --save_scores <score_file_name> --flow_pref flow_
