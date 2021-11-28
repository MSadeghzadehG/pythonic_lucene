import numpy as np


class Similarity:
    '''
    Similarity defines the components of Lucene scoring. 

    Doc: https://lucene.apache.org/core/8_11_0/core/org/apache/lucene/search/similarities/Similarity.html
    Code: https://github.com/apache/lucene/blob/main/lucene/core/src/java/org/apache/lucene/search/similarities/Similarity.java
    '''
    pass


class TFIDFSimilarity(Similarity):
    '''
    Doc: https://lucene.apache.org/core/8_11_0/core/org/apache/lucene/search/similarities/TFIDFSimilarity.html
    Code: https://github.com/apache/lucene/blob/main/lucene/core/src/java/org/apache/lucene/search/similarities/TFIDFSimilarity.java
    '''
    
    def tf(self, freq, norm):
        return freq / norm

    def idf(self, doc_freq, all_doc_count):
        return np.log(all_doc_count / (doc_freq + 1))

    def score(self, boost, idf_val, freq, norm):
        query_weight = boost * idf_val
        return self.tf(freq, norm) * query_weight
