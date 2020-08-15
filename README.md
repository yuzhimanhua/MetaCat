# Minimally Supervised Categorization of Text with Metadata

This project provides a weakly-supervised framework for categorizing text with metadata.

## Installation

For training, a GPU is highly recommended.

### Keras
The code is based on the Keras library. You can find installation instructions [**here**](https://keras.io/#installation).

### Dependency
The code is written in Python 3.6. The dependencies are summarized in the file ```requirements.txt```. You can install them like this:

```
pip3 install -r requirements.txt
```

## Quick Start
To reproduce the results in our paper, you need to first download the datasets [**here**](https://drive.google.com/file/d/1ktIzp1LR2DN-SMwNm91nYdyEoqhDBAE3/view?usp=sharing). Five datasets are used in our paper. The **GitHub-Sec** dataset, unfortunately, cannot be published due to our commitment to the data provider. The other four datasets are available. Once you unzip the downloaded file, you can see four folders related to these four datasets, respectively.

| Dataset | Folder Name | #Documents | #Classes | Class name (#Repositories in this class) | 
| ------------- |-------------| ----- | ---------- | --------- |
| [GitHub-Bio](https://drive.google.com/file/d/1C7V9Ww-ZaoWqaHdNR_fryXfEmZEowYXK/view) | ```bio/``` | 876 | 10 | Sequence Analysis (210), Genome Analysis (176), Gene Expression (63), Systems Biology (53), Genetics (47), Structural Bioinformatics (39), Phylogenetics (27), Text Mining (63), Bioimaging (125), Database and Ontologies (73)|
| [GitHub-AI](https://drive.google.com/file/d/1C7V9Ww-ZaoWqaHdNR_fryXfEmZEowYXK/view) | ```ai/``` | 1,596 | 14 | Image Generation (215), Object Detection (296), Image Classification (361), Semantic Segmentation (170), Pose Estimation (96), Super Resolution (75), Text Generation (24), Text Classification (26), Named Entity Recognition (22), Question Answering (102), Machine Translation (117), Language Modeling (44), Speech Synthesis (27), Speech Recognition (21)|
| [Amazon](http://jmcauley.ucsd.edu/data/amazon/index.html) | ```amazon/``` | 100,000 | 10 | Apps for Android (10,000), Books (10,000), CDs and Vinyl (10,000), Clothing, Shoes and Jewelry (10,000), Electronics (10,000), Health and Personal Care (10,000), Home and Kitchen (10,000), Movies and TV (10,000), Sports and Outdoors (10,000), Video Games (10,000)|
| [Twitter](https://drive.google.com/file/d/0Byrzhr4bOatCRHdmRVZ1YVZqSzA/view) | ```twitter/``` | 135,619 | 9 | Food (34,387), Shop and Service (13,730), Travel and Transport (8,826), College and University (2,281), Nightlife Spot (15,082), Residence (1,678), Outdoors and Recreation (19,488), Arts and Entertainment (26,274), Professional Places (13,783) |

You need to put the dataset folders under the repository main folder ```./```. Then the following running script can be used to run the model.

```
./test.sh
```

Micro-F1, Macro-F1 and the confusion matrix will be shown in the last several lines of the output. The classification result can be found under your dataset folder. For example, if you are using the **GitHub-Bio** dataset, the output will be ```./bio/out.txt```.

## Data

Besides the "input" version mentioned in the Quick Start section, we also provide the [**json version**](https://drive.google.com/file/d/130nPPXm0JHsS2EVg0e19SnTBc840tCLx/view?usp=sharing), where each line is a json file containing text and metadata (e.g., user, tags and product).

For **GitHub-Bio**, **GitHub-AI**, and **Twitter**, the json format is as follows:
```
{
  "user": "86372688",
  "tags": [
    "#PurityVodka",
    "#NewYorkCity"
  ],
  "text": "purityvodka hudsonmalone newyorkcity hudson malone",
  "label": "Food"
}
```
For **Amazon**, the json format is as follows:
```
{
  "user": "A1N4O8VOJZTDVB",
  "product": "B004A9SDD8",
  "text": "really cute loves the song , so he really could n't wait to play this . ... ",
  "label": "Apps_for_Android"
}
```

## Running New Datasets
In the Quick Start section, we include a pretrained embedding file in the downloaded folders. If you have a new dataset, you need to rerun our generation-guided embedding module to get your own embedding files. Please follow the steps below.

1. Create a directory named ```${dataset}``` under the main folder (e.g., ```./bio```).

2. Prepare three files: (1) ```./${dataset}/doc_id.txt``` containing labeled document ids for each class. Each line begins with the class id (starting from ```0```), followed by a colon, and then document ids in the corpus (starting from ```0```) of the corresponding class separated by commas; (2) ```./${dataset}/dataset.csv```; and (3) ```./${dataset}/dataset.json```. **You can refer to the example datasets ([doc_id/csv](https://drive.google.com/file/d/1ktIzp1LR2DN-SMwNm91nYdyEoqhDBAE3/view?usp=sharing) and [json](https://drive.google.com/file/d/130nPPXm0JHsS2EVg0e19SnTBc840tCLx/view?usp=sharing)) for the format.**

3. ```cd gge/``` and then ```./embed.sh```. Make sure you have changed the dataset name. The embedding file will be saved to ```gge/embedding_gge```.

With the embedding file, you can train the classifier as mentioned in Quick Start (make sure you move it to ```${dataset}/```.
Please always refer to the example datasets when adapting the code for a new dataset.

## Citation
If you find the implementation useful, please cite the following paper:
```
@inproceedings{zhang2020minimally,
  title={Minimally Supervised Categorization of Text with Metadata},
  author={Zhang, Yu and Meng, Yu and Huang, Jiaxin and Xu, Frank F. and Wang, Xuan and Han, Jiawei},
  booktitle={SIGIR'20},
  pages={1231--1240},
  year={2020},
  organization={ACM}
}
```
