import torch
import torch.nn as nn


class SST(nn.Module):
    def __init__(self,
                 video_dim=4096,
                 hidden_dim=512,
                 dropout=0,
                 W=64,
                 K=64,
                 rnn_type='GRU',
                 rnn_num_layers=2,
                 rnn_dropout=0
                 ):
        super(SST, self).__init__()
        self.rnn = getattr(nn, rnn_type)(video_dim, hidden_dim, rnn_num_layers, batch_first=True, dropout=rnn_dropout, bidirectional = True)
        self.scores = torch.nn.Linear(hidden_dim*2, K)

        # Saving arguments
        self.video_dim = video_dim
        self.W = W
        self.rnn_type = rnn_type
        self.rnn_num_layers = rnn_num_layers
        self.rnn_dropout = rnn_dropout
        self.K = K

    def forward(self, features):
	print (features.size())
        N, T, _ = features.size()
        rnn_output, _ = self.rnn(features)
        rnn_output = rnn_output.contiguous()
        rnn_output = rnn_output.view(rnn_output.size(0) * rnn_output.size(1), rnn_output.size(2))
        outputs = torch.sigmoid(self.scores(rnn_output))
	print(outputs.size())
        return outputs.view(N, T, self.K)

    def compute_loss(self, outputs, masks, labels):
        labels = labels.view(-1)
        masks = masks.view(-1)
        outputs = outputs.view(-1)

        ones = torch.sum(labels)
        total = labels.nelement()

        weights = torch.FloatTensor(outputs.size()).type_as(outputs.data)
        weights[labels.long() == 1] = 1.0 - ones / total
        weights[labels.long() == 0] = ones / total
        weights = weights.view(weights.size(0), 1).expand(weights.size(0), 2)

        outputs = outputs.clamp(min=1e-8)
        log_outputs = torch.log(outputs)
        neg_outputs = 1.0 - outputs
        neg_outputs = neg_outputs.clamp(min=1e-8)
        neg_log_outputs = torch.log(neg_outputs)
        all_outputs = torch.cat((log_outputs.view(-1, 1), neg_log_outputs.view(-1, 1)), 1)

        all_values = all_outputs.mul(torch.autograd.Variable(weights))
        all_labels = torch.autograd.Variable(torch.cat((labels.view(-1, 1), (1.0 - labels).view(-1, 1)), 1))
        all_masks = torch.autograd.Variable(torch.cat((masks.view(-1, 1), masks.view(-1, 1)), 1))
        loss = -torch.sum(all_values.mul(all_labels).mul(all_masks)) / outputs.size(0)
        return loss
