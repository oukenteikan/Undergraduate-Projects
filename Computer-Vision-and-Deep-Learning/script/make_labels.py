features = 
gt_times = 
duration = 

labels = np.zeros( (features.shape[0], self.K) )
half_step = duration / (features.shape[0] + 1)
for slip in gt_times:
    first = math.ceil(slip[0]/half_step)
    last = math.floor(slip[0]/half_step - 2)
    for i in range(0, self.K):
        if (first + i < last - i):
            for j in range(first + i, last - i):
                labels[j][i] = 1