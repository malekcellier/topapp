# Author: Malek Cellier
# Email: malek.cellier@gmail.com
# Created: 2019-07-08

import os
import yaml


class Presets:
    """Handles the yaml presets

    Args:

    Attributes:
        motions (dict): the motion presets
        positions (dict): the positions presets
    """
    _presets = {}
    file_names = ['topology', 'positions', 'motions', 'nodes'] 
    file_path = os.path.dirname(__file__)
    for name in file_names:
        file_name = os.path.join('presets', f'{name}.yaml')
        with open(os.path.join(file_path, file_name)) as fid:
            _presets[name] = yaml.load(fid, Loader=yaml.SafeLoader)
    del fid, file_name, file_names, name

    _alias = {}
    for name in ['positions', 'motions']:
        file_name = os.path.join('presets', f'alias_{name}.yaml')
        with open(os.path.join(file_path, file_name)) as fid:
            _alias[name] = yaml.load(fid, Loader=yaml.SafeLoader)
    del fid, file_name, file_path

    def __init__(self):
        self.topology = self._presets['topology']
        self.positions = self._presets['positions']
        self.motions = self._presets['motions']
        self.nodes = self._presets['nodes']

    @staticmethod
    def expand_alias(alias):
        """Expands the string alias to 2 strings

        It is just a way to make the class/preset easier to specify.
        """
        if '@' in alias:  # shorthand in the form preset@class
            alias = alias.split('@')
            class_ = alias[1]
            preset_ = alias[0]
        else:  # shorthand in the form class_preset
            alias = alias.split('_')
            class_ = alias[0]
            preset_ = '_'.join(alias[1:])

        return class_.capitalize(), preset_

    def get_elements(self, cfg_type, cfg):
        """Get the class, preset, and transform elements
        
        cfg_type: 'positions', 'motions'
        cfg: list of 'configurations', a row in the topology.yaml
        """
        if isinstance(cfg, str):
            cfg_ = self._alias[cfg_type].get(cfg)
            if cfg_ is None:  # it is not in the alias_*.yaml file
                # which means it is the shorthand in the form class_preset
                class_, preset_ = self.expand_alias(cfg)
                transforms_ = None
            else:  # it is in the alias_*.yaml file
                # which means it is the shorthand in the form preset@class
                class_ = cfg_['class'].capitalize()
                preset_ = cfg_['preset']
                transforms_ = cfg_.get('transformations')
        elif isinstance(cfg, dict):
            class_ = cfg['class'].capitalize()
            preset_ = cfg['preset']
            transforms_ = cfg.get('transformations')

        return class_, preset_, transforms_

presets = Presets()
