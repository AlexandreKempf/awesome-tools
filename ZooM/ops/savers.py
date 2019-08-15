import os
import yaml
import matplotlib.pyplot as plt
import numpy as np
import json

class _NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def save_yaml(data, path, dirname=''):
    with open(os.path.join(dirname, path), 'w') as file:
        yaml.dump(data, file, default_flow_style=False)


def save_json(data, path, dirname=''):
    with open(os.path.join(dirname, path), 'w') as file:
        json.dump(data, file, cls=_NumpyEncoder)


def save_image(image, mask, path, dirname=''):
    data = np.concatenate([image, np.expand_dims(mask, -1)], -1)
    plt.imsave(os.path.join(dirname, path), data)


def save_text(data, path, dirname='', mode='w'):
    with open(os.path.join(dirname, path), mode) as file:
        file.writelines(data)
