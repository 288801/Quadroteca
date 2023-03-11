# W - up, S - down, A - left, D - right, K - rotate left, L - rotate right

import copy
import sys
from enum import Enum

import random
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QComboBox

field_size = 5
cell_size = 70
frame_size = 3

class Color(Enum):
    RED = 1
    YELLOW = 0

class Cell:
    def __init__(self, color=Color):
        super().__init__()
        self.size = cell_size
        self.color = color

    @classmethod
    def init_with_params(cls, color=Color, size=int):
        cls.size = size
        cls.color = color

class Frame:
    def __init__(self, i=0, j=0):
        self.i = i
        self.j = j

    def rotate(self, field):
        new_field = copy.deepcopy(field)
        i = self.i
        j = self.j
        field[i][j] = new_field[i+2][j]
        field[i][j+1] = new_field[i+1][j]
        field[i][j+2] = new_field[i][j]
        field[i+1][j] = new_field[i+2][j+1]
        field[i+1][j+2] = new_field[i][j+1]
        field[i+2][j] = new_field[i+2][j+2]
        field[i+2][j+1] = new_field[i+1][j+2]
        field[i+2][j+2] = new_field[i][j+2]

    def reverse_rotate(self, field):
        for i in range(3):
            self.rotate(field)

class GameField:
    def __init__(self):
        super().__init__()
        self.field = []
        self.frame = Frame(0, 0)
        for i in range(field_size):
            self.field.append([])
            for j in range(field_size):
                if j % 2 == 0:
                    self.field[i].append(Cell(Color.RED))
                else:
                    self.field[i].append(Cell(Color.YELLOW))
        self.shuffle()

    def make_true(self):
        for i in range(field_size):
            for j in range(field_size):
                if j % 2 == 0:
                    self.field[i][j].color = Color.RED
                else:
                    self.field[i][j].color = Color.YELLOW

    def rotate(self):
        self.frame.rotate(self.field)

    def reverse_rotate(self):
        self.frame.reverse_rotate(self.field)

    def shuffle(self):
        start_i = self.frame.i
        start_j = self.frame.j
        for i in range(10):
            i = random.randint(0, field_size-3)
            j = random.randint(0, field_size-3)
            self.frame.i = i
            self.frame.j = j
            self.frame.rotate(self.field)
        self.frame.i = start_i
        self.frame.j = start_j

    def check_rows(self):
        result = 0

        for i in range(field_size):
            red_count = 0
            for j in range(field_size):
                if self.field[i][j].color == Color.RED:
                    red_count += 1
            if red_count == field_size or red_count == 0:
                result += 1

        for i in range(field_size):
            red_count = 0
            for j in range(field_size):
                if self.field[j][i].color == Color.RED:
                    red_count += 1
            if red_count == field_size or red_count == 0:
                result += 1

        return result

