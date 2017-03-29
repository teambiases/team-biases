import _path_config

import sys

from gensim.corpora.wikicorpus import WikiCorpus
from gensim.corpora.dictionary import Dictionary
from gensim.models.tfidfmodel import TfidfModel
from gensim.corpora.mmcorpus import MmCorpus

if __name__ == '__main__':
    if len(sys.argv) not in range(4, 6):
        print('Usage: python3 build_wiki_vectors.py wiki-pages-articles.xml.bz2 dict.pickle vectors.mm (vectorformat)')
        print('Build  vectors of all documents in the given Wikipedia dump using the')
        print('given dictionary. Stores the result in matrix market format.')
        print('Uses tf-idf for vectors unless vectorformat is specified as bow, in which case')
        print('outputs a bag-of-words representation.')
    else:
        dump_fname = sys.argv[1]
        dict_fname = sys.argv[2]
        mm_fname = sys.argv[3]
        vector_format = sys.argv[4] if len(sys.argv) >= 5 else 'tfidf'
        
        freq_dict = Dictionary.load(dict_fname)
        wiki_corpus = WikiCorpus(dump_fname, dictionary = freq_dict)
        tfidf = TfidfModel(dictionary = freq_dict)
        
        # Since metadata doesn't normally stay with a document when it's
        # transformed into tf-idf values, we have to implement it ourselves
        
        wiki_corpus.metadata = True
        metadata_queue = []
        
        class MetadataRemovedCorpus:
            def __init__(self, corpus):
                self.corpus = corpus
            def __iter__(self):
                for doc, metadata in self.corpus:
                    metadata_queue.append(metadata)
                    yield doc
            
        tfidf_corpus = tfidf[MetadataRemovedCorpus(wiki_corpus)]
        
        class MetadataAddedCorpus:
            def __init__(self, corpus):
                self.corpus = corpus
                self.metadata = True
            def __iter__(self):
                for doc in self.corpus:
                    yield doc, metadata_queue.pop()
                
        tfidf_metadata_corpus = MetadataAddedCorpus(tfidf_corpus)
        
        if vector_format == 'tfidf':
            corpus = tfidf_metadata_corpus
        elif vector_format == 'bow':
            corpus = wiki_corpus
        
        MmCorpus.serialize(mm_fname, corpus, progress_cnt=10000, metadata=True)
