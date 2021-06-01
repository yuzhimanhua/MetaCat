# Minimally Supervised Categorization of Text with Metadata

This project provides a weakly supervised framework for categorizing text with metadata.

## Links

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Data](#data)
- [Running on New Datasets](#running-on-new-datasets)
- [Citation](#citation)

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
To reproduce the results in our paper, you need to first download the [**datasets**](https://drive.google.com/file/d/1ktIzp1LR2DN-SMwNm91nYdyEoqhDBAE3/view?usp=sharing). Five datasets are used in our paper. The **GitHub-Sec** dataset, unfortunately, cannot be published due to our commitment to the data provider. The other four datasets are available. Once you unzip the downloaded file, you can see four folders corresponding to these four datasets, respectively.

| Dataset | Folder Name | #Documents | #Classes | Class name (#Repositories in this class) | 
| ------------- |-------------| ----- | ---------- | --------- |
| [GitHub-Bio](https://github.com/yuzhimanhua/HiGitClass) | ```bio/``` | 876 | 10 | Sequence Analysis (210), Genome Analysis (176), Gene Expression (63), Systems Biology (53), Genetics (47), Structural Bioinformatics (39), Phylogenetics (27), Text Mining (63), Bioimaging (125), Database and Ontologies (73)|
| [GitHub-AI](https://github.com/yuzhimanhua/HiGitClass) | ```ai/``` | 1,596 | 14 | Image Generation (215), Object Detection (296), Image Classification (361), Semantic Segmentation (170), Pose Estimation (96), Super Resolution (75), Text Generation (24), Text Classification (26), Named Entity Recognition (22), Question Answering (102), Machine Translation (117), Language Modeling (44), Speech Synthesis (27), Speech Recognition (21)|
| [Amazon](http://jmcauley.ucsd.edu/data/amazon/index.html) | ```amazon/``` | 100,000 | 10 | Apps for Android (10,000), Books (10,000), CDs and Vinyl (10,000), Clothing, Shoes and Jewelry (10,000), Electronics (10,000), Health and Personal Care (10,000), Home and Kitchen (10,000), Movies and TV (10,000), Sports and Outdoors (10,000), Video Games (10,000)|
| [Twitter](https://github.com/franticnerd/geoburst) | ```twitter/``` | 135,619 | 9 | Food (34,387), Shop and Service (13,730), Travel and Transport (8,826), College and University (2,281), Nightlife Spot (15,082), Residence (1,678), Outdoors and Recreation (19,488), Arts and Entertainment (26,274), Professional Places (13,783) |

You need to put these 4 dataset folders under the repository main folder ```./```. Then the following running script can be used to run the model.

```
./test.sh
```

Micro-F1, Macro-F1 and the confusion matrix will be shown in the last several lines of the output. The classification result can be found under your dataset folder. For example, if you are using the **GitHub-Bio** dataset, the output will be ```./bio/out.txt```.

## Data

Besides the "input" version mentioned in the Quick Start section, we also provide the [**json version**](https://drive.google.com/file/d/130nPPXm0JHsS2EVg0e19SnTBc840tCLx/view?usp=sharing), where each line is a json file containing text and metadata (e.g., user, tags and product).

For **GitHub-Bio**, **GitHub-AI**, and **Twitter**, the json format is as follows:
```
{
  "user": [
    "Natsu6767"
  ],
  "text": "pytorch implementation of dcgan trained on the celeba dataset ...",
  "tags": [
    "pytorch",
    "dcgan",
    "gan",
    "implementation",
    "deeplearning",
    "computer-vision",
    "generative-model"
  ],
  "label": 0,
  "label_name": "$Image-Generation"
}
```
Here, the "user" field is global metadata; the "tags" field is local metadata. (Please refer to our [paper](https://arxiv.org/abs/2005.00624) for the definitions of global and local metadata.)

For **Amazon**, the json format is as follows:
```
{
  "user": [
    "A1N4O8VOJZTDVB"
  ],
  "text": "really cute loves the song so he really could ...",
  "product": [
    "B004A9SDD8"
  ],
  "label": 0,
  "label_name": "Apps_for_Android"
}
```
Here, both "user" and "product" are global metadata; there is no local metadata in the Amazon dataset.

**NOTE: If you would like to run our code on your own dataset, when you prepare this json file, make sure: (1) For each document, its metadata field is always represented by a list. For example, the "user" field should be \["A1N4O8VOJZTDVB"\] instead of "A1N4O8VOJZTDVB". (2) The "label" field is an integer. If you have N classes, the label space should be 0, 1, ..., N-1. The "label_name" field is optional.**

## Running on New Datasets
In the Quick Start section, we include a pretrained embedding file in the downloaded folders. If you have a new dataset, you need to rerun our generation-guided embedding module to get your own embedding files. Please follow the steps below.

1. Create a directory named ```${dataset}``` under the main folder (e.g., ```./bio```).

2. Prepare three files: 

(1) ```./${dataset}/doc_id.txt``` containing labeled document ids for each class. Each line begins with the class id (starting from ```0```), followed by a colon, and then document ids in the corpus (starting from ```0```) of the corresponding class separated by commas. 

(2) ```./${dataset}/dataset.json```. You can refer to the provided [json files](https://drive.google.com/file/d/130nPPXm0JHsS2EVg0e19SnTBc840tCLx/view?usp=sharing) for the format. **Make sure it has two fields "text" and "label".** ("label" should be an integer in 0, 1, ..., N-1, corresponding to the classes in ```./${dataset}/doc_id.txt```.) **You can add your own metadata fields in the json.**            

(3) ```./${dataset}/meta_dict.json``` indicating the names of your global/local metadata fields. For example, for GitHub-Bio, GitHub-AI, and Twitter, it should be
```
{"global": ["user"], "local": ["tags"]}
```
For Amazon, it should be
```
{"global": ["user", "product"], "local": []}
```

3. ```./prep_emb.sh```. Make sure you have changed the dataset name. The embedding file will be saved to ```./${dataset}/embedding_gge```.

With the embedding file, you can train the classifier as mentioned in Quick Start (i.e., ```./test.sh```).
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
