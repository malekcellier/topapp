# Author: Malek Cellier
# Email: malek.cellier@gmail.com
# Created: 2019-07-03

import sys
from qtpy.QtWidgets import QApplication

from app.topology import Topology
from gui.gui import TopologyGui, pwdi, QIcon

# Illustration of the Topology class
"""
t1 = Topology('topo_1')
# Showing the topology
t1.show()
# Showing the value of the connections
for conn in t1.connections.values():
    conn.show()


t3 = Topology('topo_3')
t3.show()
for conn in t3.connections.values():
    conn.show()
"""


app = QApplication(sys.argv)
app.setApplicationName('TopologyApp')
app.setOrganizationName('M.C.')
app.setWindowIcon(QIcon(pwdi('noun_Baby Penguin_57276.png')))
win = TopologyGui()
win.show()
sys.exit(app.exec_())
