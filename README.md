# QGIS Plugin Creator

A simple plugin that provides a UI to create the skeleton of a functional plugin.

Largely based on Gary Sherman's PluginBuilder plugin.

## How to use it

Click on the "Plugins/Plugin Creator/Create plugin skeleton" menu to open the plugin dialog.

Enter the destination folder where you want to plugin folder to be created.

Enter the required information in the dialog widgets and click OK to generate the plugin.

Here is an explanation of each element in the UI.

* "General" tab

	* Plugin name: The name of the plugin. Class names and module names will be derived from it

	* Short description: A one-line description of the plugin.

	* Detailed description: A longer description of the plugin.

	* Version number: The version of the plugin.

	* Minimum QGIS version: The minimum QGIS version needed to run the plugin. Notice that the template includes QGIS3-compatible code, so the minimum version has to be greater or equal to 3.0. 

	* Author: The author of the plugin.

	* Email. The email of the author.


* "Options" tab

	* Sphinx documentation project: If checked, a `docs` folder with a Sphinx project will be added to the plugin folder. Edit the `docs/source/index.rst` file to add content. By default, it contains a single input file, `intro.rst`, which is empty.

	* "Lessons for Lessons plugin". If checked, a `_lessons` folder will be added to the plugin folder, with the required structure to add lessons for the [Lessons plugin](https://github.com/boundlessgeo/qgis-lessons-plugin). A single sample lesson is added in a folder named `samplelesson`. Use that as a template to add more lessons. Lessons will be automatically added when the plugin is loaded, since the necessary code is also added to the plugin class constructor.

	* "Tests for Tester plugin". If checked, a `tests` folder will be added to the plugin folder, with the required structure to add tests for the [Tester plugin](https://github.com/boundlessgeo/qgis-tester-plugin). A `testerplugin.py` file is added, which contains sample unit and semi-automated tests, to use as a starting point. Tests added to that file will be automatically added to the Tester plugin when the plugin is loaded, since the necessary code is also added to the plugin class constructor.

		A folder with sample data is included in the `tests` folder, to be used for testing your plugin.

	* "Travis files for Travis CI integration". If checked, a `travis.yml` file will be added for Travis CI integration. It will define a travis task that runs the unit tests that are added in case the "Tests for Tester plugin" option has been checked.

	* "Sample dialog files". If checked, it adds a sample dialog tat can be used in the plugin. A `.ui` file is included, which contains the design of the dialog. A `.py` file is included as well, containing the logic of the dialog. The dialog class is not called from anywhere in the plugin skeleton. It's up to you to instantiate it and use it from the plugin code.

	* "Add qgiscommons library". if checked, the [qgiscommons](https://github.com/boundlessgeo/lib-qgis-commons) library is added as a dependency of the plugin. If this option is enabled, the following ones will be available:

		* "Add Settings menu". If your plugin has user settings, check this to have a corresponding menu that will display a custom interface to edit settings values. Settings are defined in a `settings.json` file in the plugin folder. Open it and edit there the settings that you need for your plugin, defining its name, default value and type. Check the qgiscommons help to know more about how to later use settings values.

		* "Add About menu". Adds a "About" menu to the plugin menu.

		* "Add Help menu". Adds a "Help" menu to the plugin menu. Clicking on it will open a webbrowser and show the help files built based on the Sphinx documents (you should enable that option as well, unless you want to manually create the help files using another tool)

* "Menus" tab.

	Use this tab to add menus that will be available when you plugin is loaded. Type the menu title and select the parent menu under which it should appear. Optionally, you can click on the "Select icon" button and select an icon from the provided sample set. That will open a file selector in the folder where icon files are stored, but you can select any other icon in your file system. The selected icons will be copied to an `icons` folder under the output plugin folder. Click on the "Add Menu" button to add the menu to the list of the ones to add to your plugin.

* "Publication" tab.

	* Bug tracker.  The URL of the plugin bug tracker.

	* Repository. The URL of the repository where the code of the plugin will be stored.

	* Homepage. The URL of the plugin project homepage (optional)

	* Tags. A comma-separated list of tags used to categorize the plugin.

	* Flag as experimental. If checked, the plugin will be flagged as experimental in the metadata file.

## Other elements in the generated plugin.

Regardless of the configuration selected in the Plugin Creator UI, plugins generated with the Plugin Creator always contain the following elements:


* A plugin class (`plugin.py` in the folder named with the short name of your plugin). The plugin adds a single menu item. Selecting it will open a simple dialog. The .ui file corresponding to that dialog is located in `ui/[pluginname]dialog.py`. Edit it with Qt Designer to adapt it to your needs.

* A `requirements.txt` file with additional libraries required by the plugin.

* A `pavement.py` file with the following tasks:

    + `setup`. Downloads and installs the required dependencies for the plugin  in the `extlibs` folder. This folder is added to the PYTHONPATH by default by the plugin itself. The list of dependencies should be in the `requirements.txt` file, listing the PyPI names of the libraries, one per line. If you checked the "Add qgiscommons library" check box, the generated plugin will contains the [qgiscommons](https://github.com/boundlessgeo/lib-qgis-commons) library as its only dependency. Otherwise it will contain no dependencies.

    + `install`. Installs the plugin into the user plugins folder. It might copy the plugin folder itself, or create a symlink, depending on the OS.

    + `package`. Creates a `package.zip` file with the content of the plugin, ready to be published. It includes dependencies as well, but it will not download them, so the `setup` task has to be run before packaging. Accepts a `test`or `-t` parameter, which indicates that tests should also be packaged. By default, tests are not added.

* An empty `README.md` file, which just contains the name of the plugin in its header.



