from app.topology import Topology
from qtpy.QtCore import QObject, Signal, Property, QAbstractItemModel


class GuiPositions(QObject):
    def __init__(self, position, parent=None):
        super().__init__(parent)
        self.position = position
        #self._x = [float(n) for n in self.position.x]
        #self._y = [float(n) for n in self.position.y]

    def x(self):
        return [float(n) for n in self.position.x]

    def y(self):
        return [float(n) for n in self.position.y]

    def angle(self):
        return self.position.angle

    def absolute_scale(self):
        return self.position.absolute_scale

    def translation(self):
        return self.position.translation

    def rotate(self, angle_deg):
        self.position.rotate(angle_deg)
        self.angle_changed.emit()
        self.x_changed.emit()
        self.y_changed.emit()

    def translate(self, x, y):
        self.position.translate(x, y)
        self.translation_changed.emit()
        self.x_changed.emit()
        self.y_changed.emit()

    def scale(self, scale_factor):
        self.position.scale(scale_factor)
        self.absolute_scale_changed.emit()
        self.x_changed.emit()
        self.y_changed.emit()

    x_changed = Signal()
    x = Property('QVariant', x, notify=x_changed)
    y_changed = Signal()
    y = Property('QVariant', y, notify=y_changed)
    angle_changed = Signal()
    angle = Property('QVariant', angle, notify=angle_changed)
    absolute_scale_changed = Signal()
    absolute_scale = Property('QVariant', absolute_scale, notify=absolute_scale_changed)
    translation_changed = Signal()
    translation = Property('QVariant', translation, notify=translation_changed)

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
        self._nodes_dict = {key : GuiNodes(key, nodes) for key, nodes in self.topology.nodes.items()}
        self._nodes = list(self._nodes_dict.values())

    def presetName(self):
        return self.topology.preset_name

    def nodes(self):
        return self._nodes

    def nodes_dict(self):
        return self._nodes_dict

    nodes_changed = Signal()
    nodes = Property('QVariant', nodes, notify=nodes_changed)
    nodes_dict_changed = Signal()
    nodes_dict = Property('QVariant', nodes_dict, notify=nodes_dict_changed)
    presetName_changed = Signal()
    presetName = Property(str, presetName, notify=presetName_changed)

