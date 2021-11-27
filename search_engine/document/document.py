import uuid


class Document:
    '''
    Documents are the unit of indexing and search. 
    A Document is a set of fields. Each field has a name and a textual value.
    A field may be stored with the document, in which case it is returned with search hits on the document.
    Thus each document should typically contain one or more stored fields which uniquely identify it.

    Note that fields which are not stored are not available in documents retrieved from the index.

    Doc: https://lucene.apache.org/core/8_11_0/core/org/apache/lucene/document/Document.html
    Code: https://github.com/apache/lucene/blob/main/lucene/core/src/java/org/apache/lucene/document/Document.java
    '''

    def __init__(self, fields, doc_id=None):
        '''
        fields: a list of Field.
        '''
        self.fields = fields
        self.fields_dict = {f.name: f for f in fields}
        self.id = str(doc_id) if doc_id is not None else str(uuid.uuid4())
        self.to_store_fields = [
            f for f in fields if f.get_to_store() is True
        ]

    def get_id(self):
        return self.id

    def get_raw_field(self, field_name):
        return self.fields_dict[field_name].get_raw_data()

    def get_to_store_fields(self):
        return self.to_store_fields
