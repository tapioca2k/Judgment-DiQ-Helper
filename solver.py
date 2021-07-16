import json
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

class Node:
    def __init__(self, id, stype, connections):
        self.id = id
        self.stype = stype
        self.connections = connections

    def map_descriptor(self, i):
        if i >= 17:
            return 'Right fork'
        elif i >= 14:
            return 'Ending bit'
        elif i >= 7:
            return 'Left fork'
        else:
            return 'Starting line'

    def __repr__(self):
        return '%s (#%s, %s)' % (self.stype, self.id, self.map_descriptor(self.id))

with open('judgment.json', 'r') as file:
    j = json.loads(file.read())

nodes = [Node(n['id'], n['type'], n['connections']) for n in j['nodes']]


weights = {
'end': 0,
'dice -2': 0.5,
'start': 1,
'visited': 1,
'gift': 2,
'safe': 3,
'fight': 4,
'dice +2': 5
}


            

'''
space = 0
while True:
    roll = int(input('Roll: '))
    paths = traverse(space, roll)
    r_nodes = [nodes[p] for p in paths]
    sort = sorted(r_nodes, key=lambda x: weights[x.stype])
    print('Go to %s' % (sort[0],))
    sort[0].stype = 'visited'
    space = sort[0].id
'''


class MainWindow(QDialog):
    def __init__(self, nodes, parent=None):
        super(MainWindow, self).__init__(parent)

        self.nodes = nodes

        self.space = 0

        self.setWindowTitle('Judgment solver')
        
        self.vlayout = QVBoxLayout()
        self.setLayout(self.vlayout)

        self.topParent = QWidget()
        self.top = QHBoxLayout()

        self.rollbox = QLineEdit('Roll goes here')
        self.top.addWidget(self.rollbox, 3)
        self.rollbutton = QPushButton('Search')
        self.rollbutton.clicked.connect(self.search)
        self.top.addWidget(self.rollbutton, 1)

        self.bottomParent = QWidget()
        self.bottom = QHBoxLayout()
        self.result = QLabel('Result goes here...')
        self.bottom.addWidget(self.result)
        
        self.topParent.setLayout(self.top)
        self.vlayout.addWidget(self.topParent)
        self.bottomParent.setLayout(self.bottom)
        self.vlayout.addWidget(self.bottomParent)

    def traverse(self, start, moves):
        stack = [(start, 0, -1)]
        distance = {i: set() for i in range(moves+1)}
        for c in self.nodes[start].connections:
            distance[0].add((start, int(c)))
        while stack:
            node, dist, prev = stack.pop()
            failure = False
            for i in range(dist):
                for p in distance[i]:
                    if p[0] == node:
                        failure = True
            if failure: continue
            distance[dist].add((node, prev))
            if dist < moves:
                stack.extend((int(x), dist+1, node) for x in self.nodes[node].connections if x != prev)
        return {node for (node, prev) in distance[moves]}

    def search(self):
        roll = int(self.rollbox.text())
        paths = self.traverse(self.space, roll)
        r_nodes = [nodes[p] for p in paths]
        sort = sorted(r_nodes, key=lambda x: weights[x.stype])
        self.result.setText('Go to %s' % (sort[0],))
        self.rollbox.setText('')
        self.space = sort[0].id

if __name__=='__main__':
    sys.excepthook = except_hook
    app = QApplication([])
    window = MainWindow(nodes)
    window.show()
    sys.exit(app.exec_())





