[pluginname]
==================

[Write your plugin description here]

Installation
************

To install the latest version of the plugin:

- Clone this repository or download and unzip the latest code of the plugin

- If you do not have paver (https://github.com/paver/paver) installed, install it by typing the following in a console:

::

	pip install paver
	
- Open a console in the folder created in the first step, and type

::

	paver setup

This will get all the dependencies needed by the plugin.

- Install into QGIS by running

::

	paver install

That will copy the code into your QGIS user plugin folder, or create a symlink in it, depending on your OS

To package the plugin, run

::

	paver package

Documentation will be built in the `docs` folder and added to the resulting zip file. It includes dependencies as well, but it will not download them, so the `setup` task has to be run before packaging.

Usage
*****

Usage is documented `here <./docs/source/usage.rst>`_