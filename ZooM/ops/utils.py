import numpy as np


def concatenate(*args, axis=0):
    return np.concatenate([*args], axis)


def one_hot(labels, nmax=None):
    labels = np.array(labels).astype(int)
    n = labels.size
    if nmax is None:
        nmax = np.max(labels)+1
    onehot = np.zeros((n, nmax))
    onehot[np.arange(n), labels] = 1
    return onehot


# def merge(front, back, point=None, extend='fix'):
