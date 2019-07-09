# Author: Malek Cellier
# Email: malek.cellier@gmail.com
# Created: 2019-07-03

import matplotlib.pyplot as plt

import app.positions as positions
import app.motions as motions
from app.presets import presets


class Nodes:
    """
    Handles Nodes for the topology.

    Args:
        node_type (str): name of the node type. Example: type_a, type_b, etc..
        layouts (list): list of dict that contain the position, motion, and model fields required to define Nodes.

    Attributes:
        type (str): name of the node type.
        _layouts (list): list of dicts
        positions (list): list of Positions objects
        motions (list): list of Motions objects
        models (list): list of Model objects
    """

    def __init__(self, node_type, layouts):
        self.type = node_type
        self._layouts = layouts
        self.positions = []
        self.motions = []
        self.models = []
        self._build()

    def _build(self):
        """Build the Nodes from the preset"""
        for layout in self._layouts:
            print(f'Layout: {layout}')
            #class_, preset_, transforms_ = self.get_elements('positions', layout['position'])
            class_, preset_, transforms_ = presets.get_elements('positions', layout['position'])

            # Instantiate the Position object
            po = getattr(positions, class_)(preset_)
            po.apply_transformations(transforms_)
            self.positions.append(po)

            # Handling the motions.
            n_points = po.x.size
            # Not all nodes have motion
            if layout.get('motion') is not None:
                #class_, preset_, transforms_ = self.get_elements('motions', layout['motion'])
                class_, preset_, transforms_ = presets.get_elements('motions', layout['motion'])

                # Create the object and save it
                mo = getattr(motions, class_)(preset_, n_points)
            else:
                mo = None
            self.motions.append(mo)

            # Handling the node model
            models = [layout['model'] for _ in range(n_points)]
            self.models.append(models)

    @property
    def n_el(self):
        """Number of elements"""
        n_el = 0
        for pos in self.positions:
            n_el += pos.n_el

        return n_el

    def show(self, num=None, misc=None):
        """Show the topology for that Nodes object"""
        if num is None:
            plt.figure(num='Nodes')

        for pos, mot in zip(self.positions, self.motions):
            pos.show(num, misc)
            if mot is not None:
                mot.show(num, pos)

        if num is None:
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title('Nodes')
            plt.grid(True)
            plt.show(block=False)
