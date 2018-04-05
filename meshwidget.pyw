#!/usr/bin/env python3
# Copyright (c) 2018-01 Jimin Ma. All rights reserved.

import math

from PyQt5.QtCore import (Qt, QSize, QRectF, QPointF, QTimer, QLineF)
from PyQt5.QtGui import (QPainter, QPen, QColor, QFont, QPalette, QPolygonF,
                         QFontMetricsF)
from PyQt5.QtWidgets import (QWidget, QSizePolicy, QDialog, QApplication)

import Nuclide
import singlewidgetNuclide

BLANK, NOBLANK = range(2)
NMAX, ZMAX = 180, 120
NZ_MARGIN = 8
MAGIC_NUMBERS_N = [2, 8, 20, 28, 50, 82, 126]
MAGIC_NUMBERS_Z = [2, 8, 20, 28, 50, 82, 114]
MAGIC_NUMBERS_LINE_N = [[0, 15], [0, 30], [4, 50], [6, 60], [15, 70], [30, 90],
                        [60, 118]]
MAGIC_NUMBERS_LINE_Z = [[0, 15], [0, 30], [6, 60], [8, 60], [25, 95], [75, 150],
                        [120, 180]]
# Definition of colors used for decay modes
COLORS = { 'is': '#000000',
           'b-': '#62aeff',
           '2b-': '#62aeff',
           'b+': '#ff7e75',
           'ec': '#ff7e75',
           '2ec': '#ff7e75',
           'a' : '#fffe49',
           'sf': '#5cbc57',
           'p' : '#ffa425',
           '2p': '#ffa425',
           'n' : '#9fd7ff',
           '2n': '#9fd7ff',
           'it': '#ffffff',
           'cluster': '#a564cc',
           '?': '#cccccc' }

'''
元素周期表中心控件子类
'''

