from inspect import getmembers, isfunction
import yaml
from copy import deepcopy
import importlib
import os.path
import numpy as np

def load_module(module):
    if isinstance(module, list):
        ops = {}
        for m in module:
            ops.update(load_module(m))
        return ops
    else:
        m = importlib.import_module(module)
        funs = [f for f in getmembers(m) if isfunction(f[1])]
        funs = {f[0]: f[1] for f in funs}
        return funs


def exec_block(block, dico, ops):
    iargs = [deepcopy(dico[arg]) for arg in block.get('args', [])]
    ikwargs = {k: deepcopy(v) for k, v in block.get('kwargs', {}).items()}
    if os.path.isfile(block['f']):  # if subflow
        out = run_config(block['f'], iargs, ikwargs, ops)
    else:
        ifun = ops[block['f']]
        out = ifun(*iargs, **ikwargs)
    iout = block.get('out', [])
    if len(iout) == 1:
        out = {iout[0]: out}
    else:
        out = {iout[i]: out[i] for i in range(len(iout))}
    return out


def exec_loop_block(block, dico, ops):
    variant = block.get('loop', [])
    if isinstance(variant, int):
        nb_loop = variant
        variant = []
    else:
        nb_loop = len(dico[variant[0]])
    invariant = [arg for arg in block.get('args', []) if arg not in variant]
    dico_loop = {k: v for k, v in block.get('kwargs', {}).items()}
    dico_loop.update({k: deepcopy(dico[k]) for k in invariant})
    # TODO check that all variant have the same len
    out = {k: [] for k in block.get('out', [])}
    for i in range(nb_loop):
        dico_loop.update({k: deepcopy(dico[k][i]) for k in variant})
        out_tmp = exec_block(block, dico_loop, ops)
        for k in out.keys():
            out[k].append(out_tmp[k])
    return out


def run_config(yaml_path, args=None, kwargs=None, ops=None):
    if args is None:
        args = []
    if kwargs is None:
        kwargs = {}
    if ops is None:
        ops = {}

    yaml_file = yaml.safe_load(open(yaml_path, 'r'))
    ops.update(load_module(yaml_file.get('modules', [])))

    name_args = yaml_file.get('args', [])
    dico = {name_args[i]: arg for i, arg in enumerate(args)}  # match the args
    dico.update({k: v for k, v in yaml_file.get('kwargs', {}).items()})  # fill kwargs with the subfile
    dico.update({k: v for k, v in kwargs.items()}) # fill kwargs with the mainfile

    # execute the flow
    for iblock in yaml_file['flow']:
        if iblock.get('loop', None) is None:
            out = exec_block(iblock, dico, ops)
        else:
            out = exec_loop_block(iblock, dico, ops)
        dico.update(out)

    # prepare the output
    config_out = yaml_file.get('out', [])
    if len(config_out) == 1:
        return dico[config_out[0]]
    else:
        return [dico[v] for v in config_out]


yaml_path = '/home/alex/awesome/ZooM/flows/example.yaml'
out = run_config(yaml_path)
