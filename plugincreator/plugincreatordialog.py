import os
from qgis.utils import iface
from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QFileDialog

pluginPath = os.path.dirname(__file__)
WIDGET, BASE = uic.loadUiType(os.path.join(pluginPath, 'plugincreatordialog.ui'))

class WrongTextValueException(Exception):
    pass


class PluginCreatorDialog(BASE, WIDGET):

    def __init__(self, parent=None):
        parent = parent or iface.mainWindow()
        super(PluginCreatorDialog, self).__init__(parent)
        self.setupUi(self)
        self.pluginInfo = None
        self.outputFolder = None
        self.btnFolder.clicked.connect(self.selectFolder)
        self.buttonBox.accepted.connect(self.okPressed)
        self.buttonBox.rejected.connect(self.cancelPressed)

    def selectFolder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Select output folder')
        if folder:
            self.txtFolder.setText(folder)

    def _getTextValue(self, widget):
        return widget.text()

    def _getNumValue(self, widget):
        return widget.text()

    def okPressed(self):
        self.pluginInfo = {}
        try:
            self.pluginInfo["pluginName"] = self._getTextValue(self.txtName) or "My New Plugin"
            self.pluginInfo["description"] = self._getTextValue(self.txtDescription) or "bla"
            self.pluginInfo["about"] = self.txtAbout.toPlainText() or "blabla"
            self.pluginInfo["author"] = self._getTextValue(self.txtAuthor) or "victor"
            self.pluginInfo["email"] = self._getTextValue(self.txtEmail) or "volaya@bla.com"
            self.pluginInfo["minVersion"] = self._getNumValue(self.txtQgisVersion)
            self.pluginInfo["version"] = self._getNumValue(self.txtVersion)
            self.pluginInfo["homepage"] = self._getTextValue(self.txtHomepage)
            self.pluginInfo["tracker"] = self._getTextValue(self.txtTracker)
            self.pluginInfo["repository"] = self._getTextValue(self.txtRepository)
            self.pluginInfo["tags"] = self._getTextValue(self.txtTags)
            self.pluginInfo["experimental"] = self.chkExperimental.isChecked()
            self.pluginInfo["addTests"] = self.chkTests.isChecked()
            self.pluginInfo["addLessons"] = self.chkLessons.isChecked()
            self.pluginInfo["addTravis"] = self.chkTravis.isChecked()
            self.pluginInfo["addDocs"] = self.chkDocs.isChecked()
            qgiscommons = self.chkQgisCommons.isChecked()
            self.pluginInfo["addQgisCommons"] = qgiscommons
            if qgiscommons:
                self.pluginInfo["addSettings"] = self.chkSettings.isChecked()
                self.pluginInfo["addAbout"] = self.chkAbout.isChecked()
                self.pluginInfo["addHelp"] = self.chkHelp.isChecked()
        except WrongTextValueException as e:
            self.pluginInfo = None
            return
        self.outputFolder = self.txtFolder.text()
        self.close()

    def cancelPressed(self):
        self.pluginInfo = None
        self.close()
