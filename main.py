# Author: Malek Cellier
# Email: malek.cellier@gmail.com
# Created: 2019-07-03

import sys
import os

os.environ['QT_API'] = 'pyqt5'
from qtpy.QtWidgets import QApplication
from gui.gui import TopologyGui, pwdi, QIcon


app = QApplication(sys.argv)
app.setApplicationName('TopologyApp')
app.setOrganizationName('M.C.')
app.setWindowIcon(QIcon(pwdi('noun_Baby Penguin_57276.png')))
win = TopologyGui()
win.show()
sys.exit(app.exec_())
