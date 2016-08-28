import _path_config

import gensim, sys, logging

if __name__ == '__main__':
    if len(sys.argv) not in range(4, 6):
        print('Usage: python3 train_lda.py corpus.mm.bz2 dict.pickle model.lda.pickle (num_passes)')
        print('Train an LDA model over the given corpus using the given dictionary.')
        print('If num_passes is specified, makes multiple passes over the corpus.')
        print('See https://radimrehurek.com/gensim/wiki.html for details.')
    else:
        _, mm_fname, dict_fname, model_fname = sys.argv[:4]
        num_passes = 1
        if len(sys.argv) == 5:
            num_passes = int(sys.argv[4])
        
        mm = gensim.corpora.MmCorpus(mm_fname)
        id2word = gensim.corpora.Dictionary.load(dict_fname)
        
        lda_model = gensim.models.ldamodel.LdaModel(corpus=mm, id2word=id2word,
                num_topics=100, update_every=1, chunksize=10000,
                passes=num_passes)
        lda_model.save(model_fname)
