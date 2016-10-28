"""
Utilities having to do with the gensim library.
"""

import gensim, pickle

def load_mm_corpus(mm_fname):
    """
    Given the filename of a matrix-market corpus, returns a 3-tuple
    (mm_corpus, metadata, index) by loading the corpus file as well as the
    metadata and index files.
    """
    
    mm = gensim.corpora.MmCorpus(mm_fname)
    meta_fname = mm_fname[:-4] + '.metadata.cpickle'
    with open(meta_fname, 'rb') as meta_file:
        metadata = pickle.load(meta_file)
    index_fname = mm_fname[:-4] + '.index'
    with open(index_fname, 'rb') as index_file:
        index = pickle.load(index_file)
    corpus = (mm, metadata, index)
    return corpus
