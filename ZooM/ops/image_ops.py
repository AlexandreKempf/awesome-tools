from scipy.ndimage import filters as filt
import numpy as np


def image_scale(img, low=0, high=1):
    """
    Normalize a img between two values `low` and `high`.

    **Parameters**

    > **img:** `img` -- img to normalize.

    > **low:** `float` -- default: `0` -- Minimum value after normalization.

    > **high:** `float` -- default: `1` -- Maximum value after normalization.


    **Returns**

    > `img` -- The img normalized.
    """
    img *= high-low
    img += low
    return img


def image_smooth(img, sigma=None):
    """
    Smooth a img with gaussian smoothing.

    **Parameters**

    > **img:** `img` -- Tensor to smooth.

    > **sigma:** `int` or `tuple` -- default: `None` -- The amount of smoothness as the std of the gaussian distribution.
    If `sigma` is an `int`, it smooth all the dimension with the same smoothness.
    If `sigma` is a `tuple`, it should have the same dimensionality as `img` and each sigma value correspond to a dimension.
    By default, smooth of 1/50 of the size of each dimension.

    **Returns**

    > `img` -- The img smoothed.
    """
    if sigma is None:
        sigma = np.array(img.shape)/50
        sigma[-1] = 0
    return filt.gaussian_filter(img, sigma)


def image_pool(img, binsize, binstep=None, fun='mean'):
    """
    Bin a img into bin of `binsize`, with a function `fun`.

    **Parameters**

    > **img:** `img` -- Tensor to smooth.

    > **binsize:** `int` or `tuple` -- Size of the bin
    If `binsize` is an `int`, it bins all the dimension with the same binsize.
    If `binsize` is a `tuple`, it should have the same dimensionality as `img` and each binsize value correspond to a dimension.

    > **binstep:** `int` or `tuple` -- default: `None` -- The step of the sliding window that bin
    If `binstep` is an `int`, it bins all the dimension with the same binstep.
    If `binstep` is a `tuple`, it should have the same dimensionality as `img` and each binstep value correspond to a dimension.
    By default, binstep is equal to binsize.

    > **fun:** `str` -- default: `mean` -- Function applied to reduce the bin into a single pixel. Should be in `["mean", "max", "min"]`


    **Returns**

    > `img` -- The img binned.
    """
    Ndim = img.ndim
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
            dims = np.array(img.shape)
            argdims = np.arange(img.ndim)
            argdims[0], argdims[dim] = argdims[dim], argdims[0]
            img = img.transpose(argdims)
            img = [fun(np.take(img, np.arange(int(i*binstep[dim]), int(i*binstep[dim]+binsize[dim])), 0), 0) for i in np.arange(dims[dim]//binstep[dim])]
            img = np.array(img).transpose(argdims)
    return img
