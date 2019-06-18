import argparse
import os
import time

import numpy as np
import torch
import torch.optim as optim
from torch.autograd import Variable
from torch.utils.data import DataLoader

import data
import models
from data import TrainSplit, EvaluateSplit

def iou(interval, featstamps, return_index=False):
    start_i, end_i = interval[0], interval[1] 
    output = 0.0
    gt_index = -1
    for i, (start, end) in enumerate(featstamps):
        intersection = max(0, min(end, end_i) - max(start, start_i))	
	union = min(max(end, end_i) - min(start, start_i), end - start + end_i - start_i)
        overlap = float(intersection) / (union + 1e-8)
        if overlap >= output:
            output = overlap
            gt_index = i
    if return_index:
        return output, gt_index
    return output

def proposals_to_timestamps(proposals, duration, num_proposals):
    _, nb_steps, K = proposals.size()
    if num_proposals and num_proposals < nb_steps * K:
        sort, _ = proposals.view(nb_steps * K).sort()
        score_threshold = sort[-num_proposals]
        proposals = proposals >= score_threshold
    step_length = duration / (nb_steps + 1)
    timestamps = []
    for time_step in np.arange(nb_steps):
        p = proposals[0, time_step]
        if p.sum() != 0:
            for k in np.arange(K):
                if p[k] != 0:
                    start = max(0, time_step - k) * step_length
		    end = min((time_step + k + 2) * step_length, duration)
                    timestamps.append((start, end))
    return timestamps


def calculate_stats(proposals, gt_times, duration, args):
    timestamps = proposals_to_timestamps(proposals.data, duration, args.num_proposals)
    gt_detected = np.zeros(len(gt_times))
    for i, timestamp in enumerate(timestamps):
        iou_i, k = iou(timestamp, gt_times, return_index=True)
        if iou_i > args.iou_threshold:
            gt_detected[k] = 1
    return gt_detected.sum()*1./len(gt_detected)

def evaluate(data_loader, maximum):
    model.eval()
    total = len(data_loader)
    total = min(total, maximum)
    recall = np.zeros(total)
    for batch_idx, (features, gt_times, duration) in enumerate(data_loader):
        if batch_idx >= maximum:
            break
        features = features.cuda()
        features = Variable(features)
        proposals = model(features)
    recall[batch_idx] = calculate_stats(proposals, gt_times, duration, args)
    return np.mean(recall)

