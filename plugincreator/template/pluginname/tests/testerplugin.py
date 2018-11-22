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
    sampleTest.addStep("Sample step", sampleMethod)

    return [sampleTest]


class [pluginclassname]Test(unittest.TestCase):

    def testSampleTest(self):
        pass


def pluginSuite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite([pluginclassname]Test, 'test'))
    return suite

def unitTests():
    _tests = []
    _tests.extend(pluginSuite())
    return _tests

# run all tests, this function is automatically called by the travis CI
# from the qgis-testing-environment-docker system
def run_all():
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(pluginSuite())
