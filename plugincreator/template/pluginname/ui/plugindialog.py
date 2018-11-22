import os
from qgis.PyQt import uic
 
WIDGET, BASE = uic.loadUiType(os.path.join(os.path.dirname(__file__), '[pluginmodulename]dialog.ui'))

class [pluginclassname]Dialog(BASE, WIDGET):

    def __init__(self, parent=None):
        super([pluginclassname]Dialog, self).__init__(parent)
        self.setupUi(self)

