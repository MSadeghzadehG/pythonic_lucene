class Field:
    '''
    A field is a section of a Document.

    Doc: https://lucene.apache.org/core/8_11_0/core/org/apache/lucene/document/Field.html
    Code: https://github.com/apache/lucene/blob/main/lucene/core/src/java/org/apache/lucene/document/Field.java
    '''
    def __init__(self, name, raw_data, to_store=False):
        self.name = name
        self.to_store = to_store
        self.raw_data = raw_data

    def get_to_store(self):
        return self.to_store

    def get_raw_data(self):
        return self.raw_data
