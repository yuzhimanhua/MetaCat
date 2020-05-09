dataset=bio

samples=100
# samples = 100 for bio and ai; samples = 200 for cyber, amazon and twitter

python preprocess.py --dataset ${dataset}

./line -train edge.txt --output out.emb -binary 0 -size 100 -order 1 -negative 5 -samples ${samples} -rho 0.025 -threads 20

python postprocess.py
