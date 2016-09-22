# -*- coding: utf-8 -*-

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

    def initGui(self):
        icon = QIcon(os.path.dirname(__file__) + "[pluginshortname].png")
        self.action = QAction(icon, "[pluginname]", self.iface.mainWindow())
        self.action.setObjectName("start[pluginshortname]")
        self.action.triggered.connect(self.run)

        helpIcon = QgsApplication.getThemeIcon('/mActionHelpAPI.png')
        self.helpAction = QAction(helpIcon, "[pluginname] Help", self.iface.mainWindow())
        self.helpAction.setObjectName("[pluginshortname]Help")
        self.helpAction.triggered.connect(lambda: webbrowser.open_new(
                                          os.path.join(os.path.dirname(__file__), "docs", "html")))

    def run(self):
        pass

    def unload(self):

        try:
            from .tests import testerplugin
            from qgistester.tests import removeTestModule
            removeTestModule(testerplugin, "[pluginname]")
        except:
            pass

    def initGui(self):
        pass
