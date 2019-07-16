import yaml
import operators.operators as operators
from inspect import getmembers, isfunction


def load_module(module):
    funs = [f for f in getmembers(module) if isfunction(f[1])]
    funs = {f[0]: f[1] for f in funs}
    return funs


def load_modules(modules):
    funs = {}
    for module in modules:
        funs.update(load_module(module))
    return funs


def execute_pipeline(yaml_path, funs):
    yaml_file = yaml.safe_load(open(yaml_path, 'r'))
    dico_kwargs = yaml_file['inputs']
    dico_kwargs['config'] = yaml_file
    for iblock in yaml_file['pipeline']:
        iargs = [dico_kwargs[a] for a in iblock.get('args', [])]
        ikwargs = iblock.get('kwargs', {})
        ifun = funs[iblock['f']]
        iout = iblock.get('out', [])
        output = ifun(*iargs, **ikwargs)
        if len(iout) == 1:
            output = {iblock['out'][0]: output}
        else:
            output = {iblock['out'][i]: output[i] for i in range(len(iblock['out']))}
        dico_kwargs.update(output)
    return dico_kwargs


funs = load_modules([operators])
yaml_path = '/home/alex/awesome/ZooM/preprocessing/preprocess_classif.yaml'
out = execute_pipeline(yaml_path, funs)
