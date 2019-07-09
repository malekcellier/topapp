from qtpy.QtWidgets import QStyledItemDelegate, QComboBox, QSpinBox, QSlider, QFrame, QHBoxLayout
from qtpy.QtCore import Qt

from .project_model import ProjectModel
from .properties_model import PropertiesTreeModel
from .gui_presets import presets


class TreeDelegate(QStyledItemDelegate):
    """

    Customizing the way the tree represents its elements,
    for each column
    """
    def createEditor(self, parent, option, index):
        if index.isValid():
            role = index.data(ProjectModel.TYPE_ROLE)
            if role == 'combo':
                node_types = list(presets.nodes.keys())
                cbox = QComboBox(parent)
                current_item = index.data(Qt.DisplayRole)
                for idx, node_type in enumerate(node_types):
                    cbox.addItem(node_type)
                    if node_type == current_item:
                        cbox.setCurrentIndex(idx)
                def text_changed(txt):
                    """
                    go up the tree to get which topo preset it is
                    model.index.sibling
                    """
                    presets.topo_changed.emit() # pass which topo has changed
                    # then update the viz
                cbox.currentTextChanged.connect(text_changed)
                return cbox
        return super().createEditor(parent, option, index)


class PropertiesTreeDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        if index.isValid():
            role = index.data(PropertiesTreeModel.TYPE_ROLE)
            if role == 'class_combo':
                node_types = list(presets.nodes.keys())
                cbox = QComboBox(parent)
                current_item = index.data(Qt.DisplayRole)
                for idx, node_type in enumerate(node_types):
                    cbox.addItem(node_type)
                    if node_type == current_item:
                        cbox.setCurrentIndex(idx)
                return cbox
            elif role == 'preset_combo':
                pass
            elif role == 'spin_scale':
                spin = QSpinBox(parent)
                spin.setValue(index.data(PropertiesTreeModel.DATA_ROLE))
                spin.setMinimum(1)
                spin.setMaximum(100)

                def update_scale(newValue):
                    positions = index.parent().data(PropertiesTreeModel.MODEL_ROLE)
                    oldValue = positions.absolute_scale
                    positions.scale(newValue / oldValue)

                spin.valueChanged.connect(update_scale)

                return spin
            elif role == 'spin_x':
                spin = QSpinBox(parent)
                spin.setValue(index.data(PropertiesTreeModel.DATA_ROLE))

                def update_x(newValue):
                    positions = index.parent().parent().data(PropertiesTreeModel.MODEL_ROLE)
                    print(f"update x, positions:{positions}, translation:{positions.translation}")
                    oldValue = positions.translation["x"]
                    positions.translate(newValue - oldValue, 0)

                spin.valueChanged.connect(update_x)

                return spin
            elif role == 'spin_y':
                spin = QSpinBox(parent)
                spin.setValue(index.data(PropertiesTreeModel.DATA_ROLE))

                def update_y(newValue):
                    positions = index.parent().parent().data(PropertiesTreeModel.MODEL_ROLE)
                    oldValue = positions.translation["y"]
                    positions.translate(0, newValue - oldValue)

                spin.valueChanged.connect(update_y)

                return spin
            elif role == 'rotate_slider':
                slider = QSlider(parent)
                slider.setOrientation(Qt.Horizontal)
                slider.setMinimum(0)
                slider.setMaximum(359)
                slider.setValue(index.data(PropertiesTreeModel.DATA_ROLE))
                slider.setAutoFillBackground(True)
                def update_rotation(newValue):
                    positions = index.parent().data(PropertiesTreeModel.MODEL_ROLE)
                    oldValue = positions.angle
                    print(f"rotate by: {newValue - oldValue}")
                    print(f"X before: {positions.x}")
                    positions.rotate(newValue - oldValue)
                    print(f"X after: {positions.x}")

                slider.valueChanged.connect(update_rotation)
                return slider

        return super().createEditor(parent, option, index)
