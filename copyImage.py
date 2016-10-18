import os
from shutil import copyfile
import numpy as np
sourcePath = 'anonD'
destPath = 'to_be_uploaded'
nameFileList = [line[:-1] for line in open('filename.txt','r')]
print np.array(nameFileList)
#np.savetxt('out.out',nameFileList)

for dirpath, dirs, files in os.walk(sourcePath, topdown=True):
	print 'dirpath: ', dirpath
	print 'dirs: ', dirs
	for fileNameExt in files:
		sourceFilePath = os.path.join(dirpath, fileNameExt)
		destFilePath = os.path.join(destPath, fileNameExt)
		#print 'fileNameExt: ', fileNameExt
		if fileNameExt.split('.')[0] in nameFileList and fileNameExt != destFilePath:
			#print fileNameExt
			copyfile(sourceFilePath, destFilePath)