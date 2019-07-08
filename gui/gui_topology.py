from app.topology import Topology
from qtpy.QtCore import QObject, Property, QAbstractItemModel


class GuiPositions(QObject):
    def __init__(self, position, parent=None):
        super().__init__(parent)
        self.position = position

    @Property('QVariant')
    def x(self):
        return self.position.x

    @Property('QVariant')
    def y(self):
        return list(self.position.y)


class GuiNodes(QObject):
    def __init__(self, nodes, parent=None):
        super().__init__(parent)
        self.nodes = nodes

    @Property('QVariant')
    def positions(self):
        return [GuiPositions(positions) for positions in self.nodes.positions]


class GuiTopology(QObject):
    """
    Expose Topology attributes to QML
    """
    def __init__(self, preset, parent=None):
        super().__init__(parent)
        self.topology = Topology(preset)

    @Property(str)
    def presetName(self):
        return self.topology.preset_name

    @Property('QVariant')
    def nodes(self):
        return [GuiNodes(nodes) for nodes in self.topology.nodes.values()]

