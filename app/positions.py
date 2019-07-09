# Author: Malek Cellier
# Email: malek.cellier@gmail.com
# Created: 2019-07-03

from abc import ABC, abstractmethod
import numpy as np
import matplotlib.pyplot as plt

from app.presets import presets

class Positions(ABC):
    """
    Abstract Base Class that represent points position in 2D-space.

    Args:
        preset (str): name of the preset for the subclass (coming from yaml file)

    Attributes:
        name (str): name of the class
        preset (str): name of the preset
        presets (dict): input configuration (coming from yaml file)
        x (ndarray): x coordinates
        y (ndarray): y coordinates
        _x0 (ndarray): initial x coordinates
        _y0 (ndarray): initial y coordinates
        delta (dict): adjustement on top of the coordinates. This has both x and y element as ndarray.

    """

    def __init__(self, preset):
        self.name = self.__class__.__name__.lower()
        preset_ = presets.positions[self.name].get(preset)
        assert preset_ is not None, f'passed preset {preset} does not exist'
        self.preset_name = preset
        self.preset = preset_
        x, y = self._generate()
        assert x.size == y.size, f'vector x={x.size} & y={y.size} should be equal'

        # X/Y positions list
        self.x = x
        self.y = y

        # absolute rotation, translation and scale from functions
        self.angle = 0
        self.translation = {"x": 0, "y": 0}
        self.absolute_scale = 1

        self._x0 = x.copy()
        self._y0 = y.copy()
        self.delta = {'x': np.zeros(self.x.shape), 'y': np.zeros(self.y.shape)}

    @property
    def n_el(self):
        """Number of elements"""
        return self.x.size

    @property
    def total_x(self):
        """total_x is the original x plus the delta"""
        return self.x + self.delta['x']

    @property
    def total_y(self):
        """total_y is the original y plus the delta"""
        return self.y + self.delta['y']

    @abstractmethod
    def _generate(self):
        """Generate the position based on the custom values from the yaml file.

        Args:

        Returns:
            (ndarray, ndarray): x and y numpy array representing the coordinates
        """

    def move(self, vector_x, vector_y):
        """Move the points with the passed vectors
        """
        assert vector_x.size == self.x.size, 'passed vector_x has different size'
        assert vector_y.size == self.y.size, 'passed vector_y has different size'
        self.translate(vector_x, vector_y)

    def scale(self, scaling_factor=1):
        """Scale the positions by the scaling factor"""
        self.x *= scaling_factor
        self.y *= scaling_factor
        self.absolute_scale *= scaling_factor

    def translate(self, delta_x=0, delta_y=0):
        """Translate the points with delta_x in x and delta_y in y"""
        self.x += delta_x
        self.y += delta_y
        self.translation["x"] += delta_x
        self.translation["y"] += delta_y

    @staticmethod
    def _rot_mat(angle_deg):
        """Return a 3D rotation matrix with the selected angle"""
        theta = np.radians(angle_deg)
        c, s = np.cos(theta), np.sin(theta)
        return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])

    def rotate(self, angle_deg=0):
        """Rotate all the points around the origin with angle angle_deg"""
        pos = np.array([self.x, self.y, np.zeros(self.x.shape)])

        rot_mat = self._rot_mat(angle_deg)
        pos = rot_mat.dot(pos)

        self.x = pos[0, :]
        self.y = pos[1, :]
        self.angle = (self.angle + angle_deg) % 360

    def apply_transformations(self, tdict):
        """Apply the transformations included in the passed dictionary"""
        if not isinstance(tdict, dict):
            return

        for transformation, args in tdict.items():
            if transformation == 'rotate':
                self.rotate(args)

            elif transformation == 'scale':
                if args:
                    self.scale(args)

            elif transformation == 'translate':
                if isinstance(args, dict):
                    delta_x, delta_y = 0, 0
                    if args.get('delta_x') is not None:
                        delta_x = args.get('delta_x')
                    if args.get('delta_y') is not None:
                        delta_y = args.get('delta_y')
                elif isinstance(args, (float, int)):
                    delta_x, delta_y = args, args

                self.translate(delta_x, delta_y)

            print(f'Applied transformation: {transformation} with args: {args}')

    def show(self, num=None, misc=None, use_total=False):
        """Plots the points"""
        if num is None:  # in case called directly
            plt.figure('Positions')

        if use_total:
            x = self.total_x
            y = self.total_y
        else:
            x = self.x
            y = self.y

        if misc is not None:
            clr = misc['clr']
            mkr = misc['mkr']
            lbl = misc['lbl']
        else:
            clr = 'b'
            mkr = 'o'
            lbl = 'points'

        plt.plot(x, y, color=clr, marker=mkr, markersize=6,
                 fillstyle='full', linestyle='', label=lbl, alpha=0.5)

        if num is None:
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title(f'Positions for preset {self.preset_name} of Class {self.name.capitalize()}')
            plt.grid(True)
            plt.show(block=False)


class Custom(Positions):
    """
    Positions specified in a custom fashion.
    """
    def _generate(self):
        x = self.preset['x']
        y = self.preset['y']

        return np.array(x), np.array(y)


class Grid(Positions):
    """
    Positions specified in a grid.
    """
    def _generate(self):
        x = self.preset['x']
        y = self.preset['y']
        X, Y = np.meshgrid(np.arange(x['min'], x['max'] + x['step'], x['step']),
                           np.arange(y['min'], y['max'] + y['step'], y['step']))
        x = np.array(X.flatten())
        y = np.array(Y.flatten())

        return x, y


class Circle(Positions):
    """
    Positions specified on a Circle.
    """
    def _generate(self):
        center = self.preset['center']
        radius = self.preset['radius']
        n = self.preset['n']
        delta_angle = 2*np.pi/n
        angles = np.arange(0, 2*np.pi, delta_angle)
        positions = radius*np.array([np.cos(angles), np.sin(angles)])

        return positions[0, :] + center['x'], positions[1, :] + center['y']


if __name__ == "__main__":
    c_1 = Custom('c_1')
    c_1.show()
