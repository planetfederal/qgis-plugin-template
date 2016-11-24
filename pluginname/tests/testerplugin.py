# Tests for the QGIS Tester plugin. To know more see
# https://github.com/boundlessgeo/qgis-tester-plugin

import os
import unittest

try:
    from qgistester.test import Test
    from qgistester.utils import layerFromName
except:
    pass

def functionalTests():
    try:
        from qgistester.test import Test
        from qgistester.utils import layerFromName
    except:
        return []

    def sampleMethod(self):
        pass

    sampleTest = Test("Sample test")
    sampleTest.addStep("Sample step", _sampleMethod)

    return [sampleTest]


class [pluginclassname]Test(unittest.TestCase):

    def testSampleTest(self):
        pass


def pluginSuite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(MilStd2525Test, 'test'))
    return suite

def unitTests():
    _tests = []
    _tests.extend(pluginSuite())
    return _tests
