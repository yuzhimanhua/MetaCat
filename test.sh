dataset=bio
sup_source=docs
embedding=gge

export CUDA_VISIBLE_DEVICES=0

python main.py --dataset ${dataset} --sup_source ${sup_source} --embedding ${embedding} --with_evaluation True

python eval.py --dataset ${dataset}
