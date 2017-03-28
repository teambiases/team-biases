import _path_config

import sys, logging, pickle
import numpy as np

from gensim.models import LdaModel
#from gensim.models.ldamodel import get_random_state
from gensim.corpora import MmCorpus

from biases.utils.math import sparse2dense

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print('Usage: python3 build_topics_corpus.py titles.txt tfidf.mm.bz2 lda.pickle corpus.pickle')
    else:
        _, titles_fname, vectors_fname, lda_fname, out_fname = sys.argv
        vectors_index_fname = vectors_fname[:-7] + '.index.pickle'
        
        with open(vectors_index_fname, 'rb') as vectors_index_file:
            vectors_index = pickle.load(vectors_index_file)
            vectors_index = [vectors_index[i] for i in
                             range(max(vectors_index.keys()))]
            
        with open(titles_fname, 'r') as titles_file:
            titles_set = set(title.strip() for title in
                             titles_file.readlines())
            logging.info('Loaded %d titles in corpus', len(titles_set))
            
        lda_model = LdaModel.load(lda_fname)
        #if not hasattr(lda_model, 'random_state'):
        #    lda_model.random_state = get_random_state(None)
        freq_dict = lda_model.id2word
        langs = []
        id2lang = {}
        for word_id in sorted(freq_dict.keys()):
            word = freq_dict[word_id]
            lang = word[:word.index('#')]
            id2lang[word_id] = lang
            if lang not in langs:
                langs.append(lang)
        logging.info('Found languages: %s', ', '.join(langs))
        
        corpora_topics = [[] for _ in langs]
        corpora_titles = [[] for _ in langs]
        
        vectors = MmCorpus(vectors_fname)
        for vector, titles in zip(vectors, vectors_index):
            if titles[0] in titles_set:
                lang_vectors = {lang: [] for lang in langs}
                for word_id, weight in vector:
                    lang_vectors[id2lang[word_id]].append((word_id, weight))
                for corpus_topics, corpus_titles, lang, title in \
                        zip(corpora_topics, corpora_titles, langs, titles):
                    lang_vector = lang_vectors[lang]
                    topics_vector = sparse2dense(lda_model[lang_vector],
                                                 lda_model.num_topics)
                    corpus_topics.append(topics_vector)
                    corpus_titles.append(title)
                    
        combined_corpora = []
        for lang, corpus_titles, corpus_topics in \
                zip(langs, corpora_titles, corpora_topics):
            combined_corpus = lang, corpus_titles, np.array(corpus_topics)
            combined_corpora.append(combined_corpus) 
        
        with open(out_fname, 'wb') as out_file:
            logging.info('Saving topics corpus to %s', out_fname)
            pickle.dump(combined_corpora, out_file)
          