from qtpy.QtGui import QStandardItemModel, QStandardItem
from qtpy.QtCore import Qt

from app.presets import presets

TYPE_ROLE = Qt.UserRole


class ProjectModel(QStandardItemModel):
    """Project model

    It should build a model from the yaml files using the Presets class as intermediate

    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load()
        self.setColumnCount(2)

    def load(self):
        """Walk the tree starting from topology"""
        for el, val in presets.topology.items():
            item = QStandardItem(el)
            self.appendRow(item)
            nodes = QStandardItem('nodes')
            item.appendRow(nodes)
            # Walk the nodes
            for node_name, nvals in val['nodes'].items():
                n = QStandardItem(node_name)
                nodes.appendRow(n)
                for nval in nvals:
                    node_layout = QStandardItem('')
                    n.appendRow(node_layout)
                    p = nval.get('position')
                    if isinstance(p, dict):
                        p = 'dict..'
                    pos = QStandardItem(p)
                    pos.setData('position', TYPE_ROLE)
                    node_layout.appendRow([QStandardItem('position'), pos])

                    m = nval.get('motion')
                    if isinstance(m, dict):
                        m = 'dict..'
                    mot = QStandardItem(m)
                    mot.setData('motion', TYPE_ROLE)
                    node_layout.appendRow([QStandardItem('motion'), mot])

                    mdl = QStandardItem(nval.get('model'))
                    node_layout.appendRow([QStandardItem('model'), mdl])
            
            connections = QStandardItem('connections')
            item.appendRow(connections)
            # Walk the connections
            for conn in val['connections']:
                c = QStandardItem('')
                connections.appendRow(c)
                src = QStandardItem('Source:')
                src_val = QStandardItem(conn['source'])
                src_val.setData('combo', TYPE_ROLE)
                c.appendRow([src, src_val])

                snk = QStandardItem('Sink:')
                snk_val = QStandardItem(conn['sink'])
                snk_val.setData('combo', TYPE_ROLE)
                c.appendRow([snk, snk_val])

                mdl = QStandardItem('Model:')
                mdl_val = QStandardItem(conn['model'])
                c.appendRow([mdl, mdl_val])

    