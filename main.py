# Author: Malek Cellier
# Email: malek.cellier@gmail.com
# Created: 2019-07-03

from app.topology import Topology

# Illustration of the Topology class

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
