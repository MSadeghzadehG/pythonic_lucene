import pickle
from os.path import join
from heapq import nlargest

from search_engine.document.document import Document
from search_engine.document.field import Field

from os import makedirs


class IndexWriter:
    """
    An IndexWriter creates and maintains an index.

    Doc: https://lucene.apache.org/core/8_11_0/core/org/apache/lucene/index/IndexWriter.html
    Code: https://github.com/apache/lucene/blob/main/lucene/core/src/java/org/apache/lucene/index/IndexWriter.java
    """

    def __init__(
        self,
        name,
        analyzer,
        fields_to_index,
        num_of_top_docs,
        eliminate_docs=False,
    ):
        self.name = name
        self.analyzer = analyzer
        self.fields_to_index = fields_to_index
        self.eliminate_docs = eliminate_docs
        self.num_of_top_docs = num_of_top_docs
        self.term_top_docs = {}
        self.raw_docs = {}
        self.indexed_docs = {}
        self.count_of_docs = 0  # the count of index docs.

        try:
            makedirs(join(join("search_engine", "indices"), name))
        except FileExistsError:
            pass

    def add_document(self, raw_doc):
        """
        raw_doc: dict.
        """
        doc = Document(
            doc_id=self.count_of_docs,
            fields=[
                Field(
                    name=field_name,
                    to_store=(field_name in self.fields_to_index),
                    raw_data=val,
                )
                for field_name, val in raw_doc.items()
            ],
        )

        doc_freq, doc_max_term_freq = self.process_doc(
            doc.get_id(), doc.get_to_store_fields()
        )

        self.indexed_docs[doc.get_id()] = {
            "doc_freq": doc_freq,
            "doc_max_term_freq": doc_max_term_freq,
        }
        self.raw_docs[doc.get_id()] = doc
        self.count_of_docs += 1

    def add_documents(self, docs):
        """
        docs: list of dict.
        """
        list(map(self.add_document, docs))
        for term in self.term_top_docs.keys():
            self.term_top_docs[term] = nlargest(
                self.num_of_top_docs,
                self.term_top_docs[term].items(),
                key=lambda i: i[1],
            )
        self.write_docs()

    def write_docs(self):
        index_dir = join("search_engine/indices", self.name)
        with open(join(index_dir, "doc_index"), "wb") as f:
            pickle.dump(self.indexed_docs, f, protocol=pickle.HIGHEST_PROTOCOL)
        with open(join(index_dir, "term_top_docs"), "wb") as f:
            pickle.dump(self.term_top_docs, f, protocol=pickle.HIGHEST_PROTOCOL)
        with open(join(index_dir, "doc_raw"), "wb") as f:
            pickle.dump(self.raw_docs, f, protocol=pickle.HIGHEST_PROTOCOL)
        with open(join(index_dir, "index_meta"), "wb") as f:
            pickle.dump(
                {"count": self.count_of_docs},
                f,
                protocol=pickle.HIGHEST_PROTOCOL,
            )

    def process_field(self, field):
        field_freq = {}
        for token in self.analyzer.analyze_val(field.get_raw_data()):
            if token is not None:
                if token.value not in field_freq:
                    field_freq[token.value] = {"pos_list": [], "len_list": []}
                field_freq[token.value]["pos_list"].append(token.position)
                field_freq[token.value]["len_list"].append(token.length)
        return field_freq

    def process_doc(self, doc_id, fields):
        doc_freq = {}
        doc_max_term_freq = 0
        fields_freq = {f.name: self.process_field(f) for f in fields}
        for field_name, field_freq in fields_freq.items():
            for term, info in field_freq.items():
                if term not in doc_freq:
                    doc_freq[term] = {"freq": 0}
                if term not in self.term_top_docs:
                    self.term_top_docs[term] = {}
                if doc_id not in self.term_top_docs[term]:
                    self.term_top_docs[term][doc_id] = 0
                term_field_freq = len(info["pos_list"])
                doc_freq[term]["freq"] += term_field_freq
                self.term_top_docs[term][doc_id] += term_field_freq
                doc_freq[term]["fields"] = {field_name: info}
                if doc_freq[term]["freq"] > doc_max_term_freq:
                    doc_max_term_freq = doc_freq[term]["freq"]

        return doc_freq, doc_max_term_freq
