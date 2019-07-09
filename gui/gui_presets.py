from qtpy.QtCore import QObject, Signal, Property

from app.presets import presets as raw_presets


class GuiPresets(QObject):
    def __init__(self, parent=None):
        super(QObject, self).__init__(parent)

    def __getattr__(self, item):
        return getattr(raw_presets, item)
    
    def __setattr__(self, item, value):
        setattr(raw_presets, item, value)

    topo_changed = Signal(str)

    positions_changed = Signal(str)

presets = GuiPresets()
