# Author: Malek Cellier
# Email: malek.cellier@gmail.com
# Created: 2019-07-04

import numpy as np
import matplotlib.pyplot as plt


class Connections:
    """
    Connections between Nodes.

    The connection is based on the shortest distance between the chosen types.

    Args:
        source (str): name of the source node
        sink (str): name of the sink node
        nodes (Nodes): reference to the parent Nodes

    Attributes:
        src (Nodes): source nodes object
        _src_name (str): name of the source
        snk (Nodes): sink nodes object
        _snk_name (str): name of the sink
        values (ndarray): matrix of connection value between each source and sink

    """
    def __init__(self, source, sink, nodes):
        self.src = nodes[source]
        self._src_name = source
        self.snk = nodes[sink]
        self._snk_name = sink
        self.values = -1*np.inf*np.ones((self.src.n_el, self.snk.n_el))
        self.kpis = {}
        self.update()

    def update(self):
        """Update the values

        To do that, we need to loop through all the positions object and get their coordinates
        """
        src_n_el = self.src.n_el
        x_src, y_src = np.zeros(src_n_el), np.zeros(src_n_el)
        idx = 0
        for pos in self.src.positions:
            n = pos.n_el
            x_src[idx:idx+n] = pos.x
            y_src[idx:idx+n] = pos.y
            idx += n

        snk_n_el = self.snk.n_el
        x_snk, y_snk = np.zeros(snk_n_el), np.zeros(snk_n_el)
        idx = 0
        for pos in self.snk.positions:
            n = pos.n_el
            x_snk[idx:idx+n] = pos.x
            y_snk[idx:idx+n] = pos.y
            idx += n

        x_snk, x_src = np.meshgrid(x_snk, x_src)
        y_snk, y_src = np.meshgrid(y_snk, y_src)

        self.values = np.sqrt((x_snk-x_src)**2+(y_snk-y_src)**2)

    def compute(self):
        """Compute dumy values for display purposes only"""
        kpi_names = [f'var_{n:02}' for n in range(10)]
        for kpi_name in kpi_names:
            self.kpis[kpi_name] = np.random.rand(1000)

    def show(self):
        """Show the resulting values matrix"""
        fig_name = f'Connections for source {self._src_name} & sink {self._snk_name}'
        fig_size = (12, 8)
        fig, axes = plt.subplots(nrows=1, ncols=1, squeeze=0, figsize=fig_size, num=fig_name)
        axes[(0, 0)].set_xlabel('sink')
        axes[(0, 0)].set_ylabel('source')
        axes[(0, 0)].set_title(fig_name)
        mh = axes[(0, 0)].matshow(self.values, interpolation='nearest',
                                  vmin=self.values.min(), vmax=self.values.max(),
                                  origin='lower', aspect='auto')
        axes[(0, 0)].xaxis.set_ticks_position('bottom')
        plt.colorbar(mh, ax=axes[(0, 0)], label='Value')
        plt.show(block=False)
