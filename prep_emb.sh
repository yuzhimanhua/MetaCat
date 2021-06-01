dataset=bio

echo Data Preprocessing ...
python data_preprocess.py --dataset ${dataset}

cd gge/

echo Embedding Preprocessing ...
python preprocess.py --dataset ${dataset}

echo Embedding Learning ...
./embed.sh

echo Embedding Postprocessing ...
python postprocess.py --dataset ${dataset}

cd ../
