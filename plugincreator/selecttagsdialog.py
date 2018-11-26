# coding=utf-8

import os

from qgis.PyQt import QtGui, QtWidgets, uic

WIDGET, BASE = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'selecttagsdialog.ui'))


class SelectTagsDialog(BASE, WIDGET):
    def __init__(self, parent=None):
        super(SelectTagsDialog, self).__init__(parent)
        self.setupUi(self)
        tagFile = os.path.join(os.path.dirname(__file__), 'taglist.txt')

        with open(tagFile) as tf:
            tags = tf.readlines()

        model = QtGui.QStandardItemModel()

        for tag in tags:
            item = QtGui.QStandardItem(tag[:-1])
            model.appendRow(item)

        self.listView.setModel(model)
