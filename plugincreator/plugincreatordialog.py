import os
from qgis.utils import iface
from qgis.PyQt import uic
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QFileDialog
from qgis.PyQt.QtWidgets import QSizePolicy
from qgis.gui import QgsMessageBar
from qgis.core import Qgis 

from .selecttagsdialog import SelectTagsDialog

pluginPath = os.path.dirname(__file__)
WIDGET, BASE = uic.loadUiType(os.path.join(pluginPath, 'plugincreatordialog.ui'))

class WrongTextValueException(Exception):
    
    def __init__(self, widget, tab):
        super(WrongTextValueException, self).__init__("")
        self.widget = widget
        self.tab = tab
        self.errormessage = "Wrong or missing parameter value"

class WrongNumValueException(Exception):

    def __init__(self, widget, tab):
        super(WrongNumValueException, self).__init__("")
        self.widget = widget
        self.tab = tab
        self.errormessage = "Version numbers must be numeric"


class PluginCreatorDialog(BASE, WIDGET):

    def __init__(self, parent=None):
        parent = parent or iface.mainWindow()
        super(PluginCreatorDialog, self).__init__(parent)
        self.setupUi(self)
        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout().insertWidget(0, self.bar)
        self.pluginInfo = None
        self.outputFolder = None
        self.btnFolder.clicked.connect(self.selectFolder)
        self.btnTags.clicked.connect(self.selectTags)
        self.buttonBox.accepted.connect(self.okPressed)
        self.buttonBox.rejected.connect(self.cancelPressed)
        self.chkQgisCommons.stateChanged.connect(self.qgiscommonsChanged)

    def qgiscommonsChanged(self, state):
        state = state == Qt.Checked
        self.chkSettings.setEnabled(state)
        self.chkHelp.setEnabled(state)
        self.chkAbout.setEnabled(state)

    def selectTags(self):
        dialog = SelectTagsDialog(self)
        ok = dialog.exec_()
        if ok:
            selected = dialog.listView.selectedIndexes()
            seltags = []
            for tag in selected:
                seltags.append(tag.data())
            taglist = ", ".join(seltags)
            self.txtTags.setText(taglist)

    def selectFolder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Select output folder')
        if folder:
            self.txtFolder.setText(folder)

    def _getTextValue(self, widget, tab):
        text = widget.text().strip()
        if text == "":
            raise WrongTextValueException(widget, tab)
        widget.setStyleSheet("QLineEdit{background: white}")
        return text

    def _getNumValue(self, widget, tab):
        value = self._getTextValue(widget, tab)
        try:
            num = float(value)
        except:
            raise WrongNumValueException(widget, tab)
        widget.setStyleSheet("QLineEdit{background: white}")
        return widget.text()

    def okPressed(self):
        self.pluginInfo = {}
        try:
            self.pluginInfo["pluginName"] = self._getTextValue(self.txtName, 0)
            self.pluginInfo["description"] = self._getTextValue(self.txtDescription, 0)
            self.pluginInfo["about"] = self.txtAbout.toPlainText()
            self.pluginInfo["author"] = self._getTextValue(self.txtAuthor, 0)
            self.pluginInfo["email"] = self._getTextValue(self.txtEmail, 0)
            self.pluginInfo["minVersion"] = self._getNumValue(self.txtQgisVersion, 0)
            self.pluginInfo["version"] = self._getNumValue(self.txtVersion, 0)
            self.pluginInfo["homepage"] = self.txtHomepage.text()
            self.pluginInfo["tracker"] = self._getTextValue(self.txtTracker, 2)
            self.pluginInfo["repository"] = self._getTextValue(self.txtRepository, 2)
            self.pluginInfo["tags"] = self.txtTags.text()
            self.pluginInfo["experimental"] = self.chkExperimental.isChecked()
            self.pluginInfo["addTests"] = self.chkTests.isChecked()
            self.pluginInfo["addLessons"] = self.chkLessons.isChecked()
            self.pluginInfo["addTravis"] = self.chkTravis.isChecked()
            self.pluginInfo["addDocs"] = self.chkDocs.isChecked()
            qgiscommons = self.chkQgisCommons.isChecked()
            self.pluginInfo["addQgisCommons"] = qgiscommons
            self.pluginInfo["addSettings"] = self.chkSettings.isChecked() and qgiscommons
            self.pluginInfo["addAbout"] = self.chkAbout.isChecked() and qgiscommons
            self.pluginInfo["addHelp"] = self.chkHelp.isChecked() and qgiscommons
        except WrongTextValueException as e:
            self.pluginInfo = None
            self._showError(e)
            return
        except WrongTextValueException as e:
            self.pluginInfo = None
            self._showError(e)
            return
        self.outputFolder = self.txtFolder.text()
        self.close()

    def _showError(self, e):
        e.widget.setStyleSheet("QLineEdit{background: yellow}")
        self.tabWidget.setCurrentIndex(e.tab)
        self.bar.pushMessage("", e.errormessage, level=Qgis.Warning, duration=5)

    def cancelPressed(self):
        self.pluginInfo = None
        self.close()
