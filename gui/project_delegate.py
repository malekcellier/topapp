from qtpy.QtWidgets import QStyledItemDelegate, QComboBox
from qtpy.QtCore import Qt

from .project_model import TYPE_ROLE
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
