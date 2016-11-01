import pandas as pd
result = pd.read_csv('./result/central-state-hospital-board-meeting-minutes-transcription-classifications.csv')
import re

grouped = result.groupby(result.subject_ids)
#print type(grouped.groups)
'''
def processTran(x):
	anno = x.translate(None, '[]{}\"').split(',')
	output = []
	pattern = 'value'
	for string in anno:
		if re.search(pattern, string):
			output.append(string.split(':')[1])
	return output
	
def processImage(x):
	name = x.translate(None, '[]{}').split(',')
	output = []
	value = name[1].split(':')[1]
	output.append(value)
	return output
trans = result.annotations.apply(processTran)
imagename = result.subject_data.apply(processImage)
for i in trans:
	print(i)

def decide(x):
	pass  #need to know the structure of the csv file
'''
