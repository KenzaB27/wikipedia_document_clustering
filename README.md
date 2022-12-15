# Wikipedia Document clustering

## Project setup instructions

### Installation

You can install all the requirements with following command.
```
    pip install -r requirements.txt
```

### Clustering Pipeline Launch 
You can launch the clustering pipeline in two different modes:
* **Experiment**: this mode execute all the pipeline from scratch. This includes data preprocessing + graph creation + clustering. 
```bash
python main.py --experiment
```
* **Backup**: Given that the preprocessing takes a long time, a backup processed dataset is stored in the data folder and can be retrieved with backup mode to then execute the graph creation and clustering.
```bash
python main.py --backup 
```
## Plot Recreation

All the plots can be created and are saved in the ```data\images``` folder by launching all the cells of the Jupiter notebook ``` feedly_challenge.ipynb``` 

## Code Structure

The jupyter notebook represents all the results of my investigation, and the code is structered in the following way.
```bash
│   .gitignore
│   feedly_challenge.ipynb
│   main.py
│   README.md
│   requirements.txt
│   test.pdf
│   __init__.py
│
├───clustering
│   │   clustering_pipeline.py
│   │   wiki_graph.py
│   │   __init__.py
│   │
│   └───__pycache__
│
├───data
│   │   dataset_business_technology_cybersecurity.pickle
│   │
│   ├───backup_preprocess
│   │       content.txt
│   │       content_normalized.txt
│   │       content_tokenized.txt
│   │       content_without_noise.txt
│   │       nb_clusters.npy
│   │       titles.txt
│   │
│   └───images
│           nb_unique_words.png
│           n_cl_vs_n_tokens.png
│           n_cl_vs_n_tokens_int.png
│           quality_eval.png
│
├───Models
│       best_gbc.pickle
│       best_knnc.pickle
│       best_lrc.pickle
│       best_mnbc.pickle
│       best_rfc.pickle
│       best_svc.pickle
│
├───tests
│       test_preprocessing_unittest.py
│       test_wiki_graph_unittest.py
│       __init__.py
│
└───utils
    │   preprocessing.py
    │   __init__.py
    │
    └───__pycache__
```
