#!/usr/bin/env python3
# Copyright (c) 2018-01 Jimin Ma. All rights reserved.


from PyQt5.QtCore import (Qt, QSize, QRectF)
from PyQt5.QtGui import (QPainter, QColor, QFont)
from PyQt5.QtWidgets import (QWidget, QSizePolicy, QDialog, QTableWidget,
                             QTableWidgetItem, QTabWidget, QHBoxLayout,
                             QGridLayout, QHeaderView,
                             QApplication)
GREEK_DICT = {'a':'\u03B1', 'b':'\u03B2', "EC":'\u03B5'}

import element

'''上端块'''
class BlockWidget(QWidget):

    XMARGIN = 400.0
    YMARGIN = 100.0

    def __init__(self, element, parent=None):
        super(BlockWidget, self).__init__(parent)

        self.element = element
        # 固定大小
        self.setFixedSize(QSize(BlockWidget.XMARGIN, BlockWidget.YMARGIN))

        # 设置主要参数列表
        self.table = QTableWidget(self)
        self.updateTable()


    def sizeHint(self):
        return self.minimumSizeHint()

    def minimumSizeHint(self):
        return QSize(BlockWidget.XMARGIN, BlockWidget.YMARGIN)

    # 尺寸大小调整事件，用于确定子窗口部件的位置
    def resizeEvent(self, event=None):
        x = BlockWidget.YMARGIN
        y = 0
        self.table.move(x, y)   # 将常用表格定位在右端

    def paintEvent(self, event=None):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        # 视口与窗口
        painter.setViewport(0, 0, BlockWidget.YMARGIN, BlockWidget.YMARGIN)
        painter.setWindow(0, 0, BlockWidget.YMARGIN, BlockWidget.YMARGIN)

        rect = QRectF(0, 0, self.height(), self.height())
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(Qt.blue).lighter(170))
        painter.drawRect(rect)
        # Text for Z, name, symbol
        font = QFont("Cambria", 45)
        font.setWeight(QFont.Bold)
        painter.setFont(font)
        painter.setPen(Qt.black)
        painter.drawText(rect, Qt.AlignCenter, "{}".format(self.element.symbol))
        font = QFont("Courier New", 15)
        font.setWeight(QFont.Bold)
        painter.setFont(font)
        painter.setPen(Qt.black)
        painter.drawText(rect, Qt.AlignLeft, "{}".format(self.element.number))
        painter.drawText(rect, Qt.AlignBottom | Qt.AlignCenter,
                         "{:.2f}".format(self.element.atomicMass))

    def updateTable(self):
        self.table.clear()
        self.table.setRowCount(4)
        self.table.setColumnCount(2)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)

        self.table.horizontalHeader().setDefaultSectionSize(15)
        self.table.setShowGrid(False)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)    # 不可编辑
        self.table.setSelectionMode(QTableWidget.NoSelection)      # 不可选中

        # 给出各行数据
        item = QTableWidgetItem("Density")
        self.table.setItem(0, 0, item)
        item = QTableWidgetItem("{} g/cm^3".format(self.element.density))
        self.table.setItem(0, 1, item)
        item = QTableWidgetItem("Melt Point ")
        self.table.setItem(1, 0, item)
        item = QTableWidgetItem("{} K".format(self.element.melt))
        self.table.setItem(1, 1, item)
        item = QTableWidgetItem("Moler Heat ")
        self.table.setItem(2, 0, item)
        item = QTableWidgetItem("{} mol*K".format(self.element.molarHeat))
        self.table.setItem(2, 1, item)

        # 调整表格宽度
        self.table.resizeColumnsToContents()


'''
单个元素控件子类
'''

