#!/usr/bin/env python3
# Copyright (c) 2018-01 Jimin Ma. All rights reserved.


from PyQt5.QtCore import (Qt, QSize, QRectF)
from PyQt5.QtGui import (QPainter, QColor, QFont)
from PyQt5.QtWidgets import (QWidget, QSizePolicy, QDialog, QTableWidget,
                             QTableWidgetItem, QTabWidget, QHBoxLayout,
                             QGridLayout, QHeaderView,
                             QApplication)

import Nuclide

GREEK_DICT = {'a':'\u03B1', 'b':'\u03B2', "EC":'\u03B5'}
KEV_TO_MASS = 931494.


'''上端块'''
class BlockWidgetNuclide(QWidget):

    XMARGIN = 400.0
    YMARGIN = 100.0

    def __init__(self, nuclide, parent=None):
        super(BlockWidgetNuclide, self).__init__(parent)

        self.nuclide = nuclide
        # 固定大小
        self.setFixedSize(QSize(BlockWidgetNuclide.XMARGIN, BlockWidgetNuclide.YMARGIN))

    def sizeHint(self):
        return self.minimumSizeHint()

    def minimumSizeHint(self):
        return QSize(BlockWidgetNuclide.XMARGIN, BlockWidgetNuclide.YMARGIN)

    def paintEvent(self, event=None):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        # 视口与窗口
        painter.setViewport(0, 0, BlockWidgetNuclide.YMARGIN, BlockWidgetNuclide.YMARGIN)
        painter.setWindow(0, 0, BlockWidgetNuclide.YMARGIN, BlockWidgetNuclide.YMARGIN)

        rect = QRectF(0, 0, self.height(), self.height())
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(Qt.blue).lighter(170))
        painter.drawRect(rect)
        # Text for Z, name, symbol
        font = QFont("Combria", 45)
        font.setWeight(QFont.Bold)
        painter.setFont(font)
        painter.setPen(Qt.black)
        painter.drawText(rect, Qt.AlignCenter, "{}".format(self.nuclide.element))
        font = QFont("Courier New", 15)
        font.setWeight(QFont.Bold)
        painter.setFont(font)
        painter.setPen(Qt.black)
        painter.drawText(rect, Qt.AlignLeft, "{}".format(self.nuclide.A))
        painter.drawText(rect, Qt.AlignBottom | Qt.AlignCenter, "{0:.2f}".format(
            float(self.nuclide.mass_defect["value"])/KEV_TO_MASS + self.nuclide.A))

'''
单个元素控件子类
'''

class SingleWidgetNuclide(QDialog):

    def __init__(self, nuclide, parent=None):
        super(SingleWidgetNuclide, self).__init__(parent)

        self.nuclide = nuclide
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

        # 上端控件
        topWidget = BlockWidgetNuclide(self.nuclide)

        # 下端标签页控件
        self.propertyTable = QTableWidget()
        self.propertyTable.clear()
        self.propertyTable.setRowCount(5)
        self.propertyTable.setColumnCount(2)
        self.propertyTable.verticalHeader().setVisible(False)
        self.propertyTable.horizontalHeader().setVisible(False)
        self.propertyTable.setAlternatingRowColors(True)
        self.propertyTable.setEditTriggers(QTableWidget.NoEditTriggers)
        self.propertyTable.setFocusPolicy(Qt.NoFocus)
        header = self.propertyTable.horizontalHeader()   # 设置列宽
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)

        # 给出各行数据
        item = QTableWidgetItem("Mass")
        self.propertyTable.setItem(0, 0, item)
        try:
            item = QTableWidgetItem("{0:.5f} u".format(float(self.nuclide.mass_defect["value"])/KEV_TO_MASS
                                                       + self.nuclide.A))
        except ValueError:
            item = QTableWidgetItem("{0:.5f}{} u".format(self.nuclide.A, self.nuclide.mass_defect["value"]))
        finally:
            self.propertyTable.setItem(0, 1, item)
        item = QTableWidgetItem("Mass Excess")
        self.propertyTable.setItem(1, 0, item)
        item = QTableWidgetItem("{} +/- {} keV".format(self.nuclide.mass_defect["value"],
                                                   self.nuclide.mass_defect["uncertainity"]))
        self.propertyTable.setItem(1, 1, item)
        item = QTableWidgetItem("Half Life")
        self.propertyTable.setItem(2, 0, item)
        item = QTableWidgetItem("{} +/- {} {}".format(
            self.nuclide.half_life["value"], self.nuclide.half_life["uncertainity"],
            self.nuclide.half_life["unit"]))
        self.propertyTable.setItem(2, 1, item)
        item = QTableWidgetItem("Spin")
        self.propertyTable.setItem(3, 0, item)
        item = QTableWidgetItem("{}".format(self.nuclide.gs_spin["value"]))
        self.propertyTable.setItem(3, 1, item)
        item = QTableWidgetItem("Comment")
        self.propertyTable.setItem(4, 0, item)
        if self.nuclide.comment:
            item = QTableWidgetItem("{}".format(self.nuclide.comment.nodeValue))
        else:
            item = QTableWidgetItem(" ")
        self.propertyTable.setItem(4, 1, item)

        # TODO 衰变模式，激发核的情况
        self.decaymodeTable = QTableWidget()
        decaymode = self.nuclide.decay_modes
        row = len(decaymode)
        self.decaymodeTable = QTableWidget()
        self.decaymodeTable.clear()
        self.decaymodeTable.setRowCount(row)
        self.decaymodeTable.setColumnCount(1)
        self.decaymodeTable.verticalHeader().setVisible(False)
        self.decaymodeTable.horizontalHeader().setVisible(False)
        self.decaymodeTable.setAlternatingRowColors(True)
        self.decaymodeTable.setEditTriggers(QTableWidget.NoEditTriggers)
        self.decaymodeTable.setFocusPolicy(Qt.NoFocus)
        header = self.decaymodeTable.horizontalHeader()  # 设置列宽
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        for i, v in enumerate(decaymode):
            v2 = v["mode"]
            for key in GREEK_DICT:
                v2 = v2.replace(key, GREEK_DICT[key])
            item = QTableWidgetItem("{:5s} {} {}+/-{} %".format(
                v2, v["relation"], v["value"], v["uncertainity"]))
            self.decaymodeTable.setItem(i, 0, item)


        # 使用列表给出数据，使用Tab标签式给出不同分类
        tabWidget = QTabWidget()
        commonWidget = QWidget()
        commonLayout = QHBoxLayout()
        commonLayout.addWidget(self.propertyTable)
        commonWidget.setLayout(commonLayout)
        tabWidget.addTab(commonWidget, "Common")
        decaymodeWidget = QWidget()
        decaymodeLayout = QHBoxLayout()
        decaymodeLayout.addWidget(self.decaymodeTable)
        decaymodeWidget.setLayout(decaymodeLayout)
        tabWidget.addTab(decaymodeWidget, "Decay Mode")

        grid = QGridLayout()
        grid.addWidget(topWidget, 0, 0)
        grid.addWidget(tabWidget, 1, 0)
        self.setLayout(grid)

        self.setWindowTitle(self.nuclide.element)

    def closeEvent(self, event):
        self.setMouseTracking(True)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    nuclides = Nuclide.NuclideLibrary()
    form = SingleWidgetNuclide(nuclides.getNuclide(7, 4))
    form.setWindowTitle("GridTest")
    form.show()
    app.exec_()