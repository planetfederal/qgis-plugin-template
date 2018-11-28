import os
from qgis.utils import iface
from qgis.PyQt import uic
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QCursor, QPixmap
from qgis.PyQt.QtWidgets import QFileDialog, QListWidgetItem, QSizePolicy, QApplication
from qgis.gui import QgsMessageBar
from qgis.core import Qgis 
from plugincreator.plugincreator import createPlugin

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

PLUGIN, DATABASE, RASTER, VECTOR, WEB = range(5)

class MenuItem(QListWidgetItem):

    def __init__(self, name, parent, icon):
        super(MenuItem, self).__init__(name)
        self.name = name
        self.parent = parent
        self.icon = icon

    def updateInfo(self, name, parent, icon):
        self.name = name
        self.parent = parent
        self.setText(name)
        self.icon = icon

class PluginCreatorDialog(BASE, WIDGET):

    def __init__(self, parent=None):
        parent = parent or iface.mainWindow()
        super(PluginCreatorDialog, self).__init__(parent)
        self.setupUi(self)
        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout().insertWidget(0, self.bar)
        self.outputFolder = None
        self.btnFolder.clicked.connect(self.selectFolder)
        self.btnTags.clicked.connect(self.selectTags)
        self.buttonBox.accepted.connect(self.okPressed)
        self.buttonBox.rejected.connect(self.cancelPressed)
        self.chkQgisCommons.stateChanged.connect(self.qgiscommonsChanged)
        self.btnAddMenu.clicked.connect(self.addMenuClicked)
        self.btnRemoveMenu.clicked.connect(self.removeMenuClicked)
        self.listMenus.currentItemChanged.connect(self.listItemChanged)
        self.btnSelectIcon.clicked.connect(self.selectIcon)
        self.labelIcon.iconPath = None

    def listItemChanged(self, current, previous):
        if current:
            self.txtMenuTitle.setText(current.name)
            self.comboParentMenu.setCurrentIndex(current.parent)
            if current.icon:
                self.labelIcon.setText("")
                pixmap = QPixmap(current.icon)
                self.labelIcon.setPixmap(pixmap)
            else:
                self.labelIcon.setText("[No Icon]")
                self.labelIcon.setPixmap(None)            
        else:
            self.labelIcon.setText("[No Icon]")
            self.labelIcon.setPixmap(None)            
            self.txtMenuTitle.setText("")
            self.comboParentMenu.setCurrentIndex(0)

    def addMenuClicked(self):
        itemToUpdate = None
        name = self.txtMenuTitle.text()
        for i in range(self.listMenus.count()):
            item = self.listMenus.item(i)
            if item.name == name:
                itemToUpdate = item
                break
        if itemToUpdate:
            itemToUpdate.updateInfo(name, self.comboParentMenu.currentIndex(), self.labelIcon.iconPath)
        else:
            newItem = MenuItem(name, self.comboParentMenu.currentIndex(), self.labelIcon.iconPath)      
            self.listMenus.addItem(newItem)

    def removeMenuClicked(self):        
        self.listMenus.takeItem(self.listMenus.currentRow())
        self.txtMenuTitle.setText("")
        self.comboParentMenu.setCurrentIndex(0)

    def qgiscommonsChanged(self, state):
        state = state == Qt.Checked
        self.chkSettings.setEnabled(state)
        self.chkHelp.setEnabled(state)
        self.chkAbout.setEnabled(state)

    def selectIcon(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Icon", os.path.join(os.path.dirname(__file__), "icons"))
        if filename:
            pixmap = QPixmap(filename)
            self.labelIcon.setText("")
            self.labelIcon.setPixmap(pixmap)            
            self.labelIcon.iconPath = filename

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
        pluginInfo = {}
        try:
            pluginInfo["pluginName"] = self._getTextValue(self.txtName, 0)
            pluginInfo["description"] = self._getTextValue(self.txtDescription, 0)
            pluginInfo["about"] = self.txtAbout.toPlainText()
            pluginInfo["author"] = self._getTextValue(self.txtAuthor, 0)
            pluginInfo["email"] = self._getTextValue(self.txtEmail, 0)
            pluginInfo["minVersion"] = self._getNumValue(self.txtQgisVersion, 0)
            pluginInfo["version"] = self._getNumValue(self.txtVersion, 0)
            pluginInfo["homepage"] = self.txtHomepage.text()
            pluginInfo["tracker"] = self._getTextValue(self.txtTracker, 3)
            pluginInfo["repository"] = self._getTextValue(self.txtRepository, 3)
            pluginInfo["tags"] = self.txtTags.text()
            pluginInfo["experimental"] = self.chkExperimental.isChecked()
            pluginInfo["addTests"] = self.chkTests.isChecked()
            pluginInfo["addLessons"] = self.chkLessons.isChecked()
            pluginInfo["addTravis"] = self.chkTravis.isChecked()
            pluginInfo["addDocs"] = self.chkDocs.isChecked()
            pluginInfo["addDialog"] = self.chkSampleDialog.isChecked()
            qgiscommons = self.chkQgisCommons.isChecked()
            pluginInfo["addQgisCommons"] = qgiscommons
            pluginInfo["addSettings"] = self.chkSettings.isChecked() and qgiscommons
            pluginInfo["addAbout"] = self.chkAbout.isChecked() and qgiscommons
            pluginInfo["addHelp"] = self.chkHelp.isChecked() and qgiscommons
            menus = {}
            for i in range(self.listMenus.count()):
                item = self.listMenus.item(i)
                menus[item.name] = (item.parent, item.icon)
            pluginInfo["menus"] = menus
        except WrongTextValueException as e:
            pluginInfo = None
            self._showError(e)
            return
        except WrongTextValueException as e:
            pluginInfo = None
            self._showError(e)
            return
        outputFolder = self.txtFolder.text()
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            createPlugin(pluginInfo, outputFolder)
        finally:
            QApplication.restoreOverrideCursor()

        self.close()

    def _showError(self, e):
        e.widget.setStyleSheet("QLineEdit{background: yellow}")
        self.tabWidget.setCurrentIndex(e.tab)
        self.bar.pushMessage("", e.errormessage, level=Qgis.Warning, duration=5)

    def cancelPressed(self):
        self.close()
