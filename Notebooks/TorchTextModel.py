from torch import nn
import torch.nn.functional as fun

class TorchTextModel(nn.Module):
    def __init__(self, vocab_size, embed_dim, num_class):
        super(TorchTextModel, self).__init__()
        self.embedding = nn.EmbeddingBag(vocab_size, embed_dim, sparse=True)
        self.fc1=nn.Linear(embed_dim, 64)
        self.fc2=nn.Linear(64,16)
        self.fc3=nn.Linear(16, num_class)
        self.init_weights()

    def init_weights(self):
        initrange = 0.5
        self.embedding.weight.data.uniform_(-initrange, initrange)
        self.fc1.weight.data.uniform_(-initrange, initrange)
        self.fc1.bias.data.zero_()
        self.fc2.weight.data.uniform_(-initrange, initrange)
        self.fc2.bias.data.zero_()
        self.fc3.weight.data.uniform_(-initrange, initrange)
        self.fc3.bias.data.zero_()

    def forward(self, text, offsets):
        embedded = self.embedding(text, offsets)
        x = fun.relu(self.fc1(embedded))
        x = fun.relu(self.fc2(x))
        x = self.fc3(x)
        return x

