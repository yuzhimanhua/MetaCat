import string
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
import argparse

parser = argparse.ArgumentParser(description='main', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--dataset', default='bio', choices=['bio', 'ai', 'cyber', 'amazon', 'twitter'])
args = parser.parse_args()
dataset = args.dataset

train = []
with open(f'{dataset}/doc_id.txt') as fin:
	for line in fin:
		idx = line.strip().split(':')[1].split(',')
		train += [int(x) for x in idx]

y = []
with open(f'{dataset}/dataset.csv') as fin:
	for idx, line in enumerate(fin):
		if idx not in train:
			y.append(line.strip().split(',')[0])

y_pred = []
with open(f'{dataset}/out.txt') as fin:
	for idx, line in enumerate(fin):
		if idx not in train:
			y_pred.append(line.strip())

print(f1_score(y, y_pred, average='micro'))
print(f1_score(y, y_pred, average='macro'))

print(confusion_matrix(y, y_pred))