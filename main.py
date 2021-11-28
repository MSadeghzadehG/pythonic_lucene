#!/usr/local/bin/python3
# -*- coding: utf-8 -*- 
import pandas as pd
import time

from ujson import dumps
from os.path import join

from search_engine.index.index_writer import IndexWriter
from search_engine.index.index_reader import IndexReader
from search_engine.search.index_searcher import IndexSearcher
from search_engine.analyzer.tokenizer import StandardTokenizer
from search_engine.analyzer.analyzer import Analyzer
from persian_char_filters import PersianCharFilter, BadCharFilter
from persian_token_filters import (
    PersianStopFilter, PersianStemFilter, PersianNormalizeFilter
)


def read_excel():
    df = pd.read_excel('IR1_7k_news.xlsx', sheet_name=None)['Sheet1']
    print(df)
    return df


def main():
    analyzer = Analyzer(
        char_filters=[BadCharFilter()],
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
    
    index_reader = IndexReader(name='test')
    # docs_freq = index_reader.get_all_docs_freq()
    # print(docs_freq)

    index_searcher = IndexSearcher(
        index_reader=index_reader,
        analyzer=analyzer
    )

    queries = [ 'واکسن آسترازنکا' , 'ژیمناستیک' , 'بین‌الملل' , 'دانشگاه امیرکبیر' , 'جمهوری اسلامی ایران' , 'سازمان ملل متحد' , 'دانشگاه صنعتی امیرکبیر' ]
    for q in queries:
        with open(join('test_results', q) + '.json', 'w') as f: 
            start_time = time.perf_counter() 
            results = index_searcher.search(
                query=q,
                number_of_results=10,
                retrievable_fields=['title']
            )
            elapsed_time = time.perf_counter() - start_time
            f.write(dumps(
                {
                    'query': q,
                    'elapsed_time': elapsed_time, 
                    'top 10 results': results
                },
                ensure_ascii=False,
                indent=4
            ))



if __name__ == "__main__":
    main()
