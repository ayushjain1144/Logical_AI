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


        self.setFixedSize(QSize(25, 25))
        self.x = x
        self.y = y

        self.initialize()

    def initialize(self):
        """Contains the states of the mines"""

        self.is_wumpus = False
        #self.number = 0
        self.is_gold = False
        self.is_pit = False
        self.is_clicked = False

        self.update()

    def set_flag(self):
        """Sets flag on discovered mines"""

        self.is_flagged = True
        self.reveal()



    def reveal(self):
        """Reveal the tile"""

        self.is_revealed = True
        self.update()
        self.revealed.emit(self)

    def undo_reveal(self):
        """Undo Reveal of tile"""

        self.is_revealed = False
        self.update()
        self.revealed.emit(self)


    def left_click(self):
        """Emulates the functionality of left click in real Minesweeper"""

        self.revealed.emit(self)

        if self.number == 0:
            self.expandable.emit(self.row,  self.col)
        self.clicked.emit()


    def paintEvent(self, event):

        pane = QPainter(self)
        pane.setRenderHint(QPainter.Antialiasing)

        object = event.rect()

        #Conditions if the square is is_revealed

        if self.is_revealed:

            if not self.is_clicked:
                pane.fillRect(object, QBrush(Qt.green))
                pen = QPen(Qt.green)
            else:
                pane.fillRect(object, QBrush(Qt.blue))
                pen = QPen(Qt.blue)
            pen.setWidth(1)
            pane.setPen(pen)
            pane.drawRect(object)

            if self.is_mine and not self.is_flagged:

                pane.drawPixmap(object, QPixmap("bomb.png"))

            elif self.is_flagged:
                pane.drawPixmap(object, QPixmap("flag.png"))
                pane.setOpacity(0.3)
                pane.drawPixmap(object, QPixmap("bomb.png"))


            elif self.number > 0:

                pen = QPen(Qt.red)
                pane.setPen(pen)
                font = pane.font()
                font.setBold(True)
                pane.setFont(font)

                pane.drawText(object, Qt.AlignHCenter | Qt.AlignVCenter, str(self.number))

        else:

            pane.fillRect(object, QBrush(Qt.lightGray))
            pen = QPen(Qt.gray)
            pen.setWidth(1)
            pane.setPen(pen)
            pane.drawRect(object)




            if self.is_mine:
                pane.setOpacity(0.3)
                pane.drawPixmap(object, QPixmap("bomb.png"))



app = QApplication(sys.argv)
ex = InputWidget()
sys.exit(app.exec_())

