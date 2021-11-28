# Pythonic Lucene
a simplified python impelementaiton of [Apache Lucene](https://github.com/apache/lucene) search engine, mabye helps to understand how an enterprise search engine really works.

Usually, the companies don't use Lucene; but use [ElasticSearch](https://github.com/elastic/elasticsearch), the distributed and RESTful wrapper of Lucene.


## analyzer TODO
- [x] tokenizer -> generator
- [ ] Analyzer -> factory class that creates TokenGraphs when needed. 

## index TODO
- [ ] index structure: index -> set of segments -> set of docs -> set of fields -> set of terms
- [ ] index -> FST
- [ ] then construct the inverted table through the add method under the TermsHashPerField, and finally store the relevant data of the Field in the freqProxPostingsArray of the type FreqProxPostingsArray, and the termVectorsPostingsArray of the TermVectorsPostingsArray, Constitute an inverted list;
- [ ] index write buffer and flush
- [ ] segment merge
- [ ] index config
