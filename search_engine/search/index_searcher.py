from heapq import nlargest
from collections import Counter

from .similarity import TFIDFSimilarity


class IndexSearcher:
    """
    Implements search over a single IndexReader.
    Applications usually need only call the inherited search(Query,int) method.

    Doc: https://lucene.apache.org/core/8_11_0/core/org/apache/lucene/search/IndexSearcher.html
    Code: https://github.com/apache/lucene/blob/main/lucene/core/src/java/org/apache/lucene/search/IndexSearcher.java
    """

    def __init__(
        self, index_reader, analyzer, score_threshold=0.01, just_top_docs=True
    ):
        self.reader = index_reader
        self.analyzer = analyzer
        self.score_threshold = score_threshold
        self.similarity = TFIDFSimilarity()
        self.just_top_docs = just_top_docs

    def search_token(self, token):
        df = self.reader.get_docs_freq(token.value)
        n = self.reader.get_docs_count()
        idf_val = self.similarity.idf(df, n)

        all_fields_score = {}

        target_docs = (
            self.reader.get_top_docs(token.value)
            if self.just_top_docs
            else self.reader.get_docs_id()
        )

        for doc_id in target_docs:
            if self.reader.get_doc_max_freq(doc_id) != 0:
                score = self.similarity.score(
                    freq=self.reader.get_term_freq_in_doc(doc_id, token.value),
                    idf_val=idf_val,
                    boost=1,
                    norm=self.reader.get_doc_max_freq(doc_id),
                )
                if score >= self.score_threshold:
                    all_fields_score[doc_id] = score

        return all_fields_score

    # public LucenePageResults search(final Query qry,Set<SortField> sortFields, final int firstResultItemOrder,final int numberOfResults) {
    def search(
        self, query, number_of_results, retrievable_fields, min_token=None
    ):
        analyzed_query = self.analyzer.analyze_val(query)
        tokens_result = [
            self.search_token(token)
            for token in analyzed_query
            if token is not None
        ]

        has_min_tokens = []
        if min_token is not None:
            aggregated_results = []
            for token_result in tokens_result:
                aggregated_results += token_result
            has_min_tokens = [
                item
                for item, count in Counter(aggregated_results).items()
                if count >= min_token
            ]

        aggregated_token_result = tokens_result[0]
        for result in tokens_result[1:]:
            aggregated_token_result = {
                k: s0 + s1
                for k, s0 in result.items()
                for j, s1 in aggregated_token_result.items()
                if k == j
                and ((min_token and j in has_min_tokens) or not min_token)
            }
        docs = self.reader.get_raw_docs()

        sorted_result = nlargest(
            number_of_results,
            aggregated_token_result.items(),
            key=lambda i: i[1],
        )

        filtered_result = {
            result[0]: {
                "score": result[1],
                "fields": {
                    retrievable_field: docs[result[0]].get_raw_field(
                        retrievable_field
                    )
                    for retrievable_field in retrievable_fields
                },
            }
            for result in sorted_result
        }

        return filtered_result
