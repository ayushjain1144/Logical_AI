from logic import * 

#######################
# NAME: AYUSH JAIN
# ID: 2017A7PS0093P
######################

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
from functools import partial
import re
from copy import deepcopy
from collections import deque
import time
#######################################
logic_prob = 1
fc = 0
rl = 0

def form_CNF(fname):

    fp = open(fname)
    fout = open(f"KB-{fname}", 'w')
    clauses = []
    logic_kb = PropKB()

    for line in fp.readlines():

        if line:    
            try:
                ex = expr(line)
                clauses.append(ex)
                logic_kb.tell(ex)
                print(ex)
                #fout.write(ex)

            except Exception as e:
                print(str(e))
                print(line)


    
    print(logic_kb.clauses)

    for rule in logic_kb.clauses:
        fout.write(str(rule) + "\n")

    fp.close()
    fout.close()

def form_KB(fname):

    fp = open(fname)
    fout = open(f"KB-{fname}", 'w')
    clauses = []

    for line in fp.readlines():

        if line:    
            try:
                ex = expr(line)
                clauses.append(ex)
                #logic_kb.tell(ex)
                print(ex)
                #fout.write(ex)

            except Exception as e:
                print(str(e))
                print(line)

    logic_kb = FolKB(clauses)
    print(logic_kb.clauses)
    return logic_kb


def query(fname):
    logic_kb = form_KB('ruleFile1.txt')

    fp = open(fname)

    for line in fp.readlines(): 
        answer = fol_fc_ask(logic_kb, expr(line))
        q = list(answer)
        

        if not q:
            print(False)
        elif q and not q[0]:
            print(True)
        else:
            
            print(q[0])   
            
        #print(list(answer)) 

        #answer2 = pl_resolution(logic_kb, expr(line))
        #print(answer2)



#form_KB('ruleFile1.txt')
#query('query1.txt')





#######################################################################################################################################################


class InputWidget(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"AI Game")
        window = QWidget()

        self.normal_button = QPushButton()
        self.normal_button.setFixedSize(QSize(200, 100))
        self.normal_button.setText("Logic Problem 1")
        self.normal_button.pressed.connect(partial(self.open_game, 1))

        self.ab_button = QPushButton()
        self.ab_button.setFixedSize(QSize(200, 100))
        self.ab_button.setText("Logic Problem 2")
        self.ab_button.pressed.connect(partial(self.open_game, 2))
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.ab_button1 = QPushButton()
        self.ab_button1.setFixedSize(QSize(200, 100))
        self.ab_button1.setText("Logic Problem 3")
        self.ab_button1.pressed.connect(partial(self.open_game, 3))
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.label.setText("Choose the logic problem")
        font = self.label.font()
        font.setPointSize(20)
        font.setWeight(65)
        self.label.setFont(font)

        layout =QHBoxLayout()
        layout.addWidget(self.normal_button)
        layout.addWidget(self.ab_button)
        layout.addWidget(self.ab_button1)

        vert_layout = QVBoxLayout()
        vert_layout.addWidget(self.label)
        vert_layout.addLayout(layout)

        window.setLayout(vert_layout)
        self.setCentralWidget(window)
        self.resize(600, 600)
        self.center()
        self.show()

    def open_game(self, val):

        global logic_prob
        logic_prob = val
        self.win = AlgoWidget()
        self.win.show()
        self.close()

    def center(self):

        qr = self.frameGeometry()
        cp  = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class AlgoWidget(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"AI Game")
        window = QWidget()

        self.normal_button = QPushButton()
        self.normal_button.setFixedSize(QSize(200, 100))
        self.normal_button.setText("Forward Chaining")
        self.normal_button.pressed.connect(partial(self.open_game, 0))

        self.ab_button = QPushButton()
        self.ab_button.setFixedSize(QSize(200, 100))
        self.ab_button.setText("Resolution")
        self.ab_button.pressed.connect(partial(self.open_game, 1))
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)


        self.label.setText("Choose the algorithm")
        font = self.label.font()
        font.setPointSize(20)
        font.setWeight(65)
        self.label.setFont(font)

        layout =QHBoxLayout()
        layout.addWidget(self.normal_button)
        layout.addWidget(self.ab_button)

        vert_layout = QVBoxLayout()
        vert_layout.addWidget(self.label)
        vert_layout.addLayout(layout)

        window.setLayout(vert_layout)
        self.setCentralWidget(window)
        self.resize(600, 600)
        self.center()
        self.show()

    def open_game(self, val):

        global logic_prob
        logic_prob = val
        self.win = AlgoWidget()
        self.win.show()
        self.close()

    def center(self):

        qr = self.frameGeometry()
        cp  = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class Tile(QWidget):


    def __init__(self, x , y):

        super().__init__()


        self.setFixedSize(QSize(50, 50))
        self.x = x
        self.y = y

        self.initialize()

    def initialize(self):
        """Contains the states of the mines"""

        self.is_wumpus = False
        #self.number = 0
        self.is_gold = False
        self.is_pit = False
        self.is_start = False

        self.update()


    def set_start(self):
        """Sets flag on discovered mines"""

        self.is_start = True
        self.update()

    def unset_start(self):
        """Sets flag on discovered mines"""

        self.is_start = False
        self.update()    

    def set_wumpus(self):
        """Sets flag on discovered mines"""

        self.is_wumpus = True
        self.update()

    def set_gold(self):
        """Sets flag on discovered mines"""

        self.is_gold = True
        self.update()    

    def set_pit(self):
        """Sets flag on discovered mines"""

        self.is_pit = True
        self.update()


    def paintEvent(self, event):

        pane = QPainter(self)
        pane.setRenderHint(QPainter.Antialiasing)

        object = event.rect()

        if self.is_wumpus:

            pane.fillRect(object, QBrush(Qt.lightGray))
            pen = QPen(Qt.black)
            pen.setWidth(1)
            pane.setPen(pen)
            pane.drawRect(object)

        elif self.is_pit:
            pane.fillRect(object, QBrush(Qt.brown))
            pen = QPen(Qt.black)
            pen.setWidth(1)
            pane.setPen(pen)
            pane.drawRect(object)
            
        elif self.is_gold:
            pane.fillRect(object, QBrush(Qt.gold))
            pen = QPen(Qt.black)
            pen.setWidth(1)
            pane.setPen(pen)
            pane.drawRect(object)
               
        else:
            pane.fillRect(object, QBrush(Qt.white))
            pen = QPen(Qt.black)
            pen.setWidth(1)
            pane.setPen(pen)
            pane.drawRect(object) 

        if self.is_start:
            pane.drawPixmap(object, QPixmap("flag.png"))               

       
