#!/usr/local/bin/python3
# -*- coding: utf-8 -*- 
import pandas as pd
import time

from search_engine.index.index_writer import IndexWriter
from search_engine.index.index_reader import IndexReader
from search_engine.search.index_searcher import IndexSearcher
from search_engine.analyzer.tokenizer import StandardTokenizer
from search_engine.analyzer.analyzer import Analyzer
from persian_char_filters import PersianCharFilter
from persian_token_filters import (
    PersianStopFilter, PersianStemFilter, PersianNormalizeFilter
)


def read_excel():
    df = pd.read_excel('IR1_7k_news.xlsx', sheet_name=None)['Sheet1']
    print(df)
    return df


def main():
    analyzer = Analyzer(
        char_filters=[PersianCharFilter()],
        tokenizer=StandardTokenizer(),
        token_filters=[
            PersianStopFilter('persian_stops.txt'),
            PersianNormalizeFilter(),
            PersianStemFilter()
        ]
    )
    
    index = IndexWriter(
        name='test',
        analyzer=analyzer,
        fields_to_index=['content']
    )
    df = read_excel()
    st = time.perf_counter() 
    index.add_documents([r.to_dict() for _,r in df.iterrows()])
    # index.add_documents([{'content': 'in the name of god.'}, {'content': 'in practice it is needed to trust god!'}])
    print(time.perf_counter() -st)
    index_searcher = IndexSearcher(
        index_reader=IndexReader(name='test'),
        analyzer=analyzer
    )

    st = time.perf_counter() 
    print(index_searcher.search(
        query='ژیمناستیک',
        number_of_results=10,
        retrievable_fields=['title']
    ))
    print(time.perf_counter()-st)


if __name__ == "__main__":
    main()
