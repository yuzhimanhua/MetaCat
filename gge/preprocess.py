import string
import json
from collections import defaultdict

import argparse
parser = argparse.ArgumentParser(description='main', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('--dataset', default='bio', choices=['bio', 'ai', 'cyber', 'amazon', 'twitter'])
args = parser.parse_args()

folder = '../' + args.dataset + '/'

lengths = {'bio': 600, 'ai': 600, 'cyber': 800, 'amazon': 150, 'twitter': 30}

cnt = defaultdict(int)
rpid = set()
label = set()
tag = set()
prod = set()
user = set()

doc_id = []
length = lengths[dataset]

with open(folder+'doc_id.txt') as fin:
	for line in fin:
		doc_idx = line.strip().split(':')[1].split(',')
		doc_id += [int(x) for x in doc_idx]

label2id = dict()

with open(folder+dataset+'.json') as fin:
	for idx, line in enumerate(fin):
		
		js = json.loads(line)

		js['label'] = js['label'].replace(' ', '-')

		if js['label'] not in label2id:
			label2id[js['label']] = len(label2id)

		rpid.add('$DOCU_'+str(idx))
		user.add('$USER_'+js['user'])
		label.add('$LABL_'+js['label']+'$'+str(label2id[js['label']]))

		if dataset in ['bio', 'ai', 'twitter']:
			for T in js['tags']:
				tag.add('$TAG_'+T.lower())

		if dataset in ['amazon']:
			prod.add('$PROD_'+js['product'])

		W = js['text'].lower().split()
		for token in W[:length]:
			cnt[token] += 1

node2id = defaultdict()
with open(folder+'node2id.txt', 'w') as fout:
	for R in rpid:
		node2id[R] = len(node2id)
		fout.write(R+' '+str(node2id[R])+'\n')
	
	for U in user:
		node2id[U] = len(node2id)
		fout.write(U+' '+str(node2id[U])+'\n')

	for L in label:
		node2id[L] = len(node2id)
		fout.write(L+' '+str(node2id[L])+'\n')

	if dataset in ['bio', 'ai', 'twitter']:
		for T in tag:
			node2id[T] = len(node2id)
			fout.write(T+' '+str(node2id[T])+'\n')

	if dataset in ['amazon']:
		for P in prod:
			node2id[P] = len(node2id)
			fout.write(P+' '+str(node2id[P])+'\n')

	for W in cnt:
		if cnt[W] < 10:
			continue
		node2id[W] = len(node2id)
		node2id['$CTXT_'+W] = len(node2id)
		fout.write(W+' '+str(node2id[W])+'\n')
		fout.write('$CTXT_'+W+' '+str(node2id['$CTXT_'+W])+'\n')

moduli = len(node2id)+1
win = 5
edge = defaultdict(int)

with open(folder+dataset+'.json') as fin:
	for idx, line in enumerate(fin):	
		if idx % 1000 == 0:
			print(idx)
		js = json.loads(line)

		js['label'] = js['label'].replace(' ', '-')

		R = '$DOCU_'+str(idx)
		U = '$USER_'+js['user']
		L = '$LABL_'+js['label']+'$'+str(label2id[js['label']])
		W = js['text'].lower().split()

		sent = []
		for token in W[:length]:
			if cnt[token] < 10:
				continue
			sent.append(token)

		for i in range(len(sent)):
			for j in range(i+1, i+win+1):
				if j >= len(sent):
					continue
				id1 = node2id[sent[i]]
				id2 = node2id['$CTXT_'+sent[j]]
				edge[id1*moduli+id2] += 1
				id1 = node2id[sent[j]]
				id2 = node2id['$CTXT_'+sent[i]]
				edge[id1*moduli+id2] += 1

		for i in range(len(sent)):
			id1 = node2id[R]
			id2 = node2id[sent[i]]
			edge[id1*moduli+id2] += win
			id1 = node2id[sent[i]]
			id2 = node2id[R]
			edge[id1*moduli+id2] += win
			
		id1 = node2id[U]
		id2 = node2id[R]
		edge[id1*moduli+id2] += win * length
		id1 = node2id[R]
		id2 = node2id[U]
		edge[id1*moduli+id2] += win * length

		if idx in doc_id:
			id1 = node2id[R]
			id2 = node2id[L]
			edge[id1*moduli+id2] += win * length
			id1 = node2id[L]
			id2 = node2id[R]
			edge[id1*moduli+id2] += win * length

		if dataset in ['bio', 'ai', 'twitter']:
			Ts = ['$TAG_'+x.lower() for x in js['tags']]
			for T in Ts:
				id1 = node2id[R]
				id2 = node2id[T]
				edge[id1*moduli+id2] += win
				id1 = node2id[T]
				id2 = node2id[R]
				edge[id1*moduli+id2] += win

		if dataset in ['amazon']:
			P = '$PROD_'+js['product']
			id1 = node2id[P]
			id2 = node2id[R]
			edge[id1*moduli+id2] += win * length
			id1 = node2id[R]
			id2 = node2id[P]
			edge[id1*moduli+id2] += win * length

with open(folder+'edge.txt', 'w') as fout:
	for e in edge:
		id1 = e // moduli
		id2 = e % moduli
		fout.write(str(id1)+'\t'+str(id2)+'\t'+str(edge[e])+'\n')