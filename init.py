import os
import shutil

def prompt(message, validate):
    res = None
    while res is None:
        res = raw_input(message)
        if not validate(res):
            print "Invalid value!"
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

def main ():

	pluginName = prompt("Plugin name:", lambda v : bool(v.strip()))
	defaultShortName = removeInvalidChars(pluginName).lower()
	pluginShortName = (prompt("Plugin short name (no blank spaces allowed) [Leave empty to use '%s']: " 
							% defaultShortName, lambda s: s == removeInvalidChars(s)) or defaultShortName)
	defaultClassName = className(pluginName)
	pluginClassName = (prompt("Plugin class name [Leave empty to use '%s']: " % defaultClassName,
							lambda s: s == removeInvalidChars(s)) or defaultClassName)

	toReplace = [("[pluginname]", pluginName), ("[pluginshortname]", pluginShortName), ("[pluginclassname]", pluginClassName)]
	folder = os.path.dirname(os.path.realpath(__file__))
	gitFolder = os.path.join(folder, ".git")
	if os.path.exists(gitFolder):
		try:
			shutil.rmtree(gitFolder)
		except:
			pass
	for root, dirs, files in os.walk(folder):
	    for f in files:       
	    	if ".git" not in root:
				replaceInFiles(os.path.join(root, f), toReplace)
	
	os.rename(os.path.join(folder, "pluginname"), os.path.join(folder, pluginShortName))

	with open(os.path.join(folder, "README.md"), 'w') as f:
	  f.write("#" + pluginName)


if __name__ == '__main__':
	main()