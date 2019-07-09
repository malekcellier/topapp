# Author: Malek Cellier
# Email: malek.cellier@gmail.com
# Created: 2019-06-19


import os
import sys
from qtpy.QtWidgets import (QApplication, QMainWindow, QDockWidget, QTabWidget, QWidget,
                               QGraphicsView, QGraphicsScene, QGraphicsItem, QAction, QTreeView, QTableView,
                               QGraphicsEllipseItem, QGraphicsPolygonItem, QGraphicsRectItem,
                               QMessageBox, QHBoxLayout, QVBoxLayout, QSizePolicy)
from qtpy.QtQuickWidgets import (QQuickWidget)
from qtpy.QtGui import (QIcon)
from qtpy.QtCore import (Qt, QUrl, QSizeF)
#from qtpy.QtDataVisualization import (QtDataVisualization)
#from qtpy.Qt3DRender import (Qt3DRender)
#from qtpy.Qt3DExtras import (Qt3DExtras)

from .project_model import ProjectModel, TYPE_ROLE
from .properties_model import PropertiesTreeModel
from .project_delegate import TreeDelegate, PropertiesTreeDelegate

from .gui_topology import GuiTopology


def pwdi(icon_name):
    """Returns the path to the requested icon"""
    file_path = os.path.dirname(__file__)
    file_name = os.path.join('icons', icon_name)
    icon_path = os.path.join(file_path, file_name)

    return icon_path


class DataViz(QQuickWidget):
    """Using QtDataVisualization
    
    Placeholder for the OpenGL based data visualization tool which should allow the following:
        - display 100s of 1000s of points as line graphs
        - display 100s of 1000s of points as matshow
        - allow for time scrolling from saved data
        - should open in a tab
    """
    def __init__(self, parent):
        super().__init__(parent)
        main = "gui/qml/QmlDataViz.qml"
        self.setSource(QUrl.fromLocalFile(main))
        self.resizeMode = QQuickWidget.SizeRootObjectToView
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    # workaround: have QML view same size as parent widget
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.rootObject().setWidth(self.width())
        self.rootObject().setHeight(self.height())

class SceneViz(QQuickWidget):  # or from Qt3DExtras.Qt3DWindow):
    """Using 3D library

    Placeholder for the OpenGL based input visualization which should allow the following:
        - display scenes with 100s of shapes (basic shapes as cubes)
        - allow to drag the objects and signal the coordinates changes to the underlying object
        - allow to click and look at the properties and change them (both structural and formatting related)
        - allow to drop shapes on the scene
        - should open in a tab each time a topology configuration is chosen
    """
    def __init__(self, parent=None, live=False, topologyName=""):
        super().__init__(parent)
        if live:
            from livecoding import register_types
            from livecoding.gui import MODULE_PATH

            self.engine().addImportPath(os.path.join(MODULE_PATH, '..'))
            register_types()
            main = "gui/qml/live.qml"
            self.rootContext().setContextProperty(
                "userProjectPath", QUrl.fromLocalFile(os.path.realpath(os.path.join(os.path.dirname(__file__), 'qml'))) 
            )
        else:
            main = "gui/qml/QmlSceneViz.qml"
            self.rootContext().setContextProperty("topologyModel", [])
            self.rootContext().setContextProperty("highlightNodeType", "")
        self.setSource(QUrl.fromLocalFile(main))
        self.resizeMode = QQuickWidget.SizeRootObjectToView
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.topology = GuiTopology(topologyName)
        self.rootContext().setContextProperty("topologyModel", self.topology)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.rootObject().setWidth(self.width())
        self.rootObject().setHeight(self.height())

    def highlightNodeType(self, nodeType):
        print("highlight", nodeType)
        self.rootContext().setContextProperty("highlightNodeType", nodeType)

