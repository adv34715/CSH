# CSH_new
## There should be totally 5 py files:
1. dbConfig.py
2. extractId.py
3. copyImage.py
4. getTrans.py
5. storeIntoDB.py (by Jiang)

####1. dbConfig.py is the MongoDB  database settings
####2. extractId.py is to extract image id from MongoDB and to output a csv file with ids
Usage:
python extractId.py csvFile -l limit -pn pageMin -pm pageMax -hn heightMin -hm heightMax -wn widthMin -wm widthMax

-l, -pn, -pm, -hn, -hm, -wn, -wm are optional

For example, 
python extractId.py id.csv -l 1 -pn 3 -pm 5 -hn
will store image ids into a file named 'id.csv' and 
those images are selected from page 3 to page 5, page 3 and 5 inclusive.


The default values for limit, numPage, height and width are 
0, [11,maxNumPage], (0,maxHeight) and (0, minHeight), separetly. 

Note, limit = 0 means select all images that satisfy criteria.
maxNumPage,maxHeight, minHeight are from the function find_max, 
which can retrive the max value in MongoDB

####3. copyImage.py is to copy images from soucePath folder to destPath folder according to image ids in a csv file
Usage:
python copyImage.py infile -s sourcePath -d destPath

Note, infile is a csv file stores image_id
