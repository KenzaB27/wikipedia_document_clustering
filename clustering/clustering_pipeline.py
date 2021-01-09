import nltk
import pandas as pd
from utils.preprocessing import remove_noise_from_df, normalize_df
from clustering.wiki_graph import WikiGraph


class ClusteringPipeline(object):
    def __init__(self):
        self.wiki_df = None
        self.wiki_pages = []
        self.wiki_graph = WikiGraph()
        self.wiki_clusters = None
    
    def load_raw_data(self):
        self.wiki_df = pd.read_pickle(
            "data/dataset_business_technology_cybersecurity.pickle")
        self.wiki_df = pd.DataFrame(self.wiki_df)
    
    def preprcessing(self):
        self.wiki_df["content"] = remove_noise_from_df(wiki_df["content"])
        self.wiki_df["content"] = normalize_df(wiki_df["content"])
        self.wiki_df["content"] = wiki_df["content"].progress_apply(
            nltk.word_tokenize)
        self.wiki_pages = self.wiki_df.to_dict(order="records")

    def load_processed_data(self):
        self.wiki_df = pd.read_csv("data/backup_preprocess/content_tokenized.txt")
        self.wiki_pages = self.pd.to_dict(order="records")

    def clustering(self, constraint):
        self.wiki_graph.build_graph(self.wiki_pages, constraint=constraint)
        self.wiki_clusters = self.wiki_graph.get_wiki_clusters()

        
