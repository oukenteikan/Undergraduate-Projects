import argparse
import torch
from torchvision import transforms

import opt
from places2 import Places2
from evaluation import evaluate
from net import PConvUNet
from util.io import load_ckpt

parser = argparse.ArgumentParser()
# training options
parser.add_argument('--root', type=str, default='./datasets')
parser.add_argument('--snapshot', type=str, default='./snapshots/default/ckpt')
parser.add_argument('--image_size', type=int, default=256)
parser.add_argument('--mask_root', type=str, default='./masks')
args = parser.parse_args()

device = torch.device('cuda')

size = (args.image_size, args.image_size)
img_transform = transforms.Compose(
    [transforms.Resize(size=size), transforms.ToTensor(),
     transforms.Normalize(mean=opt.MEAN, std=opt.STD)])
mask_transform = transforms.Compose(
    [transforms.Resize(size=size), transforms.ToTensor()])

dataset_val = Places2(args.root, args.mask_root, img_transform, mask_transform, 'val')

model = PConvUNet().to(device)
load_ckpt(args.snapshot+'/135000.pth', [('model', model)])

model.eval()
evaluate(model, dataset_val, device, 'result.jpg')
