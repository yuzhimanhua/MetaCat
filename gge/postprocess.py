import string

id2node = dict()

with open('node2id.txt') as fin:
	for line in fin:
		tmp = line.strip().split()
		id2node[tmp[1]] = tmp[0]

output = []
with open('out.emb') as fin, open('embedding_gge', 'w') as fout:
	for idx, line in enumerate(fin):
		if idx == 0:
			continue

		tmp = line.strip().split()
		tmp[0] = id2node[tmp[0]]
		
		if tmp[0].startswith('$LABEL') or tmp[0].startswith('$TAG') or (not tmp[0].startswith('$') and not tmp[0].endswith('$_CONTEXT')):
			output.append(' '.join(tmp)+'\n')

	fout.write(str(len(output))+'\t100\n')
	for line in output:
		fout.write(line)