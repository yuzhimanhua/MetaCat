import string
import json
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser(description='main', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--dataset', default='bio', choices=['bio', 'ai', 'cyber', 'amazon', 'twitter'])

args = parser.parse_args()
dataset = args.dataset
folder = '../' + dataset + '/'

id2node = dict()
with open('node2id.txt') as fin:
	for line in fin:
		data = line.strip().split()
		id2node[data[1]] = data[0]

with open(folder+'meta_dict.json') as fin:
	meta_dict = json.load(fin)
	local = meta_dict['local']

output = []
with open('out.emb') as fin, open(folder+'embedding_gge', 'w') as fout:
	for idx, line in enumerate(tqdm(fin)):
		if idx == 0:
			continue
		data = line.strip().split()
		data[0] = id2node[data[0]]
		
		if data[0].startswith('$LABL_') or not data[0].startswith('$'):
			output.append(' '.join(data)+'\n')
		for lm in local:
			if data[0].startswith('$'+lm.upper()+'_'):
				output.append(' '.join(data)+'\n')
				break

	fout.write(str(len(output))+'\t100\n')
	for line in output:
		fout.write(line)