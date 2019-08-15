def normalize_avg_std(tensor, axis=None):
    """
    Normalize a tensor by substracting the mean and dividing by the std.

    **Parameters**

    > **tensor:** `tensor` -- Tensor to normalize.

    > **axis:** `int` -- default: `None` -- Axis in which the operation will be computed
    (ex: 0 for batch, if the normalization should be independant for each image).
    If not precise, take the full tensor and normalize it.


    **Returns**

    > `tensor` -- The tensor normalized.
    """
    if isinstance(tensor, list):
        tensor = np.array(tensor)
    tensor = tensor.astype(float)
    if axis is None:
        tensor -= np.mean(tensor)
        tensor *= 1/np.std(tensor)
    else:  # normalize by taking the avg and std over an axis
        axis = tuple(np.delete(np.arange(tensor.ndim), axis))
        tensor -= np.mean(tensor, axis, keepdims=True)
        tensor *= 1/np.std(tensor, axis, keepdims=True)
    return tensor




def randomize(tensor, axis=0, N=None, replace=False):
    if isinstance(tensor, list):
        tensor = np.array(tensor)

    dim_n = tensor.shape[axis]
    if N is None:
        N = dim_n
    if N > dim_n:
        replace = True
    idx = np.random.choice(np.arange(dim_n), N, replace)
    return np.take(tensor, idx, axis)



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


def merge(front, back, point=None, extend='fix'):
