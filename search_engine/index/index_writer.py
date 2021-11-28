import numpy as np
import pickle
from os.path import join

from search_engine.document.document import Document
from search_engine.document.field import Field

from os import makedirs


class IndexWriter:
    '''
    An IndexWriter creates and maintains an index.

    Doc: https://lucene.apache.org/core/8_11_0/core/org/apache/lucene/index/IndexWriter.html
    Code: https://github.com/apache/lucene/blob/main/lucene/core/src/java/org/apache/lucene/index/IndexWriter.java
    '''
    
    def __init__(self, name, analyzer, fields_to_index):
        self.name = name
        self.analyzer = analyzer
        self.fields_to_index = fields_to_index 
        
        # all docs index info
        self.all_docs_freq = {}  # the set of docs that containing an specific term.
        self.count_of_docs = 0  # the count of index docs.

        self.raw_docs = {}
        self.indexed_docs = {}
        try:
            makedirs(join(join('search_engine', 'indices'), name))
        except FileExistsError:
            pass

    def add_document(self, raw_doc): 
        '''
        raw_doc: dict.
        '''
        doc = Document(
            doc_id = self.count_of_docs,
            fields=[
                Field(
                    name=field_name,
                    to_store=(field_name in self.fields_to_index),
                    raw_data=val,
                )
                for field_name, val in raw_doc.items()
            ]
        )

        doc_freq = self.process_doc(doc.get_id(), doc.get_to_store_fields())
        max_term_freq = 0
        for term in doc_freq:
            if term not in self.all_docs_freq:
                self.all_docs_freq[term] = 0
            self.all_docs_freq[term] += doc_freq[term]['docs']
            if doc_freq[term]['freq'] > max_term_freq:
                max_term_freq = doc_freq[term]['freq']

        self.indexed_docs[doc.get_id()] = {'doc_freq': doc_freq, 'max_term_freq': max_term_freq}
        self.raw_docs[doc.get_id()] = doc
        self.count_of_docs += 1

    def add_documents(self, docs):
        '''
        docs: list of dict.
        '''
        list(map(self.add_document, docs))
        self.write_docs()

    def write_docs(self):
        with open(join(join('search_engine/indices', self.name), 'doc_index'), 'wb') as f:
            pickle.dump(self.indexed_docs, f, protocol=pickle.HIGHEST_PROTOCOL)
        with open(join(join('search_engine/indices', self.name), 'doc_raw'), 'wb') as f:
            pickle.dump(self.raw_docs, f, protocol=pickle.HIGHEST_PROTOCOL)
        with open(join(join('search_engine/indices', self.name), 'all_docs_index'), 'wb') as f:
            pickle.dump(
                {
                    'count': self.count_of_docs,
                    'docs_freq': self.all_docs_freq
                },
                f, protocol=pickle.HIGHEST_PROTOCOL
            )

    def process_field(self, field):
        field_freq = {}
        for token in self.analyzer.analyze_val(field.get_raw_data()):
            if token.value not in field_freq:
                field_freq[token.value] = {'pos_list': [], 'len_list': []}
            field_freq[token.value]['pos_list'].append(token.position)
            field_freq[token.value]['len_list'].append(token.length)
        return field_freq

    def process_doc(self, doc_id, fields):
        doc_freq = {}
        fields_freq = [(f, self.process_field(f)) for f in fields]
        for field_freq in fields_freq:
            for term, info in field_freq[1].items():
                if term not in doc_freq:
                    doc_freq[term] = {'docs':set([]), 'freq': 0}
                doc_freq[term]['docs'].add(doc_id)
                doc_freq[term]['freq'] += len(info['pos_list'])
                doc_freq[term]['fields'] = {field_freq[0].name: info}
        for _, term  in doc_freq.items():
            term['docs'] = len(term['docs'])
        return doc_freq
