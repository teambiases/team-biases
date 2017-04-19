"""
Utilities having to do with the gensim library.
"""

import gensim, pickle
from gensim.models import LdaModel
from gensim.models.wrappers import LdaMallet

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

def load_lda_model(lda_fname):
    """
    Loads an LDA model that could either be a Gensim trained LdaModel or a
    MALLET wrapper (an instance of LdaMallet).
    """
    
    if lda_fname.endswith('.lda.pickle'):
        return LdaModel.load(lda_fname)
    elif lda_fname.endswith('.ldamallet.pickle'):
        return LdaMallet.load(lda_fname)
    else:
        raise ValueError('filename {} does not end with either .lda.pickle '
                         'or .ldamallet.pickle'.format(repr(lda_fname)))
