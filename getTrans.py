import pandas as pd
import re
import csv
result = pd.read_csv('./zooniverse/central-state-hospital-board-meeting-minutes-transcription-classifications.csv')

def process(x):	
	name = None
	temp = []
	for row in x:
		anno = result.iloc[row,11].translate(None, '[]{}\"').split(',')
		pattern = 'value'
		for string in anno:
			if re.search(pattern, string):
				temp.append(string.split(':')[1])
	imageinf = result.iloc[x[0],12].translate(None, '[]{}').split(',')
	pattern1 = 'Filename'
	pattern2 = 'image'
	for string in imageinf:
		if re.search(pattern1, string) or re.search(pattern2, string):
			name = string.split(':')[1]
	#print name, temp
	return name, temp
		
def answerQ(x):
	return pd.Series(x).value_counts().index[0]
		
def decide(x):
	answer1 = None
	answer2 = None
	if len(x) < 3:
		if len(x) < 2:
			return [x[0]]
		else:
			return [x[0], x[1]]
	elif len(x) % 2 != 0:
		pattern = 'No text'
		for i in x:
			if re.search(pattern, i):
				x.remove(i)
				decide(x)
	else:
		question1 = [x[2*i] for i in range(len(x)/2)]
		question2 = [x[2*i+1] for i in range(len(x)/2)]
		answer1 = answerQ(question1)
		answer2 = answerQ(question2)
	return [answer1, answer2]
	
grouped = result.groupby(result.subject_ids)
finalresult = {}
for i in grouped.groups.values():
	image, trans = process(i)
	tran = decide(trans)
	finalresult[image] = tran
	
print(finalresult)
'''
with open('./output/trans.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in finalresult.items():
       writer.writerow([key, value])
	   '''