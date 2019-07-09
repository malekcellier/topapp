# Author: Malek Cellier
# Email: malek.cellier@gmail.com
# Created: 2019-06-24

# 2019-07-09 NOTE not needed!

import os
import yaml


def yaml_to_item():
    """Create the Item tree from a series of YAML files

    The toplevel is passed
    - how to know where to find the subcategory?
        => maybe with some sort of validation?
        => maybe by explicitly creating categories?
            works with positions which will then refer to the positions.yaml and use the class/preset
    """
    presets = {}
    with open(os.path.join(os.path.dirname(__file__), '../presets/motions.yaml')) as fid:
        presets['motions'] = yaml.load(fid, Loader=yaml.SafeLoader)
    with open(os.path.join(os.path.dirname(__file__), '../presets/positions.yaml')) as fid:
        presets['positions'] = yaml.load(fid, Loader=yaml.SafeLoader)

    item_tree = Item()

    for key, value in presets['drawing'].items():
        child = Item(name=key, parent=item_tree)
        item_tree.add_child(child)
        for values in value['shapes']:
            grand_child = Item(name=f"{values['class']}: {values['preset']}", parent=child)
            child.add_child(grand_child)
            # take hold of the last level
            data = presets['shape'][values['class']][values['preset']]
            for sk, sv in data.items():
                gg_child = Item(name=f'{sk}: {sv}', parent=grand_child)
                grand_child.add_child(gg_child)

    # 2019-06-24
    # to create the list, maybe a strategy would be to have a map of what is possible
    # or to have specific functions for each category i.e. less generic approach
    # maybe there could be a more generic approach further down the line with the next refactoring?
    # doing it this way could help also for the properties editor which indeed needs the list of properties
    # TODO 
    # - identify what constitutes the definition of each block
    #   ex: a circle shape is a center + radius 
    #   ex: a square shape is a center + side
    #   ex: a drawing is a set of shapes...but does that definition help?
    # it could look like:
    #   - process_node
    #       - which will call process_layout
    # which means that the yaml_to_item should actually be a class with different subclass
    # class NetworkItem
    #   class NodesItem
    #       class LayoutItem
    #           class PositionItem
    #           class MotionItem

    return item_tree


class Item:
    """A Item model for the project tree
    Item elements are validated"""
    def __init__(self, name='root', parent=None):
        self._name = name
        self._parent = parent
        self._children = []
        self._role = None

    @property
    def name(self):
        """Get name"""
        return self._name

    @name.setter
    def name(self, name):
        """Set name"""
        self._name = name

    @property
    def parent(self):
        """Get parent"""
        return self._parent

    @parent.setter
    def parent(self, parent):
        """Set parent"""
        self._parent = parent

    @property
    def children(self):
        """Get children"""
        return self._children

    def child_count(self):
        """How many children does this Item have?"""
        return len(self._children)

    def add_child(self, child):
        """Add child to a Item"""
        if not isinstance(child, Item):
            print('Passed child not a Item instance')
            return
        self._children.append(child)

    def insert_child(self, position, child):
        """Insert child in specific position"""
        if not isinstance(child, Item):
            print('Passed child not a Item instance')
            return False
        if position < 0 or position > self.child_count():
            return False
        self._children.insert(position, child)
        child.parent = self
        # TODO child._role =

        return True

    def child(self, row):
        """Return child in specific row"""
        if not isinstance(row, int):
            print('argument must be an int')
            return None
        if row < 0 or row > self.child_count():
            print('argument outside of range')
            return None
        return self._children[row]

    def row(self):
        """Return position of Item among siblings"""
        if self.parent is not None:
            return self.parent.children.index(self)

    def show(self, tab_level=-1):
        """Display the Item tree in the console"""
        output = ''
        tab_level += 1

        for i in range(tab_level):
            output += "   "
        output += "|--" + self._name + '\n'

        for child in self._children:
            output += child.show(tab_level)

        tab_level -= 1

        #output += '\n'

        return output

    def __repr__(self):
        return self.show()
