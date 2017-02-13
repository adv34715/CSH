# This file is to copy images from soucePath folder to destPath folder according to image ids in a csv file
#
# Usage:
# python copyImage.py infile -s sourcePath -d destPath
#
# infile is a csv file stores image_id
###

import os
import sys
import pandas as pd
import argparse
from shutil import copyfile

"""parser interface for this code"""
argumentParser = argparse.ArgumentParser(description='If the source as well as destination paths are provided, the program will copy these matching files to the desitnations folder.')
argumentParser.add_argument( "infile", type=argparse.FileType('r'), help="csv file that stores image ids")
argumentParser.add_argument("-s", "--sourcePath", help="source path in which to find files")
argumentParser.add_argument("-d", "--destPath", help="destination filesystem path in which to copy files")
arguments = argumentParser.parse_args()

if len(sys.argv) < 3:
    print("Please run the program with the -h argument to see the help")
    sys.exit()

#verify that sourcePath exists
if arguments.sourcePath is not None and not os.path.exists(arguments.sourcePath):
    print("The source path: " + arguments.sourcePath + " is not a folder. Unable to continue")
    sys.exit()

#verify that destPath exists
if arguments.destPath is not None and not os.path.exists(arguments.destPath):
    print("The source path: " + arguments.destPath + " is not a folder. Unable to continue")
    sys.exit()

try:
    """open imageId file which stores the image ids extracted from MongoDB"""
    image_id = pd.read_csv(arguments.infile)
    
    sourcePath = arguments.sourcePath
    destPath = arguments.destPath
    print ('\nCopying images from folder \'%s\' to folder \'%s\'.' % (sourcePath,destPath))
    print('=====================================================================')
    print('                             Copying                                 ')
    print('=====================================================================')
    count = 0 # count for number of copied images
    
    for dirpath, dirs, files in os.walk(sourcePath, topdown=True):
        for fileNameExt in files:
            sourceFilePath = os.path.join(dirpath, fileNameExt)
            destFilePath = os.path.join(destPath, fileNameExt)
            if fileNameExt.split('.')[0] in image_id['iamge_id'].values and fileNameExt != destFilePath:
                copyfile(sourceFilePath, destFilePath)
                count +=1
    print('%d images have been copied from folder \'%s\' to folder \'%s\'.\n' % (count,sourcePath,destPath))

except IndexError:
    print( "Collection " + db_config.TRANS_DB_MeetingMinColl + " does not exist")

