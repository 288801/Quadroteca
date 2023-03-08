import sys
from enum import Enum

import PyQt5
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QApplication

class Color(Enum):
    RED = 1
    YELLOW = 0

class Cell:
    def __init__(self, x=0, y=0, color=Color.RED):
        super().__init__()
        self.size = 70
        self.x = x
        self.y = y
        self.color = color

class GameField:
    def __init__(self):
        super().__init__()
        self.field = []
        for i in range(5):
            self.field.append([])
            for j in range(5):
                if j % 2 == 0:
                    self.field[i].append(Cell(100+i*70, 100+j*70, Color.RED))
                else:
                    self.field[i].append(Cell(100+i*70, 100+j*70, Color.YELLOW))

    def check_rows(self):
        result = 0

        for i in range(len(self.field)):
            red_count = 0
            for j in range(len(self.field[0])):
                if self.field[i][j].color == Color.RED:
                    red_count += 1
            if red_count == len(self.field[0]) or red_count == 0:
                result += 1

        for i in range(len(self.field[0])):
            red_count = 0
            for j in range(len(self.field)):
                if self.field[j][i].color == Color.RED:
                    red_count += 1
            if red_count == len(self.field) or red_count == 0:
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

    def shuffle_btn_clicked(self):
        for i in range(len(self.field.field)):
            for j in range(len(self.field.field[0])):
                cell = self.field.field[i][j]
                if cell.color == Color.RED:
                    self.field.field[i][j].color = Color.YELLOW
                else:
                    self.field.field[i][j].color = Color.RED
        self.rows = self.field.check_rows()
        self.update()

    def paintEvent(self, e):
        self.painter.begin(self)
        pen = QtGui.QPen(QtGui.QColor(0, 0, 0))
        pen.setWidth(2)
        self.painter.setPen(pen)
        self.draw_field(self.painter)
        self.label.setText("rows: "+str(self.rows))
        self.painter.end()

    def draw_field(self, p):
        for i in range(len(self.field.field)):
            for j in range(len(self.field.field[0])):
                cell = self.field.field[i][j]
                if cell.color == Color.RED:
                    p.setBrush(QtCore.Qt.red)
                else:
                    p.setBrush(QtCore.Qt.yellow)
                p.drawRect(cell.x, cell.y, cell.size, cell.size)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyPaintWidget()
    sys.exit(app.exec_())
