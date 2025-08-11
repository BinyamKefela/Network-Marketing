class Tree():
    root = None
    leafes = None

    def __init__(self,root,leafes):
        self.root = root
        self.leafes = leafes


class Node():

    def __init__(self,children,parent):
        self.children = children
        self.parent = parent
        
    children = []
    parent
    