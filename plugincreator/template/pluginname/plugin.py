# -*- coding: utf-8 -*-

__author__ = '[authorname]'
__date__ = '[month] [year]'
__copyright__ = '(C) [year] [authorname]'

import os
import webbrowser

from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
[imports]

class [pluginclassname]:
    def __init__(self, iface):
        self.iface = iface
        [init]

    def initGui(self):
        [initgui]

    def unload(self):
        [unload]

    [methods]