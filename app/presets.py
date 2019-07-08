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
    del fid, file_name, file_path, file_names, name

    def __init__(self):
        self.topology = self._presets['topology']
        self.positions = self._presets['positions']
        self.motions = self._presets['motions']
        self.nodes = self._presets['nodes']


presets = Presets()
