# -*- coding: utf-8 -*-

import os
import site

site.addsitedir(os.path.abspath(os.path.dirname(__file__) + '/ext-libs'))

def classFactory(iface):
    from plugin import [pluginclassname]
    return [pluginclassname](iface)

