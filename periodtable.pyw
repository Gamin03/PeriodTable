#!/usr/bin/env python3
# Copyright (c) 2018-01 Jimin Ma. All rights reserved.

import platform
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import element
import gridwidget
import meshwidget
import Nuclide

__version__ = "0.1.0"


class MainForm(QDialog):

    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        self.ebutton = QRadioButton("Elements")
        self.ebutton.setChecked(True)
        self.ebutton.toggled.connect(lambda : self.buttonstate(self.ebutton))
        self.nbutton = QRadioButton("Nuclides")
        self.nbutton.toggled.connect(lambda : self.buttonstate(self.nbutton))

        msgbutton = QPushButton()
        msgbutton.setText("About...")
        msgbutton.clicked.connect(self.showAbout)

        self.elements = element.ElementLibrary("PeriodicTableJSON.json")
        self.nuclides = Nuclide.NuclideLibrary()
        self.elements.loadElementIsotopes(self.nuclides)

        self.mainWidget = QStackedWidget()
        self.mainWidget.addWidget(gridwidget.GridWidget(self.elements))
        self.mainWidget.addWidget(meshwidget.MeshWidget(self.nuclides))

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.ebutton)
        buttonLayout.addWidget(self.nbutton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(msgbutton)
        widget = QWidget()
        widget.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(192, 253, 123))
        widget.setPalette(palette)
        widget.setLayout(buttonLayout)

        layout = QVBoxLayout()
        layout.addWidget(widget)
        layout.addWidget(self.mainWidget)
        self.setLayout(layout)

    def buttonstate(self, b):
        if b.text() == "Elements":
            if b.isChecked() == True:
                self.mainWidget.setCurrentIndex(0)
        if b.text() == "Nuclides":
            if b.isChecked() == True:
                self.mainWidget.setCurrentIndex(1)

    def showAbout(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setInformativeText("""<b>Elements and Nuclides Table</b>  version {0}
                    <p>Copyright &copy; 2018-Now <i>Jimin Ma</i>
                    <p> E-mail: <a href="mailto:majm03@foxmail.com">majm03@foxmail.com</a>. 
                    All rights reserved.
                    <p>This application can be used to view information about
                    elements and nuclides.
                    <p> Elements information source: 
                        <a href="https://en.wikipedia.org/wiki/Chemical_element/">Wikipedia/Chemical_element</a>.
                    <p> Nuclides information source: 
                        Audi, G. et al. (2012), "The Nubase2012 evaluation of nuclear properties",
                        Chinese Physics C, Vol. 36, No. 12, 1157-1286.
                        <a href="http://iopscience.iop.org/article/10.1088/1674-1137/36/12/001/meta">Nubase2012</a>.
                    <p>Python {1} - Qt {2} - PyQt {3} on {4}""".format(
                    __version__, platform.python_version(),
                    QT_VERSION_STR, PYQT_VERSION_STR,
                    platform.system()))
        msg.setIcon(QMessageBox.Information)
        msg.exec_()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setApplicationName("Periodic Table")
    form = MainForm()
    form.show()
    app.exec_()