# -*- coding: utf-8 -*-

__author__ = '[authorname]'
__date__ = '[month] [year]'
__copyright__ = '(C) [year] [authorname]'

import os
import webbrowser

from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from .ui.[pluginmodulename]dialog import [pluginclassname]Dialog

from .extlibs.qgiscommons2.settings import readSettings
from .extlibs.qgiscommons2.gui.settings import addSettingsMenu, removeSettingsMenu
from .extlibs.qgiscommons2.gui import addAboutMenu, removeAboutMenu, addHelpMenu, removeHelpMenu

class [pluginclassname]:
    def __init__(self, iface):
        self.iface = iface
        [init]
        readSettings()

    def initGui(self):
        icon = QIcon(os.path.dirname(__file__) + "/icons/qgis.png")
        self.action = QAction(icon, "[pluginname]", self.iface.mainWindow())
        self.action.setObjectName("start[pluginmodulename]")
        self.action.triggered.connect(self.run)
        self.iface.addPluginToMenu("[pluginname]", self.action)
        [initgui]

    def unload(self):
        self.iface.removePluginMenu("[pluginname]", self.action)
        [unload]

    def run(self):
        dialog = [pluginclassname]Dialog()
        dialog.exec_()
