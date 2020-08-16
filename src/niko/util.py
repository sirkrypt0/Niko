from os.path import dirname, realpath, join

def resource_path(name):
	return join(dirname(realpath(__file__)), "resources", name)
