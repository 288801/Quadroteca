import copy
import sys
from enum import Enum

import random
import PyQt5
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication

field_size = 5
cell_size = 70
frame_size = 3

class Color(Enum):
    RED = 1
    YELLOW = 0

class Cell:
    def __init__(self, color=Color.RED):
        super().__init__()
        self.size = cell_size
        self.color = color

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


class MyPaintWidget(PyQt5.QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quadroteca")
        self.setGeometry(100, 100, 800, 600)
        self.painter = QtGui.QPainter(self)

        self.shuffle_btn = QtWidgets.QPushButton('shuffle', self)
        self.shuffle_btn.move(550, 150)
        self.shuffle_btn.setFont(QFont("Times New Roman", 20))
        self.shuffle_btn.clicked.connect(self.shuffle_btn_clicked)

        self.field = GameField()
        self.rows = self.field.check_rows()
        self.label = QtWidgets.QLabel("rows: "+str(self.rows), self)
        self.label.move(550, 250)
        self.label.setFont(QFont("Times New Roman", 20))

        self.show()

    def keyPressEvent(self, e):
        k = e.key()
        if k == Qt.Key_X:
            self.field.rotate()
        if k == Qt.Key_Z:
            self.field.reverse_rotate()
        if k == Qt.Key_W and self.field.frame.i > 0:
            self.field.frame.i -= 1
        if k == Qt.Key_S and self.field.frame.i < field_size-3:
            self.field.frame.i += 1
        if k == Qt.Key_A and self.field.frame.j > 0:
            self.field.frame.j -= 1
        if k == Qt.Key_D and self.field.frame.j < field_size-3:
            self.field.frame.j += 1
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
        self.label.setText("rows: "+str(self.rows))
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
    window = MyPaintWidget()
    sys.exit(app.exec_())
