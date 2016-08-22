import _path_config

import sys

from gensim.corpora.wikicorpus import WikiCorpus
from gensim.corpora.dictionary import Dictionary
from gensim.models.tfidfmodel import TfidfModel
from gensim.corpora.mmcorpus import MmCorpus

if __name__ == '__main__':
    if len(sys.argv) not in range(3, 5):
        print('Usage: python3 build_wiki_dict wiki-pages-articles.xml.bz2 dict.pickle vectors.mm')
        print('Build tf-idf vectors of all documents in the given Wikipedia dump using the')
        print('given dictionary for idf values. Stores the result in matrix market format.')
    else:
        dump_fname = sys.argv[1]
        dict_fname = sys.argv[2]
        mm_fname = sys.argv[3]
        
        freq_dict = Dictionary.load(dict_fname)
        corpus = WikiCorpus(dump_fname, dictionary = freq_dict)
        tfidf = TfidfModel(dictionary = freq_dict)
        
        # Since metadata doesn't normally stay with a document when it's
        # transformed into tf-idf values, we have to implement it ourselves
        
        corpus.metadata = True
        metadata_queue = []
        
        class MetadataRemovedCorpus:
            def __init__(self, corpus):
                self.corpus = corpus
            def __iter__(self):
                for doc, metadata in self.corpus:
                    metadata_queue.append(metadata)
                    yield doc
            
        tfidf_corpus = tfidf[MetadataRemovedCorpus(corpus)]
        
        class MetadataAddedCorpus:
            def __init__(self, corpus):
                self.corpus = corpus
                self.metadata = True
            def __iter__(self):
                for doc in self.corpus:
                    yield doc, metadata_queue.pop()
                
        tfidf_metadata_corpus = MetadataAddedCorpus(tfidf_corpus)
        
        MmCorpus.serialize(mm_fname, tfidf_metadata_corpus, progress_cnt=10000,
                           metadata=True)
