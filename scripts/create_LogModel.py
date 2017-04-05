import _path_config
import sys
from biases.bias.topics import LogisticTopicsBiasModel
import pickle

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: python3 topicsmatrix.pickle ldamodel.pickle thisLogisticmodel.pickle')
        print('Run this script to create the Logistic Bias model, which you can then use')
        print('in score_chunks.py')

    else:
        _, topic_corpus_fname, topic_model_fname, model_fname = sys.argv

        bias_model = LogisticTopicsBiasModel(topic_corpus_fname, topic_model_fname, model_fname)
        bias_model.train()

        with open(model_fname, 'wb') as bias_model_file:
            pickle.dump(bias_model, bias_model_file)


'''
Relevant inputs:
topic_corpus_fname = '/team-biases/data/wikipedia/corpus/coldwar.es-en-ru-wiki-20170120.100topics.pickle' or 'coldwar.es-en-ru-wiki-20160820.400topics.pickle'
topic_model_fname = '/team-biases/data/lda/es-en-ru-wiki-20170120.parallel.100t.lda.pickle' or 'es-en-ru-wiki-20160820.parallel.400t.lda.pickle'
model_fname = '/team-biases/data/lda/test_log_model.pickle'


Relevant command: 
python create_LogModel.py '/Users/elliotgoldingfrank/team-biases/data/wikipedia/corpus/coldwar.es-en-ru-wiki-20170120.400topics.pickle' '/Users/elliotgoldingfrank/team-biases/data/lda/es-en-ru-wiki-20170120.parallel.400t.lda.pickle' '/Users/elliotgoldingfrank/team-biases/data/lda/test_log_model.20170120.400t.pickle'
''' 

