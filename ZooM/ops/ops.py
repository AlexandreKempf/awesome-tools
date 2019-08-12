import torch
import torch.nn.functional as F


def one_hot(labels):
    labels = torch.tensor(labels)
    return F.one_hot(labels)
