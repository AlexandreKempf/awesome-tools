from scipy.ndimage import filters as filt
import numpy as np


def normalize_min_max(tensor, low=0, high=1, axis=None, img=False):
    """
    Normalize a tensor between two values `low` and `high`.

    **Parameters**

    > **tensor:** `tensor` -- Tensor to normalize.

    > **low:** `float` -- default: `0` -- Minimum value after normalization.

    > **high:** `float` -- default: `1` -- Maximum value after normalization.

    > **axis:** `int` -- default: `None` -- Axis in which the operation will be computed
    (ex: 0 for batch, if the normalization should be independant for each image).
    If not precise, take the full tensor and normalize it.

    > **img:** `bool` -- default: `False` -- Are the inputs images?
    Assume that the image have value between 0 and 1.


    **Returns**

    > `tensor` -- The tensor normalized.
    """
    if isinstance(tensor, list):
        tensor = np.array(tensor)
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


def normalize_avg_std(tensor, axis=None, img=False):
    """
    Normalize a tensor by substracting the mean and dividing by the std.

    **Parameters**

    > **tensor:** `tensor` -- Tensor to normalize.

    > **axis:** `int` -- default: `None` -- Axis in which the operation will be computed
    (ex: 0 for batch, if the normalization should be independant for each image).
    If not precise, take the full tensor and normalize it.

    > **img:** `bool` -- default: `False` -- Are the inputs images?
    Assume that the image have value between 0 and 1.


    **Returns**

    > `tensor` -- The tensor normalized.
    """
    if isinstance(tensor, list):
        tensor = np.array(tensor)
    tensor = tensor.astype(float)
    if not img:
        if axis is None:
            tensor -= np.mean(tensor)
            tensor *= 1/np.std(tensor)
        else:  # normalize by taking the avg and std over an axis
            axis = tuple(np.delete(np.arange(tensor.ndim), axis))
            tensor -= np.mean(tensor, axis, keepdims=True)
            tensor *= 1/np.std(tensor, axis, keepdims=True)
    else:
        tensor -= 0.5
        tensor *= 1/0.2
    return tensor


def smooth(tensor, sigma=None):
    """
    Smooth a tensor with gaussian smoothing.

    **Parameters**

    > **tensor:** `tensor` -- Tensor to smooth.

    > **sigma:** `int` or `tuple` -- default: `None` -- The amount of smoothness as the std of the gaussian distribution.
    If `sigma` is an `int`, it smooth all the dimension with the same smoothness.
    If `sigma` is a `tuple`, it should have the same dimensionality as `tensor` and each sigma value correspond to a dimension.
    By default, smooth of 1/50 of the size of each dimension.

    **Returns**

    > `tensor` -- The tensor smoothed.
    """
    if isinstance(tensor, list):
        tensor = np.array(tensor)

    if sigma is None:
        sigma = np.array(tensor.shape)/50
    return filt.gaussian_filter(tensor, sigma)


def pooling(tensor, binsize, binstep=None, fun='mean'):
    """
    Bin a tensor into bin of `binsize`, with a function `fun`.

    **Parameters**

    > **tensor:** `tensor` -- Tensor to smooth.

    > **binsize:** `int` or `tuple` -- Size of the bin
    If `binsize` is an `int`, it bins all the dimension with the same binsize.
    If `binsize` is a `tuple`, it should have the same dimensionality as `tensor` and each binsize value correspond to a dimension.

    > **binstep:** `int` or `tuple` -- default: `None` -- The step of the sliding window that bin
    If `binstep` is an `int`, it bins all the dimension with the same binstep.
    If `binstep` is a `tuple`, it should have the same dimensionality as `tensor` and each binstep value correspond to a dimension.
    By default, binstep is equal to binsize.

    > **fun:** `str` -- default: `mean` -- Function applied to reduce the bin into a single pixel. Should be in `["mean", "max", "min"]`


    **Returns**

    > `tensor` -- The tensor binned.
    """
    if isinstance(tensor, list):
        tensor = np.array(tensor)

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
