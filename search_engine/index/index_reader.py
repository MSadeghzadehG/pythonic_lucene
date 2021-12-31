import pickle
import numpy as np
from os.path import join


class IndexReader:
    """
    IndexReader providing an interface for accessing a point-in-time view of an index.

    Doc: https://lucene.apache.org/core/8_11_0/core/org/apache/lucene/index/IndexReader.html
    Code: https://github.com/apache/lucene/blob/main/lucene/core/src/java/org/apache/lucene/index/IndexReader.java
    """

    def __init__(self, name):
        self.name = name
        index_dir = join("search_engine/indices", self.name)
        with open(join(index_dir, "doc_index"), "rb") as f:
            self.doc_freq = pickle.load(f)
        with open(join(index_dir, "index_meta"), "rb") as f:
            self.index_meta = pickle.load(f)
        with open(join(index_dir, "term_top_docs"), "rb") as f:
            self.term_top_docs = pickle.load(f)
        with open(join(index_dir, "doc_raw"), "rb") as f:
            self.raw_docs = pickle.load(f)

    def get_docs_id(self):
        return self.doc_freq.keys()

    def get_term_freq_in_doc(self, doc_id, term):
        term_status = self.doc_freq[doc_id]["doc_freq"].get(term)
        return term_status["freq"] if term_status is not None else 0

    def get_top_docs(self, term):
        return [x[0] for x in self.term_top_docs.get(term, [])]

    def get_doc_max_freq(self, doc_id):
        return self.doc_freq[doc_id]["doc_max_term_freq"]

    def get_docs_freq(self, term):
        # print(term, self.term_top_docs.get(term, []))
        x = 0
        for doc in self.term_top_docs.get(term, []):
            x += doc[1]
        return x

    # def get_all_docs_freq(self):
    #     return self.all_docs_freq

    def get_docs_count(self):
        return self.index_meta["count"]

    def get_raw_docs(self):
        return self.raw_docs
