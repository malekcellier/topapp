# Author: Malek Cellier
# Email: malek.cellier@gmail.com
# Created: 2019-07-03

from abc import ABC, abstractmethod
import numpy as np
import matplotlib.pyplot as plt

from app.presets import presets


class Motions(ABC):
    """
    Abstract Base Class that represent points motion in space.

    Args:
        preset (str): name of the preset from the motions.yaml file
        n_points (int): number of points to use in order to generate the velocity vectors

    Attributes:
        name (str): name of the class
        preset (str): name of the preset
        presets (dict): input configuration (coming from yaml file)
        vx (ndarray): x component of velocity
        vy (ndarray): y component of velocity
        n_points (int): number of points in the vectors
        delta (dict): adjustement on top of the velocity. It contains vx, vy (ndarray).
    """

    def __init__(self, preset, n_points=100):
        self.name = self.__class__.__name__.lower()
        preset_ = presets.motions[self.name].get(preset)
        assert preset_ is not None, f'passed preset {preset} does not exist'
        self.preset_name = preset
        self.preset = preset_
        self.n_points = n_points
        vx, vy = self._generate()
        self.vx = vx
        self.vy = vy
        self._vx0 = vx.copy()
        self._vy0 = vy.copy()
        self.delta = {'vx': np.zeros(self.vx.shape), 'vy': np.zeros(self.vy.shape)}

    def set_n_points(self, n_points):
        """Set the number of points"""
        self.n_points = n_points
        self._generate()

    @abstractmethod
    def _generate(self):
        """Generate the position based on the custom values from the yaml file.

        Args:

        Returns:
            (ndarray, ndarray): x and y numpy array representing the coordinates
        """

    @abstractmethod
    def update(self):
        """Generate the position based on the custom values from the yaml file.

        Args:

        Returns:
            (ndarray, ndarray): x and y numpy array representing the coordinates
        """

    def show(self, num=None, pos=None):
        """Plots the velocity vectors"""
        if num is None:
            plt.figure('Motions')

        if pos is None:
            # Faking positions
            np.random.seed(0)
            X = (2*np.random.rand(self.n_points)-1)*100
            Y = (2*np.random.rand(self.n_points)-1)*100
            self.set_n_points(X.size)
            plt.plot(X, Y, color='b', marker='o', markersize=6,
                     fillstyle='none', linestyle='', label='Position')
        else:
            X = pos.x
            Y = pos.y

        # print(f'sizes: X={X.size} Y={Y.size} vx={self.vx.size} vy={self.vy.size}')
        plt.quiver(X, Y, self.vx, self.vy, width=0.0035, label='Motion')

        if num is None:
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title(f'Motions for preset {self.preset_name} of Class {self.name.capitalize()}')
            plt.grid(True)
            plt.legend()
            plt.show(block=False)


class Custom(Motions):
    """
    Motions specified in a custom fashion.

    Only this case has the number of points
    """
    def _generate(self):
        speed = self.preset['speed']
        vx = self.preset['vx']
        vy = self.preset['vy']
        assert len(vx) == len(vx), f'sizes of vx and vy must match'
        self.n_points = len(vx)

        return np.array(vx)*speed, np.array(vy)*speed

    def update(self):
        """Nothing to do since the directions are fixed"""


class Random(Motions):
    """
    Motions change randomly
    """
    def _generate(self):
        speed = self.preset['speed']
        angle = self.preset['max_angle_deg']

        angles = np.radians(angle)*np.random.random_sample((self.n_points,))
        vx = speed*np.cos(angles)
        vy = speed*np.sin(angles)

        return vx, vy

    def update(self):
        speed = self.preset['speed']
        angle = self.preset['max_angle_deg']
        turn_probability = self.preset['turn_probability']
        due_for_turn = np.random.rand(self.n_points) <= turn_probability
        angles = np.radians(angle)*np.random.random_sample((self.n_points,))

        self.vx[due_for_turn] = speed*np.cos(angles[due_for_turn])
        self.vy[due_for_turn] = speed*np.sin(angles[due_for_turn])
