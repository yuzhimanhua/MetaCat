dataset=bio
embedding=gge

python main.py --dataset ${dataset} --embedding ${embedding}

python eval.py --dataset ${dataset}