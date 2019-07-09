from qtpy.QtWidgets import QStyledItemDelegate, QComboBox, QSpinBox, QSlider, QFrame, QHBoxLayout
from qtpy.QtCore import Qt

from .project_model import TYPE_ROLE
from .properties_model import PropertiesModel
from app.presets import presets


class TreeDelegate(QStyledItemDelegate):
    """

    Customizing the way the tree represents its elements,
    for each column
    """
    def createEditor(self, parent, option, index):
        if index.isValid():
            role = index.data(TYPE_ROLE)
            if role == 'combo':
                node_types = list(presets.nodes.keys())
                cbox = QComboBox(parent)
                current_item = index.data(Qt.DisplayRole)
                for idx, node_type in enumerate(node_types):
                    cbox.addItem(node_type)
                    if node_type == current_item:
                        cbox.setCurrentIndex(idx)
                return cbox
        return super().createEditor(parent, option, index)


class PropertiesTreeDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        if index.isValid():
            role = index.data(PropertiesModel.TYPE_ROLE)
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
            elif role == 'spin':
                spin = QSpinBox(parent)
                spin.setValue(index.data(PropertiesModel.DATA_ROLE))
                return spin
            elif role == 'rotate_slider':
                slider = QSlider(parent)
                slider.setOrientation(Qt.Horizontal)
                slider.setMinimum(0)
                slider.setMaximum(359)
                slider.setValue(index.data(PropertiesModel.DATA_ROLE))
                slider.setAutoFillBackground(True)
                return slider

        return super().createEditor(parent, option, index)
