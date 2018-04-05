#!/usr/bin/env python3
# Copyright (c) 2018-01 Jimin Ma. All rights reserved.

import math

from PyQt5.QtCore import (Qt, QSize, QRectF)
from PyQt5.QtGui import (QPainter, QPen, QColor, QFont, QPalette)
from PyQt5.QtWidgets import (QWidget, QSizePolicy, QApplication)

import element
import singlewidget

BLANK, NOBLANK = range(2)


'''
元素周期表中心控件子类
'''

class GridWidget(QWidget):

    def __init__(self, elements, parent=None):
        super(GridWidget, self).__init__(parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.elements = elements    # 元素数据库
        self.grid = [[BLANK] * 11 for i in range(18)]
        for element in self.elements:
            x, y = element.pos()
            self.grid[x][y] = NOBLANK

        self.selected = [0, 0]
        self.setMinimumSize(self.minimumSizeHint())

    def sizeHint(self):
        # 设置默认大小
        return QSize(1800, 1100)

    def minimumSizeHint(self):
        return QSize(900, 500)

    def mousePressEvent(self, event):
        # 鼠标按下事件
        xOffset = self.width() / 18
        yOffset = self.height() / 11
        x = math.floor(event.x() / xOffset) + 1
        y = math.floor(event.y() / yOffset)
        if self.grid[x-1][y]:
            self.dlg = singlewidget.SingleWidget(self.elements.getElement(x, y))
            self.dlg.show()
        self.update()

    def paintEvent(self, event=None):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        xOffset = self.width() / 18
        yOffset = self.height() / 11

        for element in self.elements:
            x, y = element.pos()
            rect = (QRectF(x * xOffset, y * yOffset,
                           xOffset, yOffset * 0.7).adjusted(0.5, 0.5, -0.5, -0.5))
            segColor = None
            if element.phase == "Solid":
                segColor = QColor(Qt.blue).lighter(180)
            elif element.phase == "Gas":
                segColor = QColor(Qt.cyan).lighter(180)
            elif element.phase == "Liquid":
                segColor = QColor(Qt.magenta).lighter(180)
            if segColor is not None:
                painter.setBrush(segColor)

            if [x, y] == self.selected:
                painter.setPen(QPen(Qt.blue, 3))
            else:
                painter.setPen(Qt.NoPen)
            painter.drawRect(rect)
            # 写文本
            font = QFont("Courier New", 15)
            font.setWeight(QFont.Bold)
            painter.setFont(font)
            painter.setPen(Qt.black)
            painter.drawText(rect, Qt.AlignCenter,
                             "{}".format(element.symbol))
            # 写元素的Z值
            segColor = segColor.darker(150)
            painter.setBrush(segColor)
            painter.setPen(Qt.NoPen)
            rect = (QRectF(x * xOffset, (y+0.7) * yOffset,
                           xOffset, 0.3 * yOffset).adjusted(0.5, 0.5, -0.5, -0.5))
            painter.drawRect(rect)
            painter.setPen(Qt.black)
            font = QFont("Courier New", 10)
            font.setWeight(QFont.Bold)
            painter.setFont(font)
            painter.drawText(rect, Qt.AlignCenter, "{}".format(element.Z))


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    elements = element.ElementLibrary()
    form = GridWidget(elements)
    form.setWindowTitle("GridTest")
    form.show()
    app.exec_()