class WumpusWorld(QMainWindow):

    def __init__(self):
        super().__init__()

        self.row = 8
        self.col = 8

        self.curr_row = 0
        self.curr_col = 0
        self.setWindowTitle(f"AI Wumpus World")

        vert_layout = QVBoxLayout()

        self.grid = QGridLayout()
        self.grid.setSpacing(1)

        vert_layout.addLayout(self.grid)
        window = QWidget()
        window.setLayout(vert_layout)
        self.setCentralWidget(window)

        self.init_map()
        self.reset_map()

        
        self.show()
        self.move_right()
        self.move_down()
        self.move_right()
        self.move_down()
        self.move_left()
        self.move_up()

        

    def init_map(self):
        """Added boxes on GUI"""

        for r in range(self.row):
            for c in range(self.col):
                box = Tile(r, c)
                self.grid.addWidget(box, r, c)

                

    def reset_map(self):
        """Resets everything to inital state"""

        self.reset_position()
        #self.add_elements()


    def reset_position(self):
        """Clears the tiles"""

        for r in range(self.row):
            for c in range(self.col):
                box = self.grid.itemAtPosition(r, c).widget()
                box.initialize()

        box = self.grid.itemAtPosition(0, 0).widget()        
        box.set_start()

    def move_left(self):
        box = self.grid.itemAtPosition(self.curr_row, self.curr_col).widget()
        box.unset_start()
        if self.curr_col > 0:
            self.curr_col = self.curr_col - 1
            box = self.grid.itemAtPosition(self.curr_row, self.curr_col).widget()
            box.set_start()
        self.delay()    

    def move_right(self):
        box = self.grid.itemAtPosition(self.curr_row, self.curr_col).widget()
        box.unset_start()
        if self.curr_col < 7:
            self.curr_col = self.curr_col + 1
            box = self.grid.itemAtPosition(self.curr_row, self.curr_col).widget()
            box.set_start()
        self.delay()    

    def move_up(self):
        box = self.grid.itemAtPosition(self.curr_row, self.curr_col).widget()
        box.unset_start()
        if self.curr_row > 0:
            self.curr_row = self.curr_row - 1
            box = self.grid.itemAtPosition(self.curr_row, self.curr_col).widget()
            box.set_start()
        self.delay()                    

    def move_down(self):
        box = self.grid.itemAtPosition(self.curr_row, self.curr_col).widget()
        box.unset_start()
        if self.curr_row < 7:
            self.curr_row = self.curr_row + 1
            box = self.grid.itemAtPosition(self.curr_row, self.curr_col).widget()
            box.set_start()
        self.delay()

    def delay(self):
        loop = QEventLoop()
        QTimer.singleShot(2000, loop.quit)
        loop.exec_()

    def add_elements(self):
        """Adds the wumpus, coins and the pit"""
        
        pass
        



app = QApplication(sys.argv)
ex = WumpusWorld()
sys.exit(app.exec_())

