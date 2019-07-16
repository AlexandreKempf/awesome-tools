import yaml
import torch
import matplotlib.pyplot as plt
import os
import uuid
import torch.nn.functional as F


def load_yaml(path):
    """
    input: a yaml file
    outputs: the yaml file loaded in alphabetical order
    """
    res = yaml.safe_load(open(path, 'r'))
    if isinstance(res, dict):
        keys = sorted(res)
        res = [res[k] for k in keys]
    return (*res,)


def load_imgs(paths, dirname=None):
    """
    input: a list of img path on ROOT_PATH
    outputs: a list with the images
    """
    if dirname is not None:
        paths = [os.path.join(dirname, p) for p in paths]

    imgs = []
    for p in paths:
        imgs.append(plt.imread(p))
    return imgs


def one_hot(labels):
    labels = torch.tensor(labels)
    return F.one_hot(labels)


def save_dataset(imgs, targets, path):
    id = str(uuid.uuid4()).replace('-', '')
    path = os.path.join(os.path.dirname(path), id)
    os.mkdir(path)
    torch.save(imgs, os.path.join(path, 'inputs.pt'))
    torch.save(targets, os.path.join(path, 'target.pt'))
    return path
