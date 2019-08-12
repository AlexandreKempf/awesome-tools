from inspect import getmembers, isfunction
import yaml
from copy import deepcopy
import importlib
import os.path


def _load_module(module):
    m = importlib.import_module(module)
    funs = [f for f in getmembers(m) if isfunction(f[1])]
    funs = {f[0]: f[1] for f in funs}
    return funs


def load_modules(modules):
    ops = {}
    for module in modules:
        ops.update(_load_module(module))
    return ops


def run_config(yaml_path, input_ref={'meta': {}}):
    yaml_file = yaml.safe_load(open(yaml_path, 'r'))
    ops = load_modules(yaml_file.get('modules', []))
    dico_kwargs = deepcopy(yaml_file.get('inputs', {}))
    dico_kwargs.update(input_ref)
    dico_kwargs['meta']['config'] = dico_kwargs['meta'].get('config', {})
    dico_kwargs['meta']['config'].update({yaml_path: yaml_file})
    dico_kwargs['meta']['ops'] = dico_kwargs['meta'].get('ops', {})
    dico_kwargs['meta']['ops'].update({yaml_path: ops})
    print(dico_kwargs['meta'])
    for iblock in yaml_file['flow']:
        if os.path.isfile(iblock['f']):
            output = run_config(iblock['f'], dico_kwargs)
        else:
            iargs = [dico_kwargs[a] for a in iblock.get('args', [])]
            ikwargs = iblock.get('kwargs', {})
            ifun = ops[iblock['f']]
            output = ifun(*iargs, **ikwargs)

        iout = iblock.get('out', [])
        if len(iout) == 1:
            output = {iblock['out'][0]: output}
        else:
            output = {iblock['out'][i]: output[i] for i in range(len(iblock['out']))}
        dico_kwargs.update(output)

    config_out = yaml_file.get('outputs', [])
    if not 'meta' in config_out:
        config_out.append('meta')
    return [dico_kwargs[v] for v in config_out]


yaml_path = '/home/alex/awesome/ZooM/flows/example.yaml'
out = run_config(yaml_path)
