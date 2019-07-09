from qtpy.QtGui import QStandardItemModel, QStandardItem
from qtpy.QtCore import Qt

from app.presets import presets


class PropertiesModel(QStandardItemModel):
    """Properties model


    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(2)

    def load(self, type_, data):
        if type_ == 'position':
            pass
        elif type_ == 'motion':
            pass