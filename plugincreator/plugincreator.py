# -*- coding: utf-8 -*-

import os
import shutil
import datetime
from qgis.core import Qgis
from qgis.utils import iface

def removeInvalidChars(s):
    validChars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    s = ''.join(c for c in s if c in validChars)
    return s

def className(s):
    return ''.join(removeInvalidChars(x).capitalize() for x in s.split(' '))

def replaceInFiles(filename, toReplace):
    with open(filename) as f:
        try:
            text = f.read()
        except:
            return

    for before, after in toReplace:
        text = text.replace(before, after)

    with open(filename, 'w') as f:
         f.write(text)

def createPlugin(pluginInfo, destFolder):
    pluginName = pluginInfo["pluginName"]
    pluginModuleName = removeInvalidChars(pluginName).lower()
    pluginClassName = className(pluginName)

    d = datetime.date.today()
    year = str(d.year)
    month = d.strftime('%B')

    initGui = ""
    init = ""
    unload = ""
    imports = ""

    templateFolder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "template")
    destFolder = os.path.join(destFolder, pluginModuleName)
    if os.path.exists(destFolder):
        shutil.rmtree(destFolder)
    shutil.copytree(templateFolder, destFolder)
    os.rename(os.path.join(destFolder, 'pluginname'), os.path.join(destFolder, pluginModuleName))
    if pluginInfo["addDialog"]:
        os.rename(os.path.join(destFolder, pluginModuleName, 'ui', 'plugindialog.ui'), 
                os.path.join(destFolder, pluginModuleName,'ui', '%sdialog.ui' % pluginModuleName))
        os.rename(os.path.join(destFolder, pluginModuleName, 'ui', 'plugindialog.py'), 
                os.path.join(destFolder,  pluginModuleName, 'ui', '%sdialog.py' % pluginModuleName))
    else:
        os.remove(os.path.join(destFolder, pluginModuleName, 'ui', 'plugindialog.ui'))
        os.remove(os.path.join(destFolder, pluginModuleName, 'ui', 'plugindialog.py'))

    if pluginInfo["addTests"]:
        init += '''
        try:
            from .tests import testerplugin
            from qgistester.tests import addTestModule
            addTestModule(testerplugin, "%s")
        except:
            pass
        ''' % pluginName
        unload += '''
        try:
            from .tests import testerplugin
            from qgistester.tests import removeTestModule
            removeTestModule(testerplugin, "%s")
        except:
            pass
        ''' % pluginName
    else:
        shutil.rmtree(os.path.join(destFolder, pluginModuleName, "tests"))

    if pluginInfo["addLessons"]:
        initGui += '''
        try:
            from lessons import addLessonsFolder
            folder = os.path.join(os.path.dirname(__file__), "_lessons")
            addLessonsFolder(folder, "%s")
        except:
            pass
        ''' % pluginName
        unload += '''
        try:
            from lessons import removeLessonsFolder
            folder = os.path.join(os.path.dirname(__file__), "_lessons")
            removeLessonsFolder(folder)
        except:
            pass
        '''
    else:
        shutil.rmtree(os.path.join(destFolder, pluginModuleName, "_lessons"))

    if not pluginInfo["addTravis"]:
        os.remove(os.path.join(destFolder, pluginModuleName, ".travis.yml"))

    if not pluginInfo["addDocs"]:
        os.remove(os.path.join(destFolder, pluginModuleName, ".travis.yml"))

    if pluginInfo["addSettings"]:
        initGui += '''
        addSettingsMenu("%s")
        ''' % pluginModuleName
        unload += '''
        removeSettingsMenu("%s")
        ''' % pluginModuleName
    if pluginInfo["addHelp"]:
        initGui += '''
        addHelpMenu("%s")
        ''' % pluginModuleName
        unload += '''
        removeHelpMenu("%s")
        ''' % pluginModuleName
    if pluginInfo["addAbout"]:
        initGui += '''
        addAboutMenu("%s")
        ''' % pluginModuleName
        unload += '''
        removeAboveMenu("%s")
        ''' % pluginModuleName

    methods = ""
    functionNames = ["Menu", "DatabaseMenu", "RasterMenu", "VectorMenu", "WebMenu"]
    for menuName, menuData in pluginInfo["menus"].items():
        menuParent, menuIcon = menuData
        destIconFile = os.path.join(destFolder, pluginModuleName, "icons", os.path.basename(menuIcon))
        shutil.copyfile(menuIcon, destIconFile)
        menuCodeName = className(menuName)
        replace = {"menuname": menuName, "menucodename": menuCodeName,
                    "pluginname": pluginName, "funcname": functionNames[menuParent],
                    "iconname": os.path.basename(menuIcon)}
        initGui += '''
        icon%(menucodename)s = QIcon(os.path.join(os.path.dirname(__file__), "icons", "%(iconname)s"))
        self.action%(menucodename)s = QAction(icon%(menucodename)s, "%(menuname)s", self.iface.mainWindow())
        self.action%(menucodename)s.setObjectName("start%(menucodename)s")
        self.action%(menucodename)s.triggered.connect(self.%(menucodename)sClicked)
        self.iface.addPluginTo%(funcname)s("%(pluginname)s", self.action%(menucodename)s)
        ''' % replace
        unload += '''        
        self.iface.removePluginFrom%(funcname)s("%(pluginname)s", self.action%(menucodename)s)
        ''' % replace
        methods += '''
    def %(menucodename)sClicked(self):
        pass
        ''' % replace

    imports = ""
    qgiscommons = ""
    if pluginInfo["addQgisCommons"]:
        imports = '''
from .extlibs.qgiscommons2.settings import readSettings
from .extlibs.qgiscommons2.gui.settings import addSettingsMenu, removeSettingsMenu
from .extlibs.qgiscommons2.gui import addAboutMenu, removeAboutMenu, addHelpMenu, removeHelpMenu
        '''
        init += '''
        readSettings()
        '''
        qgiscommons = "qgiscommons"

    toReplace = [('[pluginname]', pluginName),
                 ('[pluginmodulename]', pluginModuleName),
                 ('[pluginclassname]', pluginClassName),
                 ('[month]', month),
                 ('[year]', year),
                 ('[authorname]', pluginInfo["author"]),
                 ('[email]', pluginInfo["email"]),
                 ('[initgui]', initGui),
                 ('[unload]', unload),
                 ('[init]', init),
                 ('[imports]', imports),
                 ('[methods]', methods),
                 ('[qgiscommons]', qgiscommons),
                 ('[version]', pluginInfo["version"]),
                 ('[minversion]', pluginInfo["minVersion"]),
                 ('[repository]', pluginInfo["repository"]),
                 ('[tracker]', pluginInfo["tracker"]),
                 ('[homepage]', pluginInfo["homepage"]),
                 ('[experimental]', str(pluginInfo["experimental"])),
                ]

    for root, dirs, files in os.walk(destFolder):
        for f in files:
            replaceInFiles(os.path.join(root, f), toReplace)

    iface.messageBar().pushMessage("Plugin Creator", "Plugin skeleton has been correctly created", 
                                    level=Qgis.Success, duration=5)