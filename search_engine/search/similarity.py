import numpy as np


class Similarity:
    pass


class TFIDFSimilarity(Similarity):

    def tf(self, freq, norm):
        return freq / norm

    def idf(self, doc_freq, all_doc_count):
        return np.log(all_doc_count / (doc_freq + 1))

    def score(self, boost, idf_val, freq, norm):
        query_weight = boost * idf_val
        return self.tf(freq, norm) * query_weight
