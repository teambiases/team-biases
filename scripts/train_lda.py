import _path_config

import gensim, sys, logging

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: python3 train_lda.py corpus.mm.bz2 dict.pickle model.lda.pickle')
        print('Train an LDA model over the given corpus using the given dictionary.')
        print('See https://radimrehurek.com/gensim/wiki.html for details.')
    else:
        _, mm_fname, dict_fname, model_fname = sys.argv
        
        mm = gensim.corpora.MmCorpus(mm_fname)
        id2word = gensim.corpora.Dictionary.load(dict_fname)
        
        lda_model = gensim.models.ldamodel.LdaModel(corpus=mm, id2word=id2word,
                num_topics=100, update_every=1, chunksize=10000, passes=1)
        lda_model.save(model_fname)
