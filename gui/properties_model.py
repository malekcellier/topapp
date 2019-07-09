from qtpy.QtGui import QStandardItemModel, QStandardItem
from qtpy.QtCore import Qt
from enum import Enum


class PropertiesModelRoles:
    TYPE_ROLE = Qt.UserRole
    DATA_ROLE = Qt.UserRole + 1
    MODEL_ROLE = Qt.UserRole + 2

from app.presets import presets


class PropertiesModel(QStandardItemModel, PropertiesModelRoles):
    """Properties model


    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(2)

    def load(self, type_, data, positions):
        self.clear()
        if type_ == 'position':
            if data != 'dict..':
                class_, preset_, transforms_ = presets.get_elements('positions', data)
                class_ = class_.lower()
                classes = list(presets.positions.keys())
                # Build the 'class' combobox
                class_item_val = QStandardItem(class_)
                class_item_val.setData('class_combo', self.TYPE_ROLE)
                self.appendRow([QStandardItem('class'), class_item_val])

                # Build the 'preset' combobox
                presets_ = list(presets.positions[class_].keys())
                preset_item_val = QStandardItem(preset_)
                preset_item_val.setData('preset_combo', self.TYPE_ROLE)
                self.appendRow([QStandardItem('preset'), preset_item_val])

                # Build the 'transforms' subtree
                # NOTE: self.tr is a Qt func that helps for the translation to another language
                transforms = QStandardItem(self.tr('Transformations'))
                transforms.setData(positions, self.MODEL_ROLE)
                self.appendRow(transforms)
                # Scale -> spinbox
                scale_item = QStandardItem(str(positions.absolute_scale))
                scale_item.setData('spin_scale', self.TYPE_ROLE)
                scale_item.setData(positions.absolute_scale, self.DATA_ROLE)
                transforms.appendRow([QStandardItem('Scale'), scale_item])
                # Rotate -> slider
                rotate_item = QStandardItem(str(positions.angle))
                rotate_item.setData('rotate_slider', self.TYPE_ROLE)
                rotate_item.setData(positions.angle, self.DATA_ROLE)
                transforms.appendRow([QStandardItem('Rotate'), rotate_item])
                # Translate -> 2 spinboxes
                translate_item = QStandardItem('Translation')
                x_item = QStandardItem(str(positions.translation["x"]))
                x_item.setData('spin_x', self.TYPE_ROLE)
                x_item.setData(positions.translation["x"], self.DATA_ROLE)
                y_item = QStandardItem(str(positions.translation["y"]))
                y_item.setData('spin_y', self.TYPE_ROLE)
                y_item.setData(positions.translation["y"], self.DATA_ROLE)
                translate_item.appendRow([QStandardItem('x:'), x_item])
                translate_item.appendRow([QStandardItem('y:'), y_item])
                transforms.appendRow(translate_item)

        elif type_ == 'motion':
            pass
