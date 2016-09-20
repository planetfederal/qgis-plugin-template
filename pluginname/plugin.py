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


    def unload(self):

        try:
            from .tests import testerplugin
            from qgistester.tests import removeTestModule
            removeTestModule(testerplugin, "[pluginname]")
        except:
            pass

    def initGui(self):
        pass
