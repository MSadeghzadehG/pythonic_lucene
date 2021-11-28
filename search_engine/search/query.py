from enum import Enum


class Query:
    '''
    The abstract base class for queries.

    Doc: https://lucene.apache.org/core/8_11_0/core/org/apache/lucene/search/Query.html
    Code: https://github.com/apache/lucene/blob/main/lucene/core/src/java/org/apache/lucene/search/Query.java
    '''
    def __init__(self, boost):
        self.boost = boost

    def get_weight(self):
        return self.boost


class BooleanOccur(Enum):
        FILTER = 1
        MUST = 2
        MUST_NOT = 3
        SHOULD = 4


class BooleanClause:
    def __init__(self, query, occur):
        '''
        query: Query, occur: BooleanOccur
        '''
        self.query = query
        self.occur = occur


class TermQuery(Query):
    
    def __init__(self, boost, term):
        super(TermQuery, self).__init__(boost)
        self.term = term


class BooleanQuery(Query):
    '''
    A Query that matches documents matching boolean combinations of other queries, e.g. TermQuerys, PhraseQuerys or other BooleanQuerys.

    Doc: https://lucene.apache.org/core/8_11_0/core/org/apache/lucene/search/BooleanQuery.html
    Code: https://github.com/apache/lucene/blob/main/lucene/core/src/java/org/apache/lucene/search/BooleanQuery.java
    '''

    def __init__(self, boost, clauses):
        '''
        clauses: a list of BooleanClause
        '''
        super(BooleanQuery, self).__init__(boost)
        self.clauses = clauses

    def add_clause(self, query, occur):
        self.clauses.append(
            BooleanClause(query, occur)
        )