def train(epoch):
    total_loss = []
    model.train()
    start_time = time.time()
    for batch_idx, (features, masks, labels) in enumerate(train_loader):
	features = features.cuda()
        labels = labels.cuda()
        masks = masks.cuda()
        features = Variable(features)
        optimizer.zero_grad()
        proposals = model(features)
        loss = model.compute_loss(proposals, masks, labels)
        loss.backward()
        optimizer.step()
        total_loss.append(loss.data[0])

        if batch_idx % args.log_interval == 0:
            cur_loss = total_loss[-1]
            elapsed = time.time() - start_time
            log_entry = '| epoch {:3d} | {:5d}/{:5d} batches | lr {:02.4f} | ms/batch {:5.2f} | ' \
                        'loss {:5.6f}'.format(
                    epoch, batch_idx, len(train_loader), args.lr,
                    elapsed * 1000 / args.log_interval, cur_loss * 1000)
            print (log_entry)
            start_time = time.time()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='video features to LSTM Language Model')

    parser.add_argument('--dataset', type=str, default='THUMOS',
                    help='Name of the data class to use from data.py')
    parser.add_argument('--features', type=str, default='./feature',
                    help='location of the video features')
    parser.add_argument('--training-ids', type=str, default='./training_ids.txt',
                    help='location of the training ids')
    parser.add_argument('--validation-ids', type=str, default='./validation_ids.txt',
                    help='location of the validation ids')
    parser.add_argument('--gt-times', type=str, default='./gt_time',
                    help='ground truth times')
    parser.add_argument('--durations', type=str, default='./duration.txt',
                    help='video length')
    parser.add_argument('--save', type=str, default='./model',
                    help='path to folder where to save the final model and log files and corpus')
    parser.add_argument('--save-every', type=int, default=1,
                    help='Save the model every x epochs')
    parser.add_argument('--W', type=int, default=128,
                    help='The rnn kernel size to use to get the proposal features')
    parser.add_argument('--K', type=int, default=64,
                    help='Number of proposals')
    parser.add_argument('--max-W', type=int, default=128,
                    help='maximum number of windows to return per video')
    parser.add_argument('--video-dim', type=int, default=4096,
                    help='dimensions of video (C3D) features')
    parser.add_argument('--hidden-dim', type=int, default=512,
                    help='dimensions output layer of video network')
    parser.add_argument('--lr', type=float, default=0.1,
                    help='initial learning rate')
    parser.add_argument('--momentum', type=float, default=0.9,
                    help='SGD momentum')
    parser.add_argument('--weight-decay', type=float, default=0,
                    help='SGD weight decay')
    parser.add_argument('--epochs', type=int, default=100,
                    help='upper epoch limit')
    parser.add_argument('--batch-size', type=int, default=1,
                    help='batch size')
    parser.add_argument('--nthreads', type=int, default=4,
                    help='number of worker threas used to load data')
    parser.add_argument('--resume', dest='resume', action='store_true',
                    help='reload the model')
    parser.add_argument('--iou-threshold', type=float, default=0.5,
                    help='threshold above which we say something is positive')
    parser.add_argument('--num-proposals', type=int, default=1000,
                    help='number of top proposals to evaluate')
    parser.add_argument('--log-interval', type=int, default=1, metavar='N',
                    help='report interval')

    args = parser.parse_args()

    if not os.path.isdir(args.save):
        os.makedirs(args.save)

###############################################################################
# Load data
###############################################################################

    print ("| Loading data=")
    dataset = getattr(data, args.dataset)(args)
    train_dataset = TrainSplit(dataset.training_ids, dataset, args)
    val_dataset = EvaluateSplit(dataset.validation_ids, dataset, args)
    train_val_dataset = EvaluateSplit(dataset.training_ids, dataset, args)
    print ("| Dataset created")

    train_loader = DataLoader(train_dataset, shuffle=True, batch_size=args.batch_size, num_workers=args.nthreads,
                          collate_fn=train_dataset.collate_fn)
    train_evaluator = DataLoader(train_val_dataset, shuffle=True, batch_size=1, num_workers=args.nthreads,
                             collate_fn=val_dataset.collate_fn)
    val_evaluator = DataLoader(val_dataset, shuffle=True, batch_size=1, num_workers=args.nthreads,
                           collate_fn=val_dataset.collate_fn)

    print ("| Data Loaded: # training data: %d, # val data: %d" % (len(train_loader) * args.batch_size, len(val_evaluator)))

###############################################################################
# Build the model
###############################################################################

    if args.resume:
        model = torch.load(os.path.join(args.save, 'model_70.pth'))
    else:
        model = models.SST(
            video_dim=args.video_dim,
            hidden_dim=args.hidden_dim,
            W=args.W,
            K=args.K,
        )

    model.cuda()

    optimizer = optim.SGD(model.parameters(), lr=args.lr, momentum=args.momentum, weight_decay=args.weight_decay)

###############################################################################
# Training code
###############################################################################
    
    for epoch in range(1, args.epochs + 1):
        epoch_start_time = time.time()
        train(epoch)
        recall = evaluate(val_evaluator, maximum=500)
        log_entry = ('| end of epoch {:3d} | time: {:5.2f}s | val recall@{}-iou={}: {:2.2f}\%'.format(
                epoch, (time.time() - epoch_start_time), args.num_proposals, args.iou_threshold, recall))
        print (log_entry)
        if args.save != '' and epoch % args.save_every == 0:
            torch.save(model, os.path.join(args.save, 'model_' + str(epoch) + '.pth'))