class MeshWidget(QWidget):

    def __init__(self, nuclides, parent=None):
        super(MeshWidget, self).__init__(parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.nuclides = nuclides    # 元素数据库
        self.grid = [[BLANK] * ZMAX for i in range(NMAX)]
        self.nuc = [[None] * ZMAX for i in range(NMAX)]
        for i, nuclide in enumerate(self.nuclides):
            n = nuclide.N
            z = nuclide.Z
            self.grid[n][z] = i+1  # NOBLANK
            self.nuc[n][z] = nuclide

        self.selected = [0, 0]
        self.setMinimumSize(self.minimumSizeHint())
        self.mouseX = 0
        self.mouseY = 0
        self.setMouseTracking(True)
        self.dlg = QDialog()

    def sizeHint(self):
        # 设置默认大小
        return QSize(1800, 1100)

    def minimumSizeHint(self):
        return QSize(900, 500)

    def paintEvent(self, event):
        font = QFont(self.font())
        font.setPointSize(font.pointSize() - 1)
        fm = QFontMetricsF(font)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        xOffset = self.width() / (NMAX + NZ_MARGIN)
        yOffset = self.height() / (ZMAX + NZ_MARGIN)

        # 若存在对话框，则不实时绘图
        if self.dlg.isVisible():
            self.setMouseTracking(False)
        else:
            self.setMouseTracking(True)

        for nuclide in self.nuclides:
            n, z = nuclide.N, nuclide.Z
            x, y = n + NZ_MARGIN, ZMAX - nuclide.Z - 1
            rect = (QRectF(x * xOffset, y * yOffset,
                           xOffset, yOffset).adjusted(0.5, 0.5, -0.5, -0.5))
            segColor = QColor(0, 0, 0)
            if self.grid[n][z] : #== NOBLANK:
                segColor.setNamedColor(self.getNuclideColor(nuclide))
            if segColor is not None:
                painter.setBrush(segColor)

            if [x, y] == self.selected:
                painter.setPen(QPen(Qt.blue, 3))
            else:
                # painter.setPen(self.palette().color(QPalette.Background))
                painter.setPen(Qt.NoPen)
            painter.drawRect(rect)

        # Draw magic lines
        painter.setPen(QPen(Qt.blue, 0.4))
        for nmagic in range(len(MAGIC_NUMBERS_N)):
            x1 = (MAGIC_NUMBERS_N[nmagic] + NZ_MARGIN) * xOffset
            y1 = (ZMAX - MAGIC_NUMBERS_LINE_N[nmagic][0] - 1) * yOffset
            x2 = (MAGIC_NUMBERS_N[nmagic] + 1 + NZ_MARGIN) * xOffset
            y2 = (ZMAX - MAGIC_NUMBERS_LINE_N[nmagic][1]) * yOffset
            painter.drawLine(QPointF(x1, y1), QPointF(x1, y2))
            painter.drawLine(QPointF(x2, y1), QPointF(x2, y2))
        for zmagic in range(len(MAGIC_NUMBERS_Z)):
            x1 = (MAGIC_NUMBERS_LINE_Z[zmagic][0] + NZ_MARGIN) * xOffset
            y1 = (ZMAX - MAGIC_NUMBERS_Z[zmagic] - 1 ) * yOffset
            x2 = (MAGIC_NUMBERS_LINE_Z[zmagic][1] + NZ_MARGIN) * xOffset
            y2 = (ZMAX - MAGIC_NUMBERS_Z[zmagic]) * yOffset
            painter.drawLine(QPointF(x1, y1), QPointF(x2, y1))
            painter.drawLine(QPointF(x1, y2), QPointF(x2, y2))

        # Draw coordinate system
        for i in range(NMAX):
            painter.setPen(Qt.black)
            iM = i + NZ_MARGIN
            if i % 10 :
                if not (i % 5):
                    painter.drawLine((iM + 0.5) * xOffset, (ZMAX + NZ_MARGIN - 3.5) * yOffset,
                                     (iM + 0.5) * xOffset, (ZMAX + NZ_MARGIN - 6.5) * yOffset)
                else:
                    painter.drawLine((iM + 0.5) * xOffset, (ZMAX + NZ_MARGIN - 3.5) * yOffset,
                                     (iM + 0.5) * xOffset, (ZMAX + NZ_MARGIN - 5.0) * yOffset)
            else:
                painter.drawLine((iM + 0.5) * xOffset, (ZMAX + NZ_MARGIN - 3.5) * yOffset,
                                 (iM + 0.5) * xOffset, (ZMAX + NZ_MARGIN - 7.5) * yOffset)
                rect = QRectF(fm.boundingRect("999"))
                rect.moveCenter(QPointF((iM + 0.5) * xOffset, (ZMAX + NZ_MARGIN - 1.5) * yOffset))
                painter.drawText(rect, Qt.AlignCenter, "{}".format(i))

        for i in range(ZMAX):
            painter.setPen(Qt.black)
            if i % 10 :
                if not (i % 5):
                    painter.drawLine(3.5 * xOffset, (ZMAX - i - 0.5) * yOffset,
                                     6.5 * xOffset, (ZMAX - i - 0.5) * yOffset)
                else:
                    painter.drawLine(3.5 * xOffset, (ZMAX - i - 0.5) * yOffset,
                                     5.0 * xOffset, (ZMAX - i - 0.5) * yOffset)
            else:
                painter.drawLine(3.5 * xOffset, (ZMAX - i - 0.5) * yOffset,
                                 7.5 * xOffset, (ZMAX - i - 0.5) * yOffset)
                rect = QRectF(fm.boundingRect("999"))
                rect.moveCenter(QPointF(1.5 * xOffset, (ZMAX - i - 0.5) * yOffset))
                painter.drawText(rect, Qt.AlignCenter, "{}".format(i))

        # Draw coordinate title and arrow
        font = QFont("Courier", 20)
        font.setPointSize(font.pointSize() + 1)
        fm = QFontMetricsF(font)
        painter.setFont(font)
        rect = QRectF(fm.boundingRect("9"))
        rect.moveCenter(QPointF((NMAX * 0.5 + 10) * xOffset, (ZMAX + NZ_MARGIN - 10.0) * yOffset))
        painter.drawText(rect, Qt.AlignCenter, "N")
        rect = QRectF(fm.boundingRect("9"))
        rect.moveCenter(QPointF(10. * xOffset, (ZMAX * 0.5) * yOffset))
        painter.drawText(rect, Qt.AlignCenter, "Z")


        # Draw Zoom out Nuclide
        # x = event.pos().x() / xOffset
        # y = event.pos().y() / yOffset
        x, y = self.mouseX, self.mouseY
        n, z = x - NZ_MARGIN, ZMAX - y - 1
        print("{} {} ==> {} {}".format(x, y, n, z))
        if n >= 0 and self.grid[n][z] : # == NOBLANK:
            painter.setPen(QPen(Qt.blue, 2))
            rect = (QRectF(x * xOffset, y * yOffset,
                           xOffset, yOffset).adjusted(0.5, 0.5, -0.5, -0.5))
            painter.drawRect(rect)
            # 绘制元素名称
            rect = QRectF(50, 50, 150, 150)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(Qt.blue).lighter(170))
            painter.drawRect(rect)
            # Text for Z, name, symbol
            font = QFont("Arial", 50)
            font.setWeight(QFont.Bold)
            painter.setFont(font)
            painter.setPen(Qt.black)
            painter.drawText(rect, Qt.AlignCenter, "{}".format(self.nuclides.getNuclide(n, z).element))
            font = QFont("Courier New", 15)
            font.setWeight(QFont.Bold)
            painter.setFont(font)
            painter.setPen(Qt.black)
            painter.drawText(rect, Qt.AlignLeft | Qt.AlignBottom, "{}".format(z))
            painter.drawText(rect, Qt.AlignLeft | Qt.AlignTop, "{}".format(
                self.nuclides.getNuclide(n, z).A))

        QTimer.singleShot(5000, self.update)

    # 定义鼠标移动事件
    def mouseMoveEvent(self, event):
        xOffset = self.width() / (NMAX + NZ_MARGIN)
        yOffset = self.height() / (ZMAX + NZ_MARGIN)
        x = math.floor(event.pos().x() / xOffset)
        y = math.floor(event.pos().y() / yOffset)
        self.mouseX = x
        self.mouseY = y
        self.update()

    # 鼠标按下事件
    def mousePressEvent(self, event):
        x, y = self.mouseX, self.mouseY
        n, z = x - NZ_MARGIN, ZMAX - y - 1
        if self.grid[n][z]:
            self.dlg = singlewidgetNuclide.SingleWidgetNuclide(self.nuclides.getNuclide(n, z))
            self.dlg.show()
            self.setMouseTracking(False)
        self.update()

    def event(self, event):
        return QWidget.event(self, event)

    # 按照核素主要衰变模式，确定颜色
    def getNuclideColor(self, nuclide):
        """ Get the primary decay mode for nuclide as color"""

        # List of accepted basic decay modes, primary color is chosen on
        # that basis. A '?' mode is for placeholders.
        basic_decay_modes = ['is', 'a', 'b-', 'b+',
                               'ec', 'p', '2p', 'sf',
                               'n', '2n', '2ec', '2b-']
        # This reg ex. matches cluster emission marked by isotopic name
        # it matches names starting by at excatly two digits and
        # ending with letter(s). Remember that all decay modes are lower cased!
        # Cluster decays are only secondary or tertiary
        cluster_re = r'[0-9]{2}([a-z]+)$'

        primary_color = None
        # First decay mode should be largest and should match one
        # of basic decay modes
        if nuclide.decay_modes[0]['mode'] in basic_decay_modes:
            primary_color = COLORS[nuclide.decay_modes[0]['mode']]
        elif nuclide.decay_modes[0]['mode'] == '?':
            primary_color = COLORS['?']
        else:
            # Order of basic and secondary decay modes is not kept well in NWC data
            # eg. sometimes B+p is given before B+
            # We will swap two element so any basic mode comes first
            if len(nuclide.decay_modes) > 1:
                i = 0
                for i in range(1, len(nuclide.decay_modes)):
                    if nuclide.decay_modes[i]['mode'] in basic_decay_modes:
                        nuclide.decay_modes[0], nuclide.decay_modes[i] = nuclide.decay_modes[i], nuclide.decay_modes[0]
                        primary_color = COLORS[nuclide.decay_modes[0]['mode']]
                        break

        return primary_color


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    nuclides = Nuclide.NuclideLibrary()
    form = MeshWidget(nuclides)
    form.setWindowTitle("GridTest")
    form.show()
    app.exec_()