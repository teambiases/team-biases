import _path_config

import sys
import logging
import os

from os.path import sep
from gensim.corpora import MmCorpus, Dictionary
from gensim.models.wrappers import LdaMallet

def reverse_tfidf(corpus):
    for doc in corpus:
        yield [(word, value * 200) for word, value in doc]
        
DICT_SIZE = 100000
        
def normalize_langs(corpus):
    """
    Normalizes the given corpus so that each language has the same number of
    words for a given article.
    """
    
    for doc in corpus:
        doc.sort()
        lang_docs = []
        while len(doc) > 0:
            lang_index = doc[0][0] // DICT_SIZE
            lang_doc = []
            while len(doc) > 0 and doc[0][0] // DICT_SIZE == lang_index:
                lang_doc.append(doc.pop(0))
            lang_docs.append(lang_doc)
                
        lang_lengths = [sum(freq for word, freq in lang_doc) for lang_doc
                         in lang_docs]
        max_length = max(lang_lengths)
        normalized_doc = []
        for lang_doc, lang_length in zip(lang_docs, lang_lengths):
            for word, freq in lang_doc:
                normalized_doc.append((word, freq * max_length /
                                       lang_length))
        yield normalized_doc

if __name__ == '__main__':
    if len(sys.argv) not in range(4, 6):
        print('Usage: python3 train_lda.py corpus.bow.mm.bz2 dict.pickle model.lda.pickle (num_topics)')
        print('Train an LDA model over the given corpus using the given dictionary.')
        print('If num_topics is not specified, use the default of 100.')
        print('If num_passes is specified, makes multiple passes over the corpus.')
        print('This uses MALLET to train a topic model.')
    else:
        _, mm_fname, dict_fname, model_fname = sys.argv[:4]
        num_topics = int(sys.argv[4]) if len(sys.argv) >= 5 else 100
        
        try:
            mallet_path = sep.join([os.environ['MALLET_HOME'], 'bin', 'mallet'])
        except KeyError:
            logging.error('please set the MALLET_HOME environment variable to '
                          'the root directory of your MALLET installation')
            exit()
        
        mm = MmCorpus(mm_fname)
        id2word = Dictionary.load(dict_fname)
        
        lda_model = LdaMallet(mallet_path, corpus=normalize_langs(mm), 
                id2word=id2word, num_topics=num_topics)
        lda_model.save(model_fname)