class SingleWidget(QDialog):

    def __init__(self, element, parent=None):
        super(SingleWidget, self).__init__(parent)

        self.element = element
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

        # 上端控件
        topWidget = BlockWidget(self.element)

        # 下端标签页控件
        # --- Page 1: 基本信息 ---
        self.propertyTable = QTableWidget()
        self.propertyTable.clear()
        self.propertyTable.setRowCount(4)
        self.propertyTable.setColumnCount(2)
        self.propertyTable.verticalHeader().setVisible(False)
        self.propertyTable.horizontalHeader().setVisible(False)
        self.propertyTable.setAlternatingRowColors(True)
        self.propertyTable.setEditTriggers(QTableWidget.NoEditTriggers)
        self.propertyTable.setFocusPolicy(Qt.NoFocus)
        header = self.propertyTable.horizontalHeader()  # 设置列宽
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)

        # 给出各行数据
        item = QTableWidgetItem("phase")
        self.propertyTable.setItem(0, 0, item)
        item = QTableWidgetItem("{}".format(self.element.phase))
        self.propertyTable.setItem(0, 1, item)
        item = QTableWidgetItem("shells")
        self.propertyTable.setItem(1, 0, item)
        item = QTableWidgetItem("{}".format(self.element.shells))
        self.propertyTable.setItem(1, 1, item)
        item = QTableWidgetItem("Named By")
        self.propertyTable.setItem(2, 0, item)
        item = QTableWidgetItem("{}".format(self.element.namedBy))
        self.propertyTable.setItem(2, 1, item)
        item = QTableWidgetItem("Summary")
        self.propertyTable.setItem(3, 0, item)
        item = QTableWidgetItem("{}".format(self.element.summary))
        self.propertyTable.setItem(3, 1, item)

        # --- Page 2: 核素信息 ---
        self.isotopeTable = QTableWidget()
        self.isotopeTable.clear()
        self.isotopeTable.setRowCount(len(self.element.isotopes))
        self.isotopeTable.setColumnCount(5)
        self.isotopeTable.verticalHeader().setVisible(False)
        self.isotopeTable.setHorizontalHeaderLabels(["Isotope", "Weight", "Abund,%",
                                                     "Half-life", "Decay"])
        self.isotopeTable.setAlternatingRowColors(True)
        self.isotopeTable.setEditTriggers(QTableWidget.NoEditTriggers)
        self.isotopeTable.setFocusPolicy(Qt.NoFocus)

        for i, isotope in enumerate(self.element.isotopes):
            item = QTableWidgetItem("{}-{}".format(isotope.element, isotope.A))
            self.isotopeTable.setItem(i, 0, item)
            try:
                item = QTableWidgetItem("{:.4f}".format(float(isotope.mass_defect["value"])/931494.
                                                    + isotope.A))
            except ValueError:
                item = QTableWidgetItem("~{}".format(isotope.A))
            finally:
                self.isotopeTable.setItem(i, 1, item)
            if isotope.half_life["value"] == "stable":
                item = QTableWidgetItem("{}".format(isotope.decay_modes[0]["value"]))
                self.isotopeTable.setItem(i, 2, item)
            else:
                item = QTableWidgetItem("{} {}".format(isotope.half_life["value"],
                                                       isotope.half_life["unit"]))
                self.isotopeTable.setItem(i, 3, item)
                str = []
                for j, v in enumerate(isotope.decay_modes):
                    v2 = v["mode"]
                    for key in GREEK_DICT:
                        v2 = v2.replace(key, GREEK_DICT[key])
                    str.append("{}({})".format(v2, v["value"]))
                item = QTableWidgetItem("{}".format(",".join(str)))
                self.isotopeTable.setItem(i, 4, item)

        self.isotopeTable.resizeColumnsToContents()


        # 使用列表给出数据，使用Tab标签式给出不同分类
        tabWidget = QTabWidget()
        propertyWidget = QWidget()
        propertyLayout = QHBoxLayout()
        propertyLayout.addWidget(self.propertyTable)
        propertyWidget.setLayout(propertyLayout)
        tabWidget.addTab(propertyWidget, "Property")
        isotopeWidget = QWidget()
        isotopeLayout = QHBoxLayout()
        isotopeLayout.addWidget(self.isotopeTable)
        isotopeWidget.setLayout(isotopeLayout)
        tabWidget.addTab(isotopeWidget, "Isotope")

        grid = QGridLayout()
        grid.addWidget(topWidget, 0, 0)
        grid.addWidget(tabWidget, 1, 0)
        self.setLayout(grid)

        self.setWindowTitle(self.element.name)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    elements = element.ElementLibrary("PeriodicTableJSON.json")
    form = SingleWidget(elements[75])
    form.setWindowTitle("GridTest")
    form.show()
    app.exec_()