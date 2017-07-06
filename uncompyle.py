# usage of uncompyle2
# author: woootao@gmail.com
# date: 2017.7.6
#

import os
import uncompyle2

dir_path = 'E:\program\server\server\engine'
all_path_files = []

# get all file paths
for root, dir, files in os.walk(dir_path):
	if not dir:
		for file in files:
			path = root + '\\' + file
			if path[-1] in ['c']:
				all_path_files.append(str(path))

# uncompile
for f in all_path_files:
	# #print f[:-1]
	# print f
	with open(f[:-1], 'wb') as fileobj:
		uncompyle2.uncompyle_file(f, fileobj)

print 'Done'
