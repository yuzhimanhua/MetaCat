import json
import argparse

parser = argparse.ArgumentParser(description='main', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--dataset', default='bio', choices=['bio', 'ai', 'cyber', 'amazon', 'twitter'])
args = parser.parse_args()
dataset = args.dataset

with open(dataset+'/meta_dict.json') as fin:
	meta_dict = json.load(fin)
	local = meta_dict['local']

with open(dataset+'/'+dataset+'.json') as fin, open(dataset+'/dataset.csv', 'w') as fout:
	for line in fin:
		js = json.loads(line)
		text = js['text']
		for lm in local:
			local_metadata = ['$'+lm.upper()+'_'+x for x in js[lm]]
			text += ' ' + ' '.join(local_metadata)
		fout.write(str(js['label'])+',\"'+text.strip()+'\"\n')
