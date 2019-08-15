from scipy.ndimage import filters as filt
import numpy as np


def normalize_min_max(tensor, low=0, high=1, axis=None, img=False):
    tensor = tensor.astype(float)
    if not img:  # no initial rescale for images
        if axis is None:
            tensor -= np.min(tensor)
            tensor *= 1/np.max(tensor)
        else:  # normalize by taking the min and max over an axis
            axis = tuple(np.delete(np.arange(tensor.ndim), axis))
            tensor -= np.min(tensor, axis, keepdims=True)
            tensor *= 1/np.max(tensor, axis, keepdims=True)
    tensor *= high-low
    tensor += low
    return tensor


def normalize_avg_std(tensor, axis=None):
    tensor = tensor.astype(float)
    if axis is None:
        tensor -= np.mean(tensor)
        tensor *= 1/np.std(tensor)
    else:  # normalize by taking the avg and std over an axis
        axis = tuple(np.delete(np.arange(tensor.ndim), axis))
        tensor -= np.mean(tensor, axis, keepdims=True)
        tensor *= 1/np.std(tensor, axis, keepdims=True)
    return tensor


def smooth(tensor, sigma=None):
    if sigma is None:
        sigma = np.array(tensor.shape)/100
    return filt.gaussian_filter(tensor, sigma)


def pooling(tensor, binsize, binstep=None, fun='mean'):
    Ndim = tensor.ndim
    if not isinstance(binsize, (list, tuple)):
        binsize = np.repeat(binsize, Ndim)

    if binstep is None:
        binstep = binsize
    elif not isinstance(binstep, (list, tuple)):
        binstep = np.repeat(binstep, Ndim)

    if fun == "mean":
        fun = np.nanmean
    elif fun == "max":
        fun = np.nanmax
    elif fun == "min":
        fun = np.nanmin

    for dim in range(Ndim):
        if binsize[dim] != 1:
            dims = np.array(tensor.shape)
            argdims = np.arange(tensor.ndim)
            argdims[0], argdims[dim] = argdims[dim], argdims[0]
            tensor = tensor.transpose(argdims)
            tensor = [fun(np.take(tensor, np.arange(int(i*binstep[dim]), int(i*binstep[dim]+binsize[dim])), 0), 0) for i in np.arange(dims[dim]//binstep[dim])]
            tensor = np.array(tensor).transpose(argdims)
    return tensor


def concatenate(*args, axis=0):
    return np.concatenate([*args], axis)


def randomize(tensor, axis=0, N=None, replace=False):


def merge(front, back, point=None, extend='fix'):

def one_hot(labels):




x = np.arange(5400).reshape(3,30,30,2).astype(float)
