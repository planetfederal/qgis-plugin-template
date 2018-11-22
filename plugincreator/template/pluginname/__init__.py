# -*- coding: utf-8 -*-

__author__ = '[authorname]'
__date__ = '[month] [year]'
__copyright__ = '(C) [year] [authorname]'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

def classFactory(iface):
    from .plugin import [pluginclassname]
    return [pluginclassname](iface)

