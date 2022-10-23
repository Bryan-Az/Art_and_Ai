import torch
import torchvision
from torch.utils.data import Dataset, DataLoader
import numpy as np
import pandas as pd
import math
from sklearn import preprocessing

class TitleDataset(Dataset):

    def __init__(self):
        # data loading
        feature = pd.read_csv('../../data_samples/results/en_titles.csv', index_col=0)
        target = pd.read_csv('../../data_samples/continents.csv')
        ### here we turn the data into tokens?
        ### then we load as numpy after tokenization?
        self.x = feature
        self.y = target
        self.n_samples = feature.shape[0]


    def __getitem__(self, index):
        # dataset[i]
        return self.x.iloc[index, 0], self.y.iloc[index, 0]

    def __len__(self):
        # len(dataset)
        return self.n_samples
