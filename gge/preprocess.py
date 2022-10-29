import string
import json
from collections import defaultdict
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser(description='main', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--dataset', default='bio', choices=['bio', 'ai', 'cyber', 'amazon', 'twitter'])

args = parser.parse_args()
dataset = args.dataset

folder = '../' + dataset + '/'
lengths = {'bio': 1000, 'ai': 1000, 'cyber': 1000, 'amazon': 150, 'twitter': 30}
if dataset in lengths:
	length = lengths[dataset]
else:
	length = 200

doc_id = []
label = set()
with open(folder+'doc_id.txt') as fin:
	for line in fin:
		data = line.strip().split(':')
		doc_idx = data[1].split(',')
		doc_id += [int(x) for x in doc_idx]
		label.add('$LABL_'+data[0])

with open(folder+'meta_dict.json') as fin:
	meta_dict = json.load(fin)
	globl = meta_dict['global']
	local = meta_dict['local']

metadata = set()
document = set()
cnt = defaultdict(int)
with open(folder+dataset+'.json') as fin:
	for idx, line in enumerate(tqdm(fin)):
		data = json.loads(line)
		document.add('$DOCU_'+str(idx))

		for gm in globl:
			for x in data[gm]:
				metadata.add('$'+gm.upper()+'_'+x)
		
		for lm in local:
			for x in data[lm]:
				metadata.add('$'+lm.upper()+'_'+x) 

		W = data['text'].split()
		for token in W[:length]:
			cnt[token] += 1

node2id = defaultdict()
with open('node2id.txt', 'w') as fout:
	for D in document:
		node2id[D] = len(node2id)
		fout.write(D+' '+str(node2id[D])+'\n')
	
	for L in label:
		node2id[L] = len(node2id)
		fout.write(L+' '+str(node2id[L])+'\n')

	for M in metadata:
		node2id[M] = len(node2id)
		fout.write(M+' '+str(node2id[M])+'\n')

	for W in cnt:
		if cnt[W] < 10:
			continue
		node2id[W] = len(node2id)
		node2id['$CTXT_'+W] = len(node2id)
		fout.write(W+' '+str(node2id[W])+'\n')
		fout.write('$CTXT_'+W+' '+str(node2id['$CTXT_'+W])+'\n')

mod = len(node2id)+1
win = 5
edge = defaultdict(int)
with open(folder+dataset+'.json') as fin:
	for idx, line in enumerate(tqdm(fin)):	
		data = json.loads(line)

		L = '$LABL_'+str(data['label'])
		D = '$DOCU_'+str(idx)
		W = data['text'].split()

		sent = []
		for token in W[:length]:
			if cnt[token] < 10:
				continue
			sent.append(token)

		for i in range(len(sent)):
			for j in range(i-win, i+win+1):
				if j >= len(sent) or j < 0 or j == i:
					continue
				id1 = node2id[sent[i]]
				id2 = node2id['$CTXT_'+sent[j]]
				edge[id1*mod+id2] += 1

		for i in range(len(sent)):
			id1 = node2id[D]
			id2 = node2id[sent[i]]
			edge[id1*mod+id2] += win
			
		if idx in doc_id:
			id1 = node2id[L]
			id2 = node2id[D]
			edge[id1*mod+id2] += win * length

		for gm in globl:
			for x in data[gm]:
				M = '$'+gm.upper()+'_'+x
				id1 = node2id[M]
				id2 = node2id[D]
				edge[id1*mod+id2] += win * length

		for lm in local:
			for x in data[lm]:
				M = '$'+lm.upper()+'_'+x
				id1 = node2id[D]
				id2 = node2id[M]
				edge[id1*mod+id2] += win

with open('edge.txt', 'w') as fout:
	for e in edge:
		id1 = e // mod
		id2 = e % mod
		fout.write(str(id1)+'\t'+str(id2)+'\t'+str(edge[e])+'\n')