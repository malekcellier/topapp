# Author: Malek Cellier
# Email: malek.cellier@gmail.com
# Created: 2019-07-03

import os
import yaml
import matplotlib.pyplot as plt

from app.nodes import Nodes
from app.connections import Connections


class Topology:
    """
    Topology of connected Nodes.

    Nodes are connected category-wise.

    Args:
        preset (str): name of the preset from the topology.yaml file

    Attributes:
        preset (dict): input data to the configuration of the class
        preset_name (str): name of the preset
        nodes (dict): Nodes objects keyed by node_type
        connections (dict): Connections objects keyed by <source>_<sink>
        _misc (dict): misc parameters to configure the plots

    """
    file_path = os.path.dirname(__file__)
    file_name = os.path.join('presets', 'topology.yaml')
    with open(os.path.join(file_path, file_name)) as fid:
        _presets = yaml.load(fid, Loader=yaml.SafeLoader)
        del fid, file_name, file_path

    def __init__(self, preset):
        self.preset = self._presets[preset]
        self.preset_name = preset
        self.nodes = {}
        self.connections = {}
        self._misc = {}
        self._build()

    def _build(self):
        self._build_nodes()
        self._build_connections()
        self._build_misc()

    def _build_nodes(self):
        """The Nodes are defined under the nodes category in the topology.yaml file"""
        for node_type, layouts in self.preset['nodes'].items():
            self.nodes[node_type] = Nodes(node_type, layouts)

    def _build_connections(self):
        """Connections between nodes"""
        for connection in self.preset['connections']:
            src = connection['source']
            snk = connection['sink']
            self.connections[f'{src}_{snk}'] = Connections(src, snk, self.nodes)

    def _build_misc(self):
        """General operations

            get the colors and markers for the node plots
            this is achieved by cycling through them
        """
        n_node_types = len(self.nodes.keys())
        colorset = 'Set1'
        if n_node_types > 9:
            colorset = 'tab20c'
        colors = getattr(plt.cm, colorset).colors
        markers = ['o', 's', 'D', '>', '<', '^', 'v', 'h', 'X', '.']
        misc = {}
        for idx, node_type in enumerate(self.nodes.keys()):
            misc[node_type] = {'clr': colors[idx],
                               'mkr': markers[idx],
                               'lbl': node_type}

        self._misc = misc

    def show(self):
        """Show the topology"""
        fig_name = 'Topology'
        plt.figure(figsize=(10, 8))  # num=fig_name)
        plt.grid(True)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title(f'Topology for {self.preset_name}')
        for node_type, nodes in self.nodes.items():
            nodes.show(num=fig_name, misc=self._misc[node_type])
        plt.legend()
        plt.show(block=False)
