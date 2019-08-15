import os
import yaml
import matplotlib.pyplot as plt
import numpy as np
import json


def load_yaml(path, dirname=''):
    """
    Load a YAML file into a tuple of variables

    **Parameters**

    > **path:** `str` -- Path to the YAML file relative to `dirname`.

    > **dirname:** `str` -- default: `''` -- Path to the reference point (ex: working directory).

    **Returns**

    > `tuple` -- Collection of objects sorted by alphabetical order.
    """
    res = yaml.safe_load(open(os.path.join(dirname, path), 'r'))
    if isinstance(res, dict):
        keys = sorted(res)
        res = [res[k] for k in keys]
    return (*res,)


def load_json(path, dirname=''):
    """
    Load a JSON file into a tuple of variables

    **Parameters**

    > **path:** `str` -- Path to the JSON file relative to `dirname`.

    > **dirname:** `str` -- default: `''` -- Path to the reference point (ex: working directory).


    **Returns**

    > `tuple` -- Collection of objects sorted by alphabetical order.

    See also:
        - [load_yaml](loaders.md#load_yaml)
    """
    res = json.load(open(os.path.join(dirname, path), 'r'))
    if isinstance(res, dict):
        keys = sorted(res)
        res = [res[k] for k in keys]
    return (*res,)


def load_image(path, dirname=''):
    """
    Load an image or a collection of images

    **Parameters**

    > **path:** `str` -- Path to the image file relative to `dirname`.

    > **dirname:** `str` -- default: `''` -- Path to the reference point (ex: working directory).


    **Returns**

    > `img` -- Image (row, col, 3), in float from 0 to 1

    > `mask` -- Mask (row, col, 1), in float from 0 (transparent) to 1 (opaque).


    """
    img = plt.imread(os.path.join(dirname, path))
    h, w, c = img.shape
    if c <= 3:
        return img, np.ones((h, w))
    else:
        return img[..., :3], img[..., 3]


def load_text(path, dirname=''):
    """
    Load an text file or a collection of text files

    **Parameters**

    > **path:** `str` -- Path to the text file relative to `dirname`.

    > **dirname:** `str` -- default: `''` -- Path to the reference point (ex: working directory).

    **Returns**

    > `list` -- List of lines from the file

    !!! tip "Load a list of text files"
        The fonction works also with a list of text files as input.
        Then it returns a list of list of lines.
    """
    with open(os.path.join(dirname, path), 'r') as file:
        return file.readlines()
