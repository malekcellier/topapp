from app.topology import Topology
from qtpy.QtCore import QObject, Property, QAbstractItemModel


class GuiPositions(QObject):
    def __init__(self, position, parent=None):
        super().__init__(parent)
        self.position = position
        self._x = [float(n) for n in self.position.x]
        self._y = [float(n) for n in self.position.y]

    @Property('QVariant')
    def x(self):
        return self._x

    @Property('QVariant')
    def y(self):
        return self._y


class GuiNodes(QObject):
    def __init__(self, nodes, parent=None):
        super().__init__(parent)
        self.nodes = nodes
        self._positions = [GuiPositions(positions) for positions in self.nodes.positions]

    @Property('QVariant')
    def positions(self):
        return self._positions


class GuiTopology(QObject):
    """
    Expose Topology attributes to QML
    """
    def __init__(self, preset, parent=None):
        super().__init__(parent)
        self.topology = Topology(preset)
        self._nodes = [GuiNodes(nodes) for nodes in self.topology.nodes.values()] 

    @Property(str)
    def presetName(self):
        return self.topology.preset_name

    @Property('QVariant')
    def nodes(self):
        return self._nodes

