'''
CSH-Crowdsourcing Group
Produced by Yimeng Zhao
Nov 29, 2016

This code is used to extract image id from MongoDB and to output a csv file with ids

Usage:
python extractId.py csvFile -l limit -pn pageMin -pm pageMax -hn heightMin -hm heightMax -wn widthMin -wm widthMax

-l, -pn, -pm, -hn, -hm, -wn, -wm are optional

For example, 
python extractId.py id.csv -l 1 -pn 3 -pm 5 -hn
will store image ids into a file named 'id.csv' and those images are selected from page 3 to page 5, page 3 and 5 inclusive.


The default values for limit, numPage, height and width are 0, [11,maxNumPage], (0,maxHeight) and (0, minHeight), separetly. 
Note, limit = 0 means select all images that satisfy criteria.
maxNumPage,maxHeight, minHeight are from the function find_max, which can retrive the max value in MongoDB

'''

# -*- coding: utf-8 -*-

import os
import sys
from pymongo import MongoClient
import argparse
import pandas as pd

import db_config


"""Connect to the MongoDB database
"""

mongoConn = MongoClient(db_config.DB_HOST + ":" + str(db_config.DB_PORT))
claciTransDB = mongoConn[db_config.TRANSCRIPTION_DB_NAME]
claciTransDB.authenticate( db_config.TRANSCRIPTION_DB_USER, 
                           db_config.TRANSCRIPTION_DB_PASS)
collections = claciTransDB.collection_names()

if db_config.TRANS_DB_MeetingMinColl not in collections:
   claciTransDB.create_collection(db_config.TRANS_DB_MeetingMinColl)

transWordColl = claciTransDB[db_config.TRANS_DB_MeetingMinColl] 


"""parser interface for this code"""
argumentParser = argparse.ArgumentParser(description='Extract image ids from MongoDB. You can select certain number of images in certain pages, of certain sizes (heights ans widths). Images already uploaed to Zooniverse is exlusive.')
argumentParser.add_argument( "outfile", type=argparse.FileType('w'), help="csv file that stores image ids")
argumentParser.add_argument("-l", "--limit", nargs='?', help="the number of images you want to select")
argumentParser.add_argument("-pn", "--pageMin", nargs='?', help="the minium page number to select from")
argumentParser.add_argument("-pm", "--pageMax",  nargs='?', help="the maxium page number to select from")
argumentParser.add_argument("-hn", "--heightMin", nargs='?', help="the minium height of images")
argumentParser.add_argument("-hm", "--heightMax", nargs='?', help="the maxium height of images")
argumentParser.add_argument("-wn", "--widthMin", nargs='?', help="the minium width of images")
argumentParser.add_argument("-wm", "--widthMax", nargs='?', help="the maxium width of images")
arguments = argumentParser.parse_args()

if len(sys.argv) < 1:
    print("Please run the program with the -h argument to see the help")
    sys.exit()


'''*
Define a function to Get max of one attribute (numPage, height and width) for futher use
*'''
def find_max(coll,attribute):
    for item in coll.find().sort(attribute,-1).limit(1):
            return (item[attribute])

'''*
Define a function to chanege values of each attribute (limit, numPage, height and width)
*'''
def change_value(x,y):
    if y == None:
        x = x
    else:
        x = int(y)
    return(x)

"""*
Define a function to extract image ids from MongoDB

There could be 4 different kinds of critirea to select images: 
    1) limit: how many images in total you want to select, defualt 0 means all
    2) numPage: select from which page to which page, default greater than 10 lower than the max numPage
    3) height: image heights range, default greater than 0 lower thatn max value of height
    4) width: image width range, default greater than 0 lower thatn max value of width

And only images that have not been uploaded to Zooniverse will be selected.
"""
def extract_id(coll,value):
    image_id = []
    
    for item in coll.find({'zooniverseData':{'$exists':False},'numPage':{'$gt':value[1]-1,'$lt':value[4]+1},'height':{'$gt':value[2],'$lt':value[5]},'width':{'$gt':value[3],'$lt':value[6]}}).limit(value[0]):
        image_id.append(item['_id'])
        
    return(image_id)


def main():
    attribute = ['numPage','height','width'] # input what criteria you want
    value = [0,11,0,0] # limit number and minium for numPage, height, width
    for attr in attribute:
        value.append(find_max(transWordColl,attr))
    
    print('=========================Instruction===========================')
    print('You can 4 kinds of critirea of image selection:')
    print('1) limit: how many images in total you want to select, defualt all')
    print('2) numPage: page range to select from, default starting from 11')
    print('3) height: image heights range, default greater than 0 lower thatn max value of height')
    print('4) width: image width range, default greater than 0 lower thatn max value of width')
    print('If no more changes is made, enter end')
    print('=======================Instruction Ends=========================')
    
    value[0] = change_value(value[0], arguments.limit)
    value[1] = change_value(value[1], arguments.pageMin)
    value[4] = change_value(value[4], arguments.pageMax)
    value[2] = change_value(value[2], arguments.heightMin)
    value[5] = change_value(value[5], arguments.heightMax)
    value[3] = change_value(value[3], arguments.widthMin)
    value[6] = change_value(value[6], arguments.widthMax)

    print('\nYou select %d images numPage from %d to %d, heights greater than %d lower thatn %d, width greater than %d and lower than %d' %(value[0],value[1],value[4],value[2],value[5],value[3],value[6]))
    print('================================================================')
    print('                           processing                           ')
    print('================================================================')
    image_id = extract_id(transWordColl,value)
    print(len(image_id),'image ids are stored into csv file')
    
    ''' write list  to csv'''
    df = pd.DataFrame(image_id,columns = ['iamge_id'])
    df.to_csv(arguments.outfile,index = False)
    
    
'''*
Main code starts here
'''
main()