#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import time

from ujson import dumps
from os.path import join
import matplotlib.pyplot as plt

from search_engine.index.index_writer import IndexWriter
from search_engine.index.index_reader import IndexReader
from search_engine.search.index_searcher import IndexSearcher
from search_engine.analyzer.tokenizer import StandardTokenizer
from search_engine.analyzer.analyzer import Analyzer
from search_engine.analyzer.char_filter import WhitespcaesCharFilter
from persian_char_filters import PersianCharFilter, BadCharFilter
from persian_token_filters import (
    PersianStopFileFilter,
    PersianStemFilter,
    PersianNormalizeFilter,
    RemoveSpaceFilter,
)


def read_excel():
    df = pd.read_excel("../IR1_7k_news.xlsx", sheet_name=None)["Sheet1"]
    print(df)
    return df


def write_index(analyzer, num_of_top_docs):
    index = IndexWriter(
        name="test",
        analyzer=analyzer,
        fields_to_index=["content"],
        num_of_top_docs=num_of_top_docs,
    )
    df = read_excel()
    st = time.perf_counter()
    index.add_documents([r.to_dict() for _, r in df.iterrows()])
    print(time.perf_counter() - st)


def search_queries(index_searcher):
    queries = [
        "واکسن آسترازنکا",
        "ژیمناستیک",
        "بین‌الملل",
        "دانشگاه امیرکبیر",
        "جمهوری اسلامی ایران",
        "سازمان ملل متحد",
        "دانشگاه صنعتی امیرکبیر",
    ]
    for q in queries:
        with open(join("test_results", q) + ".json", "w") as f:
            start_time = time.perf_counter()
            results = index_searcher.search(
                query=q,
                number_of_results=10,
                retrievable_fields=["title", "content"],
            )
            elapsed_time = time.perf_counter() - start_time
            filtered_results = {
                result["fields"]["title"]: {
                    "score": result["score"],
                    "content": result["fields"]["content"],
                    "matched_terms": [
                        (s.value, s.position)
                        for s in index_searcher.analyzer.analyze_val(
                            result["fields"]["content"]
                        )
                        for a_q in index_searcher.analyzer.analyze_val(q)
                        if a_q and s and a_q.value == s.value
                    ],
                }
                for doc_id, result in results.items()
            }
            f.write(
                dumps(
                    {
                        "query": q,
                        "elapsed_time": elapsed_time,
                        "top 10 results": filtered_results,
                    },
                    ensure_ascii=False,
                    indent=4,
                )
            )


def main():
    analyzer = Analyzer(
        char_filters=[
            WhitespcaesCharFilter(),
            BadCharFilter(),
            PersianCharFilter(),
        ],
        tokenizer=StandardTokenizer(),
        token_filters=[
            RemoveSpaceFilter(),
            PersianNormalizeFilter(),
            PersianStopFileFilter("persian_stops.txt"),
            PersianStemFilter(),
        ],
    )

    # write_index(analyzer=analyzer, num_of_top_docs=50)

    index_reader = IndexReader(name="test")

    index_searcher = IndexSearcher(
        index_reader=index_reader, analyzer=analyzer, just_top_docs=True
    )
    search_queries(index_searcher)


if __name__ == "__main__":
    main()
