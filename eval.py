import string
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix

dataset = 'bio'

train = []
with open(dataset+'/doc_id.txt') as fin:
	for line in fin:
		idx = line.strip().split(':')[1].split(',')
		train += [int(x) for x in idx]

y = []
with open(dataset+'/dataset.csv') as fin:
	for idx, line in enumerate(fin):
		if idx not in train:
			y.append(line.strip().split(',')[0][1:-1])

y_pred = []
with open(dataset+'/out.txt') as fin:
	for idx, line in enumerate(fin):
		if idx not in train:
			y_pred.append(line.strip())

print(f1_score(y, y_pred, average='micro'))
print(f1_score(y, y_pred, average='macro'))

print(confusion_matrix(y, y_pred))