from collections import Counter

from .similarity import TFIDFSimilarity


class IndexSearcher:
    '''
    Implements search over a single IndexReader.
    Applications usually need only call the inherited search(Query,int) method.

    Doc: https://lucene.apache.org/core/8_11_0/core/org/apache/lucene/search/IndexSearcher.html
    Code: https://github.com/apache/lucene/blob/main/lucene/core/src/java/org/apache/lucene/search/IndexSearcher.java
    '''
    def __init__(self, index_reader, analyzer):
        self.reader = index_reader
        self.analyzer = analyzer
        self.similarity = TFIDFSimilarity()

    def search_token(self, token):
        df = self.reader.get_docs_freq(token.value)
        n = self.reader.get_docs_count()
        idf_val = self.similarity.idf(df, n)

        all_fields_score = {}
        for doc_id in self.reader.get_docs_id():
            score = self.similarity.score(
                freq=self.reader.get_term_freq_in_doc(doc_id,token.value),
                idf_val=idf_val,
                boost=1,
                norm=self.reader.get_doc_max_freq(doc_id)
            )
            if score != 0:
                all_fields_score[doc_id] = score

        return all_fields_score

    # public LucenePageResults search(final Query qry,Set<SortField> sortFields, final int firstResultItemOrder,final int numberOfResults) {
    def search(self, query, number_of_results, retrievable_fields):
        analyzed_query = self.analyzer.analyze_val(query)
        tokens_result = [
            self.search_token(token) 
            for token in analyzed_query
        ]
        aggregated_token_result = Counter()
        for result in tokens_result:
            aggregated_token_result.update(result)
        
        docs = self.reader.get_raw_docs()
        
        sorted_result = dict(sorted(
            aggregated_token_result.items(),
            key=lambda x: x[1],
            reverse=True
        )[:number_of_results])

        filtered_result = {
            docs[doc_id].get_raw_field(retrievable_field): score
            for doc_id, score in sorted_result.items()
            for retrievable_field in retrievable_fields
        }

        return filtered_result
