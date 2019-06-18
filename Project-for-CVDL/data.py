import struct
import os
import math
import numpy as np
import torch
from torch.utils.data import Dataset

class THUMOS(object):
    def __init__(self, args):
        self.features_path = args.features
        print (args.features)

        self.gt_times_path = args.gt_times
        print (args.gt_times)

        self.durations_path = args.durations
        print (args.durations)

        self.training_ids_path = args.training_ids
        print (args.training_ids)
        with open(self.training_ids_path, 'r') as f:
            self.training_ids = f.read()
        self.training_ids = self.training_ids.splitlines()

        self.validation_ids_path = args.validation_ids
        print (args.validation_ids)
        with open(self.validation_ids_path, 'r') as f:
            self.validation_ids = f.read()
        self.validation_ids = self.validation_ids.splitlines()

        temp_gt_times = {}
        for video in self.training_ids:
            temp_gt_times[video] = []
            f = open(os.path.join(self.gt_times_path, video + ".gt_time"))
            content = f.read().split()
            for i in range(len(content)):
                if (i%2 == 0):
                    temp_gt_times[video].append((float(content[i]), float(content[i+1])))
            f.close()
        for video in self.validation_ids:
            temp_gt_times[video] = []
            f = open(os.path.join(self.gt_times_path, video + ".gt_time"))
            content = f.read().split()
            for i in range(len(content)):
                if (i%2 == 0):
                    temp_gt_times[video].append((float(content[i]), float(content[i+1])))
            f.close()
        self.gt_times = temp_gt_times

        temp_durations = {}
        f = open(self.durations_path)
        content = f.read().split()
        for i in range(len(content)):
            if (i%2 == 0):
                temp_durations[content[i]] = content[i+1]
        f.close()
        self.durations = temp_durations

class DataSplit(Dataset):
    def __init__(self, video_ids, dataset, args):
        self.video_ids = video_ids
        self.features_path = dataset.features_path
        self.durations = dataset.durations
        self.gt_times = dataset.gt_times
        self.W = args.W
        self.K = args.K
        self.max_W = args.max_W
        self.masks = np.zeros((self.max_W, self.W, self.K))
        for index in range(self.W):
            self.masks[:, index, :min(self.K, index, self.W - self.K)] = 1
        self.masks = torch.FloatTensor(self.masks)
    def __getitem__(self, index):
        pass
    def __len__(self):
        return len(self.video_ids)

class TrainSplit(DataSplit):
    def __init__(self, video_ids, dataset, args):
        super(self.__class__, self).__init__(video_ids, dataset, args)
    def collate_fn(self, data):
        features = [d[0] for d in data]
        masks = [d[1] for d in data]
        labels = [d[2] for d in data]
        return torch.cat(features, 0), torch.cat(masks, 0), torch.cat(labels, 0)
    def __getitem__(self, index):
        video = self.video_ids[index]
	video_path = os.path.join(self.features_path, video)
        features = []
        for f in os.listdir(video_path):
            f_path = os.path.join(video_path, f)
            f_ = open(f_path, 'rb')
            x = f_.read()
            features.append(struct.unpack('4096f', x[20:]))
            f_.close()

        gt_times = self.gt_times[video]
        duration = float(self.durations[video])
        features = np.array(features)	
	
        labels = np.zeros( (features.shape[0], self.K) )
        half_step = duration / (features.shape[0] + 1)

        for slip in gt_times:
            first = int(math.ceil(slip[0]/half_step))
            last = int(math.floor(slip[1]/half_step - 2))
            for i in range(0, self.K):
                if (first + i <= last - i):
                    for j in range(first + i, last - i + 1):
                        if j < features.shape[0]:
                            labels[j][i] = 1

        nfeats = features.shape[0]
        nWindows = max(1, nfeats - self.W + 1)
        sample = range(nWindows)
        if self.max_W < nWindows:
            sample = np.random.choice(nWindows, self.max_W)
            nWindows = self.max_W
        masks = self.masks[:nWindows, :, :]
        feature_windows = np.zeros((nWindows, self.W, features.shape[1]))
        label_windows = np.zeros((nWindows, self.W, self.K))
        for j, w_start in enumerate(sample):
            w_end = min(w_start + self.W, nfeats)
            feature_windows[j, 0:w_end - w_start, :] = features[w_start:w_end, :]
            label_windows[j, 0:w_end - w_start, :] = labels[w_start:w_end, :]
        return torch.FloatTensor(feature_windows), masks, torch.Tensor(label_windows)

class EvaluateSplit(DataSplit):
    def __init__(self, video_ids, dataset, args):
        super(self.__class__, self).__init__(video_ids, dataset, args)
    def collate_fn(self, data):
        features = data[0][0]
        gt_times = data[0][1]
        durations = data[0][2]
        return features.view(1, features.size(0), features.size(1)), gt_times, durations
    def __getitem__(self, index):
        video = self.video_ids[index]
        video_path = os.path.join(self.features_path, video)
        features = []
        for f in os.listdir(video_path):
            f_path = os.path.join(video_path, f)
            f_ = open(f_path, 'rb')
            x = f_.read()
            features.append(struct.unpack('4096f', x[20:]))
            f_.close()

        gt_times = self.gt_times[video]
        duration = float(self.durations[video])
        features = np.array(features)

        return torch.FloatTensor(features), gt_times, duration

