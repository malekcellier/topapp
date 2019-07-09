from app.topology import Topology
from qtpy.QtCore import QObject, Signal, Property, QAbstractItemModel


class GuiPositions(QObject):
    def __init__(self, position, parent=None):
        super().__init__(parent)
        self.position = position
        self._x = [float(n) for n in self.position.x]
        self._y = [float(n) for n in self.position.y]

    def x(self):
        return self._x

    def y(self):
        return self._y

    x_changed = Signal()
    x = Property('QVariant', x, notify=x_changed)
    y_changed = Signal()
    y = Property('QVariant', y, notify=y_changed)

class GuiNodes(QObject):
    def __init__(self, key, nodes, parent=None):
        super().__init__(parent)
        self.nodes = nodes
        self._positions = [GuiPositions(positions) for positions in self.nodes.positions]
        self._node_type = key

    def positions(self):
        return self._positions

    def nodeType(self):
        return self._node_type

    positions_changed = Signal()
    positions = Property('QVariant', positions, notify=positions_changed)
    node_type_changed = Signal()
    nodeType = Property(str, nodeType, notify=node_type_changed)


class GuiTopology(QObject):
    """
    Expose Topology attributes to QML
    """
    def __init__(self, preset, parent=None):
        super().__init__(parent)
        self.topology = Topology(preset)
        self._nodes = [GuiNodes(key, nodes) for key, nodes in self.topology.nodes.items()]

    def presetName(self):
        return self.topology.preset_name

    def nodes(self):
        return self._nodes

    nodes_changed = Signal()
    nodes = Property('QVariant', nodes, notify=nodes_changed)
    presetName_changed = Signal()
    presetName = Property(str, presetName, notify=presetName_changed)

