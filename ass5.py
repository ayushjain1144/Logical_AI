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


wumpus_pos = [[0, 4], [4, 3], [4, 7], [5, 3]]
pit_pos = [[1, 6], [2, 7], [3, 1], [5, 1], [7, 2], [7, 4]]
gold_pos = [[5, 5]]

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
    fout = open(f'output-{fname}', 'w')

    for line in fp.readlines(): 
        answer = fol_fc_ask(logic_kb, expr(line))
        q = list(answer)
    

        if not q:
            print(False)
            fout.write(f"{expr(line)}: False\n")
        elif q and not q[0]:
            print(True)
            fout.write(f"{expr(line)}: True\n")
        else:
            
            print(q[0])
            fout.write(f"{expr(line)}: {q[0]}\n")   
            
        #print(list(answer)) 

        #answer2 = pl_resolution(logic_kb, expr(line))
        #print(answer2)









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

        if val == 1:
            self.win = Logic1Widget()
        elif val == 2:
            self.win = Logic2Widget()
        else:
            self.win = WumpusWorld()        
        #self.win = AlgoWidget()
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
        self.win = InputWidget()
        self.win.show()
        self.close()

    def center(self):

        qr = self.frameGeometry()
        cp  = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())




class Logic1Widget(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"AI Game")
        window = QWidget()

        self.normal_button = QPushButton()
        self.normal_button.setFixedSize(QSize(200, 100))
        self.normal_button.setText("Logic Problem 2")
        self.normal_button.pressed.connect(partial(self.open_game, 2))

        self.ab_button = QPushButton()
        self.ab_button.setFixedSize(QSize(200, 100))
        self.ab_button.setText("Logic Problem 3")
        self.ab_button.pressed.connect(partial(self.open_game, 3))
        vert_layout = QVBoxLayout()

        form_KB('ruleFile1.txt')
        query('query1.txt')
        
        lb1_R1 = QLabel(self)
        lb1_R2 = QLabel(self)
        lb1_R3 = QLabel(self)
        lb1_R4 = QLabel(self)
        lb1_R5 = QLabel(self)
        lb1_R6 = QLabel(self)
        lb1_R7 = QLabel(self)
        lb1_R8 = QLabel(self)
        lbl_R9 = QLabel(self)

        lbl_list = [lb1_R1, lb1_R2, lb1_R3, lb1_R4, lb1_R5, lb1_R6, lb1_R7]
        fp = open('output-query1.txt')
        for i, line in enumerate(fp.readlines()):
            if line:
                lbl_list[i].setText(f"{line}")
                vert_layout.addWidget(lbl_list[i])

        layout =QHBoxLayout()
        layout.addWidget(self.normal_button)
        layout.addWidget(self.ab_button)

        
        vert_layout.addLayout(layout)

        window.setLayout(vert_layout)
        self.setCentralWidget(window)
        self.resize(600, 600)
        self.center()
        self.show()

    def open_game(self, val):

        global logic_prob
        logic_prob = val
        if val == 2:
            self.win = Logic2Widget()
        else:
            self.win = WumpusWorld()    
        self.win.show()
        self.close()

    def center(self):

        qr = self.frameGeometry()
        cp  = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class Logic2Widget(QMainWindow):

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
        self.ab_button.setText("Logic Problem 3")
        self.ab_button.pressed.connect(partial(self.open_game, 3))
        vert_layout = QVBoxLayout()
        
        lb1_R1 = QLabel(self)
        lb1_R2 = QLabel(self)
        lb1_R3 = QLabel(self)
        lb1_R4 = QLabel(self)
        lb1_R5 = QLabel(self)
        lb1_R6 = QLabel(self)
        lb1_R7 = QLabel(self)
        lb1_R8 = QLabel(self)
        lbl_R9 = QLabel(self)
        lbl_R10 = QLabel(self)

        lbl_list = [lb1_R1, lb1_R2, lb1_R3, lb1_R4, lb1_R5, lb1_R6, lb1_R7, lb1_R8, lbl_R9, lbl_R10]
        fp = open('output-query2.txt')
        for i, line in enumerate(fp.readlines()):
            if line:
                lbl_list[i].setText(f"{line}")
                vert_layout.addWidget(lbl_list[i])

        layout =QHBoxLayout()
        layout.addWidget(self.normal_button)
        layout.addWidget(self.ab_button)

        
        vert_layout.addLayout(layout)

        window.setLayout(vert_layout)
        self.setCentralWidget(window)
        self.resize(600, 600)
        self.center()
        self.show()

    def open_game(self, val):

        global logic_prob
        logic_prob = val
        if val == 1:
            self.win = Logic1Widget()
        else:
            self.win = WumpusWorld()    
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


        self.setFixedSize(QSize(100, 100))
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
            pane.fillRect(object, QBrush(Qt.darkRed))
            pen = QPen(Qt.black)
            pen.setWidth(1)
            pane.setPen(pen)
            pane.drawRect(object)
            
        elif self.is_gold:
            pane.fillRect(object, QBrush(Qt.yellow))
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

        self.action = "Stay"
        self.percept = "No percept"
        self.label1 = QLabel()
        self.label1.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.label1.setText(f"Percept: {self.percept}")

        font = self.label1.font()
        font.setPointSize(20)
        font.setWeight(65)
        self.label1.setFont(font)
        self.label1.setFont(font)


        self.label2 = QLabel()
        self.label2.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.label2.setText(f"Action: {self.action}")

        font = self.label2.font()
        font.setPointSize(20)
        font.setWeight(65)
        self.label2.setFont(font)
        self.label2.setFont(font)

        self.fp = open('wumpusWorld.txt')


        hor_layout = QHBoxLayout()
        hor_layout.addWidget(self.label1)
        hor_layout.addWidget(self.label2)

        vert_layout = QVBoxLayout()
        vert_layout.addLayout(hor_layout)
        self.grid = QGridLayout()
        self.grid.setSpacing(1)

        vert_layout.addLayout(self.grid)
        window = QWidget()
        window.setLayout(vert_layout)
        self.setCentralWidget(window)

        self.init_map()
        self.reset_map()

        
        self.show()
        self.take_actions()

        
    def update_percept(self):

        self.percept = self.fp.readline()
        print(self.percept)
        self.label1.setText(f"Percept: {self.percept}")
        self.delay()

    def init_map(self):
        """Added boxes on GUI"""

        for r in range(self.row):
            for c in range(self.col):
                box = Tile(r, c)
                self.grid.addWidget(box, r, c)

                

    def reset_map(self):
        """Resets everything to inital state"""

        self.reset_position()
        self.add_elements()


    def reset_position(self):
        """Clears the tiles"""

        for r in range(self.row):
            for c in range(self.col):
                box = self.grid.itemAtPosition(r, c).widget()
                box.initialize()

        box = self.grid.itemAtPosition(0, 0).widget()        
        box.set_start()

    def move_left(self):
        self.action = "move left"
        self.update_percept()
        self.label2.setText(f"Action: {self.action}")

        box = self.grid.itemAtPosition(self.curr_row, self.curr_col).widget()
        box.unset_start()
        if self.curr_col > 0:
            self.curr_col = self.curr_col - 1
            box = self.grid.itemAtPosition(self.curr_row, self.curr_col).widget()
            box.set_start()
        self.delay()    

    def move_right(self, num = 1):
        
        
        for i in range(num):
            self.update_percept()
            self.action = "move_right"
            self.label2.setText(f"Action: {self.action}")
            box = self.grid.itemAtPosition(self.curr_row, self.curr_col).widget()
            box.unset_start()
            if self.curr_col < 7:
                self.curr_col = self.curr_col + 1
                box = self.grid.itemAtPosition(self.curr_row, self.curr_col).widget()
                box.set_start()
                
            self.delay()    

    def move_up(self):
        self.action = "move_up"
        self.update_percept()
        self.label2.setText(f"Action: {self.action}")
        
        
        box = self.grid.itemAtPosition(self.curr_row, self.curr_col).widget()
        box.unset_start()
        if self.curr_row > 0:
            self.curr_row = self.curr_row - 1
            box = self.grid.itemAtPosition(self.curr_row, self.curr_col).widget()
            box.set_start()
        self.delay()  

    def take_actions(self):
        self.delay()
        self.move_right(3)
        self.move_left()                     
        self.move_down()
        self.move_right(2)
        self.move_left()
        self.move_down()
        self.move_right(3)
        self.move_left()
        self.move_down()
        self.move_right(2)
        self.move_left()
        self.move_down()
        self.move_up()
        self.move_left()
        self.move_down()
        self.move_right()
        self.move_left()
        self.move_down()
        self.action = "grab"
        self.label2.setText(f"Action: {self.action}")



    def move_down(self):
        self.action = "move_down"
        self.update_percept()
        self.label2.setText(f"Action: {self.action}")
        
       
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
        
        global wumpus_pos
        global pit_pos
        global gold_pos

        for i in wumpus_pos:
            box = self.grid.itemAtPosition(i[0], i[1]).widget()
            box.set_wumpus()
        for i in pit_pos:
            box = self.grid.itemAtPosition(i[0], i[1]).widget()
            box.set_pit()
        for i in gold_pos:
            box = self.grid.itemAtPosition(i[0], i[1]).widget()
            box.set_gold()        

        



app = QApplication(sys.argv)
ex = InputWidget()
sys.exit(app.exec_())

