# -*- coding: utf-8 -*-

import os
import shutil
import datetime
import subprocess
from sys import argv
import zipfile
import StringIO
import requests

def prompt(message, validate):
    res = None
    while res is None:
        res = raw_input(message)
        if not validate(res):
            print 'Invalid value!'
            res = None
    return res.strip()


def removeInvalidChars(s):
    validChars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    s = ''.join(c for c in s if c in validChars)
    return s

def className(s):
    return removeInvalidChars(s.title())


def replaceInFiles(filename, toReplace):
    with open(filename) as f :
        text = f.read()

    for before, after in toReplace:
        text = text.replace(before, after)

    with open(filename, 'w') as f:
         f.write(text)


def main():
    pluginName = prompt('Plugin name: ', lambda v : bool(v.strip()))
    defaultShortName = removeInvalidChars(pluginName).lower()
    pluginShortName = (prompt("Plugin short name (no blank spaces allowed) [Leave empty to use '%s']: "
                            % defaultShortName, lambda s: s == removeInvalidChars(s)) or defaultShortName)
    defaultClassName = className(pluginName)
    pluginClassName = (prompt("Plugin class name [Leave empty to use '%s']: " % defaultClassName,
                            lambda s: s == removeInvalidChars(s)) or defaultClassName)

    addCommons = prompt("Add commons library?[Y/n]:", lambda s: s.lower() in ["y", "n", ""]).lower() in ["y", ""]
    addBoundlessCommons = prompt("Add Boundless commons library?[Y/n]:", lambda s: s.lower() in ["y", "n", ""]).lower() in ["y", ""]

    authorName = prompt('Plugin author: ', lambda v : bool(v.strip()))
    d = datetime.date.today()
    year = str(d.year)
    month = d.strftime('%B')

    if addCommons:
        commons = '''
    tmpCommonsPath = path(__file__).dirname() / "qgiscommons"
    dst = ext_libs / "qgiscommons"
    if dst.exists():
        dst.rmtree()
    r = requests.get("https://github.com/boundlessgeo/lib-qgis-commons/archive/master.zip", stream=True)
    z = zipfile.ZipFile(StringIO.StringIO(r.content))
    z.extractall(path=tmpCommonsPath.abspath())
    src = tmpCommonsPath / "lib-qgis-commons-master" / "qgiscommons"
    src.copytree(dst.abspath())
    tmpCommonsPath.rmtree()
    '''
    else:
        commons = ""

    if addBoundlessCommons:
        boundlessCommons = '''
    tmpCommonsPath = path(__file__).dirname() / "boundlesscommons"
    dst = ext_libs / "boundlesscommons"
    if dst.exists():
        dst.rmtree()
    r = requests.get("https://github.com/boundlessgeo/lib-qgis-boundless-commons/archive/master.zip", stream=True)
    z = zipfile.ZipFile(StringIO.StringIO(r.content))
    z.extractall(path=tmpCommonsPath.abspath())
    src = tmpCommonsPath / "lib-qgis-boundless-commons-master" / "boundlesscommons"
    src.copytree(dst.abspath())
    tmpCommonsPath.rmtree()
    '''
    else:
        boundlessCommons = ""


    toReplace = [('[pluginname]', pluginName),
                 ('[pluginshortname]', pluginShortName),
                 ('[pluginclassname]', pluginClassName),
                 ('[month]', month),
                 ('[year]', year),
                 ('[authorname]', authorName),
                 ('[commons]', commons),
                 ('[boundlessCommons]', boundlessCommons),
                ]

    folder = os.path.dirname(os.path.realpath(__file__))
    gitFolder = os.path.join(folder, '.git')
    subprocess.call('git submodule init'.split(' '))
    subprocess.call('git submodule update'.split(' '))
    if os.path.exists(gitFolder):
        try:
            shutil.rmtree(gitFolder)
        except:
            pass

        for root, dirs, files in os.walk(folder):
            for f in files:
                if '.git' not in root:
                    replaceInFiles(os.path.join(root, f), toReplace)

        os.rename(os.path.join(folder, 'pluginname'), os.path.join(folder, pluginShortName))
        os.rename(os.path.join(folder, '_readme.rst'), os.path.join(folder, "README.rst"))

        os.remove(argv[0])
        os.remove(os.path.join(folder, 'console.png'))
        os.remove(os.path.join(folder, 'README.md'))

if __name__ == '__main__':
    main()
