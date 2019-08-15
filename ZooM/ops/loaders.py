import os
import yaml
import matplotlib.pyplot as plt
import numpy as np
import json

def load_yaml(path, dirname):
    """
    input: a yaml file
    outputs: the yaml file loaded in alphabetical order
    """
    res = yaml.safe_load(open(os.path.join(dirname, path), 'r'))
    if isinstance(res, dict):
        keys = sorted(res)
        res = [res[k] for k in keys]
    return (*res,)


def load_json(path, dirname):
    """
    input: a json file
    outputs: the json file loaded in alphabetical order
    """
    res = json.load(open(os.path.join(dirname, path), 'r'))
    if isinstance(res, dict):
        keys = sorted(res)
        res = [res[k] for k in keys]
    return (*res,)


def load_img(path, dirname=''):
    """
    input: a PATH or a list of path relative to the DIRNAME
    outputs: an image and an alpha channel, or a list of images and a list of alpha channels
    """
    if isinstance(path, list):
        imgs = []
        alphas = []
        for p in path:
            img, alpha = load_img(p, dirname)
            imgs.append(img)
            alphas.append(alpha)
        return imgs, alphas

    elif isinstance(path, str):
        img = plt.imread(os.path.join(dirname, path))
        h, w, c = img.shape
        if c <= 3:
            return img, np.ones((h, w))
        else:
            return img[...,:3], img[...,3]


def load_txt(path, dirname=''):
    """
    input: a PATH or a list of path relative to the DIRNAME
    outputs: an list of str, or a list of lists of str
    """
    if isinstance(path, list):
        txts = []
        for p in path:
            txts.append(load_txt(p, dirname))
        return txts

    elif isinstance(path, str):
        with open(os.path.join(dirname, path), 'r') as file:
            return file.readlines()
