#!/usr/bin/env python3

'''
Basic element class
'''
import os
import json
import Nuclide

from PyQt5.QtCore import QFile, QIODevice

class Element(object):

    _element = 'n' ,\
              'H' ,  'He',  'Li',  'Be',  'B',\
              'C' ,   'N',   'O',   'F',  'Ne',\
              'Na',  'Mg',  'Al',  'Si',   'P',\
              'S' ,  'Cl',  'Ar',   'K',  'Ca',\
              'Sc',  'Ti',   'V',  'Cr',  'Mn',\
              'Fe',  'Co',  'Ni',  'Cu',  'Zn',\
              'Ga',  'Ge',  'As',  'Se',  'Br',\
              'Kr',  'Rb',  'Sr',   'Y',  'Zr',\
              'Nb',  'Mo',  'Tc',  'Ru',  'Rh',\
              'Pd',  'Ag',  'Cd',  'In',  'Sn',\
              'Sb',  'Te',   'I',  'Xe',  'Cs',\
              'Ba',  'La',  'Ce',  'Pr',  'Nd',\
              'Pm',  'Sm',  'Eu',  'Gd',  'Tb',\
              'Dy',  'Ho',  'Er',  'Tm',  'Yb',\
              'Lu',  'Hf',  'Ta',   'W',  'Re',\
              'Os',  'Ir',  'Pt',  'Au',  'Hg',\
              'Tl',  'Pb',  'Bi',  'Po',  'At',\
              'Rn',  'Fr',  'Ra',  'Ac',  'Th',\
              'Pa',   'U',  'Np',  'Pu',  'Am',\
              'Cm',  'Bk',  'Cf',  'Es',  'Fm',\
              'Md',  'No',  'Lr',  'Rf',  'Db',\
              'Sg',  'Bh',  'Hs',  'Mt',  'Ds',\
              'Rg',  'Cn', 'Uut',  'Fl', 'Uup',\
              'Lv', 'Uus', 'Uuo', 'Uue', 'Ubn'

    def __init__(self, Z, name=None, symbol=None):
        self.Z = Z
        self.name = name
        self.symbol = symbol
        self.isotopes = []

    def readInfoFromDict(self, data=None):
        if data is None:
            return
        for key in data.keys():
            if key == "name":
                self.name = data[key]
            elif key == "atomic_mass":
                self.atomicMass = data[key]
            elif key == "density":
                self.density = data[key]
            elif key == "melt":
                self.melt = data[key]
            elif key == "molar_heat":
                self.molarHeat = data[key]
            elif key == "number":
                self.number = data[key]
            elif key == "phase":
                self.phase = data[key]
            elif key == "xpos":
                self.xpos = data[key]
            elif key == "ypos":
                self.ypos = data[key]
            elif key == "shells":
                self.shells = data[key]
            elif key == "symbol":
                self.symbol = data[key]
            elif key == "summary":
                self.summary = data[key]
            elif key == "named_by":
                self.namedBy = data[key]
            elif key == "source":
                self.source = data[key]

    def pos(self):
        return self.xpos - 1, self.ypos


class ElementLibrary(object):
    """A ElementLibrary holds a set of Element objects.

    The elements are held in an order based on Z.
    The library should be made through this class's load() method.
    """

    def __init__(self, parent=None):
        self.elements = []

        fh = open('PeriodicTableJSON.json', 'r')
        data = json.load(fh)

        # Parse the JSON file
        list = data["elements"]
        # 遍历元素列表
        for item in list:
            # 处理每一个元素字典
            element = Element(item["number"])
            element.readInfoFromDict(item)
            self.elements.append(element)

    # 特殊方法：循环迭代时用到
    def __iter__(self):
        return iter(self.elements)

    # 特殊方法：返回第k个值
    def __getitem__(self, k):
        return self.elements[k]

    # 按照网格位置返回元素
    def getElement(self, xpos, ypos):
        for i in range(len(self.elements)):
            element = self.elements[i]
            if element.xpos == xpos and element.ypos == ypos:
                return element

    def getElementByZ(self, Z):
        for i in range(len(self.elements)):
            element = self.elements[i]
            if element.Z == Z:
                return element

    # --- 从核素库中获得同位素信息 ---
    def loadElementIsotopes(self, nuclides=Nuclide.NuclideLibrary):
        if nuclides is None:
            return
        for i, nuclide in enumerate(nuclides):
            element = self.getElementByZ(nuclide.Z)
            if element is not None:
                element.isotopes.append(nuclide)

