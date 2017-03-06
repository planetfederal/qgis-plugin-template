# -*- coding: utf-8 -*-

"""
***************************************************************************
    __init__.py
    ---------------------
    Date                 : [month] [year]
    Copyright            : (C) [year] Boundless, http://boundlessgeo.com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = '[authorname]'
__date__ = '[month] [year]'
__copyright__ = '(C) [year] Boundless, http://boundlessgeo.com'

# This will get replaced with a git SHA1 when you do a git archive

import os
import webbrowser

from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from qgis.core import QgsApplication

from .qgiscommons.settings import open_settings_dialog, read_settings

class [pluginclassname]:
    def __init__(self, iface):
        self.iface = iface
        try:
            from .tests import testerplugin
            from qgistester.tests import addTestModule
            addTestModule(testerplugin, "[pluginname]")
        except:
            pass

        try:
            from lessons import addLessonsFolder
            folder = os.path.join(os.path.dirname(__file__), "_lessons")
            addLessonsFolder(folder)
        except:
            pass

        read_settings()

    def initGui(self):
        icon = QIcon(os.path.dirname(__file__) + "[pluginshortname].png")
        self.action = QAction(icon, "[pluginname]", self.iface.mainWindow())
        self.action.setObjectName("start[pluginshortname]")
        self.action.triggered.connect(self.run)
        self.iface.addPluginToMenu("[pluginname]", self.action)

        helpIcon = QgsApplication.getThemeIcon('/mActionHelpAPI.png')
        self.helpAction = QAction(helpIcon, "[pluginname] Help", self.iface.mainWindow())
        self.helpAction.setObjectName("[pluginshortname]Help")
        self.helpAction.triggered.connect(lambda: webbrowser.open_new(
                        "file://" + os.path.join(os.path.dirname(__file__), "docs", "html", "index.html")))
        self.iface.addPluginToMenu("[pluginname]", self.helpAction)

        settingsIcon = QgsApplication.getThemeIcon('/mActionHelpAPI.png')
        self.settingsAction = QAction(helpIcon, "[pluginname] Settings", self.iface.mainWindow())
        self.settingsAction.setObjectName("[pluginshortname]Settings")
        self.settingsAction.triggered.connect(open_settings_dialog)
        self.iface.addPluginToMenu("[pluginname]", self.settingsAction)

    def unload(self):
        try:
            from .tests import testerplugin
            from qgistester.tests import removeTestModule
            removeTestModule(testerplugin, "[pluginname]")
        except:
            pass

    def run(self):
        pass
