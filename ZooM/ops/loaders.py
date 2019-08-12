import os
import yaml
import matplotlib.pyplot as plt


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