class TopologyGui(QMainWindow):
    """The entire application

    # NOTE: is it good practice to keep a reference to all the functions that will serve as slots?
        all the functions from the underlying model are included in the object
    """
    def __init__(self):
        super().__init__()
        # Place-holders for the attributes
        self.menubar = None
        self.toolbar = None
        self.statusbar = None
        self.docks = None
        self._menus = {}  # holds references to menu items
        self._actions = {}  # holds references to action items
        self._docks = {}  # holds ref to docks for visibility toggling
        self._widgets = {}  # holds references to the widgets
        self._slots = {}
        self._models = {}
        self.backends = {}
        self.load_back_end()
        self._build()

    def load_back_end(self):
        """Load the data from the backend a.k.a the Topology class

        Is it the way to do it?
        """

    def _build(self):
        """Build the gui - wrapper for convenience and clarity"""
        self._build_window()
        self._build_actions()
        self._build_menubar()
        self._build_toolbar()
        self._build_statusbar()
        self._build_docks()

    def _build_window(self):
        """The main window"""
        self.setWindowTitle('Qt experiments')
        self.setWindowIcon(QIcon('icons/light-bulb.png'))
        self.setGeometry(1920+100, 100, 1200, 800)

        self._build_tab_widget()

        self.setCentralWidget(self._widgets['tabs'])

    def _build_tab_widget(self):
        """The tab widget should allow:
            - one tab per scenario to render (good idea)
            - adding tabs
                - other scenarios
            - removing tabs (closing)
        """
        widget_tabs = QTabWidget(self)
        self._widgets['tabs'] = widget_tabs

        # NOTE: the following is just for illustration purposes
        # The actual fonctionality should dynamically create those components
        # depending on the selection on the tree-widget

        # Data is a set of plots of the toutput data
        widget_dataviz = DataViz(widget_tabs)
        widget_tabs.addTab(widget_dataviz, 'Dataviz')
        self._widgets['dataviz'] = widget_dataviz

    def _create_action(self, text, slot=None, shortcut=None, icon=None, tip=None, checkable=False, checked=False):
        """Convenience function to create actions"""
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            action.triggered.connect(slot)
        if checkable:
            action.setCheckable(True)
            if checked:
                action.setChecked(True)
        return action

    def _build_actions(self):
        """Build the data structure that will hold the Qt actions object
        
        The idea is to save the action with the menu path as a chain of strings with underscores separating each level
        """
        self._actions['file'] = {}
        self._actions['file']['open'] = self._create_action('Open', icon=pwdi('kde-document-open.svg'), shortcut='Ctrl+O', tip='Open yaml')
        self._actions['file']['save'] = self._create_action('Save', icon=pwdi('kde-document-save.svg'), shortcut='Ctrl+S', tip='Save to yaml')
        self._actions['file']['quit'] = self._create_action('Quit', icon=pwdi('kde-application-exit.svg'), shortcut='Ctrl+Q', tip='Exit the application', slot=self.close)
        
        # The new menu should depend on what level of the tree hierarchy is selected. Grey what is not relevant
        self._actions['new'] = {}
        self._actions['new']['topology'] = self._create_action('Topology...', icon=pwdi('kde-document-new.svg'), shortcut='Ctrl+N', tip='Create new Topology')
        self._actions['new']['position'] = self._create_action('New position', icon=pwdi('button_xy.svg'), tip='New position')
        self._actions['new']['motion'] = self._create_action('New motion', icon=pwdi('button_line.svg'), tip='New ellipse')
        self._actions['new']['model'] = self._create_action('New model', icon=pwdi('kde-edit.svg'), tip='New model')
        
        self._actions['view'] = {}
        self._actions['view']['zoom'] = self._create_action('Zoom', tip='Zoom')
        
        self._actions['windows'] = {}
        self._actions['windows']['project tree'] = self._create_action('Project tree window',
                                                                       tip='Toggle project tree window',
                                                                       checkable=True, checked=True,
                                                                       slot=self._toggle_visibility('project tree'))
        self._actions['windows']['properties'] = self._create_action('Properties window', tip='Toggle properties window',
                                                                     checkable=True, checked=True,
                                                                     slot=self._toggle_visibility('properties'))
        self._actions['windows']['formatting'] = self._create_action('Formatting window', tip='Toggle formatting window',
                                                                     checkable=True, checked=True,
                                                                     slot=self._toggle_visibility('formatting'))
        self._actions['windows']['data'] = self._create_action('Data window', tip='Toggle data window',
                                                               checkable=True, checked=True,
                                                               slot=self._toggle_visibility('data'))
        self._actions['windows']['assets'] = self._create_action('Assets window', tip='Toggle assets window',
                                                                 checkable=True, checked=True,
                                                                 slot=self._toggle_visibility('assets'))
        self._actions['windows']['toolbar'] = self._create_action('Toolbars', tip='Toggle toolbars',
                                                                  checkable=True, checked=True,
                                                                  slot=self._toggle_visibility('toolbar'))
        self._actions['help'] = {}
        self._actions['help']['doc'] = self._create_action('Documentation')
        self._actions['help']['manual'] = self._create_action('Manual')
        self._actions['help']['about'] = self._create_action('About', icon=pwdi('light-bulb.png'), shortcut="Ctrl+B", slot=self.about, tip='About')

    def _toggle_visibility(self, a_string):
        """For the docks and toolbars only"""
        def closure():
            self._docks[a_string].setVisible(not self._docks[a_string].isVisible())
        return closure

    def _build_menubar(self):
        self.menubar = self.menuBar()
        # Create menu items
        self._menus['file'] = self.menubar.addMenu('&File')
        self._menus['new'] = self.menubar.addMenu('&New')
        self._menus['edit'] = self.menubar.addMenu('&Edit')
        self._menus['view'] = self.menubar.addMenu('&View')
        self._menus['windows'] = self._menus['view'].addMenu('&Windows')
        self._menus['tools'] = self.menubar.addMenu('&Tools')
        self._menus['help'] = self.menubar.addMenu('&Help')
        # Location of separators
        separators_after = [('file', 'save'), ('help', 'manual'), ('new', 'topology')]
        # Add elements to menus
        for menu in self._actions.keys():
            for key, action in self._actions[menu].items():
                if isinstance(action, dict):
                    for sub_action in action.values():
                        self._menus[menu].addAction(sub_action)
                else:
                    self._menus[menu].addAction(action)
                if (menu, key) in separators_after:
                    self._menus[menu].addSeparator()

    def _build_toolbar(self):
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(self._actions['new']['topology'])
        self.toolbar.addAction(self._actions['new']['position'])
        self.toolbar.addAction(self._actions['new']['motion'])
        self.toolbar.addAction(self._actions['new']['model'])
        self.toolbar.addAction(self._actions['file']['quit'])

    def _build_statusbar(self):
        """Builds all statusbar aspects"""
        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Experiments with Qt by M.C.')

    def _build_docks(self):
        """Build dock widgets

        They will host:
            - LEFT dock:
                - the project browser (tree) (aka hierarchy)
                - the properties editor (aka inspector)
                - the formatting editor ()
            - RIGHT dock:
                - the data browser (HDF5 outputs from the runs)
            - BOTTOM dock:
                - the assets browser
                    - positions
                    - motions
                    - models
        """
        self._build_left_dock()
        self._build_right_dock()
        self._build_bottom_dock()

    def treeItemClicked(self, index):
        tempIndex = index
        depth = 0
        while tempIndex.parent().isValid():
            tempIndex = tempIndex.parent()
            depth += 1
        topologyName = tempIndex.data(Qt.DisplayRole)

        data = index.data(Qt.DisplayRole)
        type_ = index.data(TYPE_ROLE)
        print(f'type: {type_}')
        print(data)
        print(f'parent: {index.parent().isValid()}')
        widget_tabs = self._widgets['tabs']
        if depth == 0:
            # clicked in root level -> open topology tab
            # Scene is the representation in 3D of the scene to simulate
            tab_key = 'sceneviz_' + data
            if tab_key not in self._widgets:
                widget_sceneviz = SceneViz(parent=widget_tabs, live=False, topologyName=data)
                self._widgets[tab_key] = widget_sceneviz
                widget_tabs.addTab(widget_sceneviz, 'SceneViz: ' + data)
                self.backends[data] = widget_sceneviz.topology
            widget_tabs.setCurrentWidget(self._widgets[tab_key])
        elif depth == 2:
            # clicked in 2nd level -> highlight selected node type
            widget_sceneviz = widget_tabs.widget(widget_tabs.currentIndex())
            if(isinstance(widget_sceneviz, SceneViz)):
                widget_sceneviz.highlightNodeType(data)
        elif depth == 4:
            nodeType = index.parent().parent().data(Qt.DisplayRole)
            positionIndex = index.parent().row()
            if topologyName in self.backends:
                topology = self.backends[topologyName]
                positions = topology.nodes_dict[nodeType].positions[positionIndex]
                self._models['properties'].load(type_, data, positions)

    def _build_left_dock(self):
        # QTreeView for the project view        
        w_project_tree = QDockWidget("Project tree", self)
        w_project_tree.setFloating(False)
        self._docks['project tree'] = w_project_tree
        self.addDockWidget(Qt.LeftDockWidgetArea, w_project_tree)
        # Add the treeview
        treeview = QTreeView(w_project_tree)
        treedelegate = TreeDelegate()
        treeview.setItemDelegate(treedelegate)
        pm = ProjectModel()
        treeview.setModel(pm)
        treeview.expandAll()
        treeview.resizeColumnToContents(0)
        treeview.resizeColumnToContents(1)
        w_project_tree.setWidget(treeview) 

        treeview.clicked.connect(self.treeItemClicked)

        # Formatting Editor
        w_properties = QDockWidget("Properties editor", self)
        w_properties.setFloating(False)
        self._docks['properties'] = w_properties
        self.addDockWidget(Qt.LeftDockWidgetArea, w_properties)
        # Create Container widget
        container = QWidget(w_properties)
        # Create a verticallayout in which we put a treeview and a tableview
        v_layout = QVBoxLayout(w_properties)
        # Positions Properties to start with
        # the treeview will contain the widgets for the properties of the selected item in the tree
        treeview = QTreeView(w_properties)
        v_layout.addWidget(treeview)
        v_layout.setStretchFactor(treeview, 2)
        treedelegate = PropertiesTreeDelegate()
        treeview.setItemDelegate(treedelegate)
        pm = PropertiesTreeModel()
        self._models['properties'] = pm
        treeview.setModel(pm)
        treeview.expandAll()
        # The tableview will only contain editable x,y shown as rows
        tableview = QTableView(w_properties)
        v_layout.addWidget(tableview)
        v_layout.setStretchFactor(tableview, 1)
        container.setLayout(v_layout)
        w_properties.setWidget(container)

        # Formatting Editor
        w_formatting = QDockWidget("Formatting editor", self)
        w_formatting.setFloating(False)
        self._docks['formatting'] = w_formatting
        self.addDockWidget(Qt.LeftDockWidgetArea, w_formatting)

    def _build_right_dock(self):
        w_data = QDockWidget("Data inspector", self)
        w_data.setFloating(False)
        self._docks['data'] = w_data
        self.addDockWidget(Qt.RightDockWidgetArea, w_data)

    def _build_bottom_dock(self):
        w_assets = QDockWidget("Assets", self)
        w_assets.setFloating(False)
        self._docks['assets'] = w_assets
        self.addDockWidget(Qt.BottomDockWidgetArea, w_assets)

    def about(self):
        """Display some information about the program"""
        text = "<b>Tool GUI v0.1</b><br>" + \
               "Author: Malek Cellier<br><br>" + \
               "The <b>Tool GUI</b> example shows use of the Qt framework.<br>"
        QMessageBox.about(self, "About the Tool Gui", text)

    def populate(self):
        """Populate the GUi with the actual data

        1) set the content of the tree
        2) display the content of the tree into the central widget
        3) make sure the properties/formatting editor work
        """


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('TopologyApp')
    app.setOrganizationName('M.C.')
    app.setWindowIcon(QIcon(pwdi('noun_Baby Penguin_57276.png')))
    win = TopologyGui()
    win.show()
    sys.exit(app.exec_())