class Rules(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rules")
        self.setGeometry(200, 200, 600, 400)
        self.label = QtWidgets.QLabel("Клавишами A S D W клавиатуры\nдвигается белый квадратный каркас,\n"
                                      "клавишами 'K' и 'L' вращение\nэтого каркаса с кубиками\nпо"
                                      " и против часовой стрелок.\nShuffle - перемешать кубики", self)
        self.label.setGeometry(0, 0, 600, 400)
        self.label.setFont(QFont("Times New Roman", 20))
        self.show()

class Params(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setGeometry(200, 200, 400, 200)

        self.label1 = QLabel("Выберете размеры поля: ", self)
        self.label1.setGeometry(0, 0, 250, 20)
        self.label1.setFont(QFont("Times New Roman", 12))
        field_s = QComboBox(self)
        field_s.addItem("5x5")
        field_s.addItem("6x6")
        field_s.addItem("7x7")
        field_s.addItem("8x8")
        field_s.addItem("9x9")
        field_s.addItem("10x10")
        field_s.activated[str].connect(self.on_changed1)
        field_s.move(250, 0)

        self.show()
    def on_changed1(self, text):
        global field_size
        field_size = int(text.split("x")[0])
        self.parent.setVisible(False)
        self.setVisible(False)
        self.parent = MainWindow()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quadroteca")
        self.setGeometry(100, 100, 1000, 800)
        self.painter = QtGui.QPainter(self)

        self.steps = 0
        self.step_counter = QtWidgets.QLabel("steps: " + str(self.steps), self)
        self.step_counter.setGeometry(150 + cell_size * field_size, 350, 200, 50)
        self.step_counter.setFont(QFont("Times New Roman", 20))

        self.shuffle_btn = QtWidgets.QPushButton('shuffle', self)
        self.shuffle_btn.move(150 + cell_size*field_size, 150)
        self.shuffle_btn.setFont(QFont("Times New Roman", 20))
        self.shuffle_btn.clicked.connect(self.shuffle_btn_clicked)

        self.field = GameField()
        self.rows = self.field.check_rows()
        self.counter = QtWidgets.QLabel("rows: "+str(self.rows), self)
        self.counter.move(150 + cell_size*field_size, 250)
        self.counter.setFont(QFont("Times New Roman", 20))

        self.win = QtWidgets.QLabel("Вы выиграли!", self)
        self.win.setGeometry(100, cell_size*field_size + 100, 500, 200)
        self.win.setFont(QFont("Times New Roman", 36))
        self.win.setVisible(False)

        self.rules = Rules()
        self.params = Params(self)
        self.rules.setVisible(False)
        self.params.setVisible(False)

        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('File')
        par = QtWidgets.QAction('Parameters', self)
        par.triggered.connect(lambda: self.params_click())
        file_menu.addAction(par)
        rul = QtWidgets.QAction('Rules', self)
        rul.triggered.connect(lambda: self.rules_click())
        file_menu.addAction(rul)

        quit_action = QtWidgets.QAction('Quit', self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        self.show()

    def rules_click(self):
        self.rules.setVisible(True)
        self.update()

    def params_click(self):
        self.params.setVisible(True)
        self.update()

    def keyPressEvent(self, e):
        k = e.key()
        if k == Qt.Key_L:
            self.field.rotate()
            self.steps += 1
        if k == Qt.Key_K:
            self.field.reverse_rotate()
            self.steps += 1
        if k in (Qt.Key_W, Qt.Key_Up) and self.field.frame.i > 0:
            self.field.frame.i -= 1
        if k == Qt.Key_S and self.field.frame.i < field_size-3:
            self.field.frame.i += 1
        if k == Qt.Key_A and self.field.frame.j > 0:
            self.field.frame.j -= 1
        if k == Qt.Key_D and self.field.frame.j < field_size-3:
            self.field.frame.j += 1
        if k == Qt.Key_Q:
            self.field.make_true()
        self.rows = self.field.check_rows()
        self.update()

    def shuffle_btn_clicked(self):
        self.field.shuffle()
        self.rows = self.field.check_rows()
        self.update()

    def paintEvent(self, e):
        self.painter.begin(self)
        pen = QtGui.QPen(QtGui.QColor(0, 0, 0))
        pen.setWidth(2)
        self.painter.setPen(pen)
        self.draw_field(self.painter)
        self.draw_frame(self.painter)
        self.counter.setText("rows: "+str(self.rows))
        self.step_counter.setText("steps: "+str(self.steps))
        if self.rows == field_size:
            self.win.setVisible(True)
        self.painter.end()

    def draw_frame(self, p):
        p.setBrush(QtCore.Qt.NoBrush)
        pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        pen.setWidth(2)
        p.setPen(pen)
        p.drawRect(100 + cell_size//2 + self.field.frame.j * cell_size, 100 + cell_size//2 +
                   self.field.frame.i*cell_size, cell_size*2, cell_size*2)

    def draw_field(self, p):
        for i in range(field_size):
            for j in range(field_size):
                cell = self.field.field[i][j]
                if cell.color == Color.RED:
                    p.setBrush(QtCore.Qt.red)
                else:
                    p.setBrush(QtCore.Qt.yellow)
                p.drawRect(100+j*cell_size, 100+i*cell_size, cell.size, cell.size)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
