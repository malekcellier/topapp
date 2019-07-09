from qtpy.QtGui import QStandardItemModel, QStandardItem
from qtpy.QtCore import Qt
from .gui_presets import presets


class ProjectModelRoles:
    TYPE_ROLE = Qt.UserRole
    MODEL_ROLE = TYPE_ROLE + 1

class ProjectModel(QStandardItemModel, ProjectModelRoles):
    """Project model

    It should build a model from the yaml files using the Presets class as intermediate

    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load()
        self.setColumnCount(2)
        presets.topo_changed.connect(self.load)

    def load(self):
        self.clear()
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
                    pos.setData('position', self.TYPE_ROLE)
                    node_layout.appendRow([QStandardItem('position'), pos])

                    m = nval.get('motion')
                    if isinstance(m, dict):
                        m = 'dict..'
                    mot = QStandardItem(m)
                    mot.setData('motion', self.TYPE_ROLE)
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
                src_val.setData('combo', self.TYPE_ROLE)
                c.appendRow([src, src_val])

                snk = QStandardItem('Sink:')
                snk_val = QStandardItem(conn['sink'])
                snk_val.setData('combo', self.TYPE_ROLE)
                c.appendRow([snk, snk_val])

                mdl = QStandardItem('Model:')
                mdl_val = QStandardItem(conn['model'])
                c.appendRow([mdl, mdl_val])

    def load_kpis(self, rootIndex, topology):
        kpis = QStandardItem('kpis')
        item = self.itemFromIndex(rootIndex)
        item.appendRow(kpis)
        for conn_key, conn in topology.connections.items():
            conn_item = QStandardItem(conn_key)
            kpis.appendRow(conn_item)
            for kpi_key, kpi in conn.kpis.items():
                kpi_item = QStandardItem(kpi_key)
                kpi_item.setData('kpi', self.TYPE_ROLE)
                kpi_item.setData(kpi, self.MODEL_ROLE)
                conn_item.appendRow(kpi_item)

