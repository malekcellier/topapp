from qtpy.QtWidgets import QStyledItemDelegate, QComboBox, QSpinBox, QSlider, QFrame, QHBoxLayout
from qtpy.QtCore import Qt

from .project_model import TYPE_ROLE
from .properties_model import PropertiesTreeModel
from .gui_presets import presets


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
            elif role == 'spin':
                spin = QSpinBox(parent)
                spin.setValue(index.data(PropertiesTreeModel.DATA_ROLE))
                return spin
            elif role == 'rotate_slider':
                slider = QSlider(parent)
                slider.setOrientation(Qt.Horizontal)
                slider.setMinimum(0)
                slider.setMaximum(359)
                slider.setValue(index.data(PropertiesTreeModel.DATA_ROLE))
                slider.setAutoFillBackground(True)
                return slider

        return super().createEditor(parent, option, index)
