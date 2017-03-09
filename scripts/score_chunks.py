import _path_config

import sys
import pickle
import csv
import logging

from gensim.utils import tokenize

if __name__ == '__main__':
    if len(sys.argv) != 6:
        print('Usage: python3 biasmodel.pickle chunks.pickle sample.txt lang scores.csv')
        print('Loads the given bias model (should be an instance of biases.bias.BiasModel)')
        print('and uses it to score the bias of a the chunks in chunk.pickle whose chunk IDs')
        print('are specified in sample.txt and whose language is given. Writes the bias scores')
        print('to scores.csv.')
    else:
        _, bias_model_fname, chunks_fname, sample_fname, lang, \
                scores_fname = sys.argv
        
        # Load chunk IDs in sample
        sample_chunk_ids = set()
        with open(sample_fname, 'r') as sample_file:
            for line in sample_file:
                article, section_index, chunk_index = line.strip().split('\t')
                section_index = int(section_index)
                chunk_index = int(chunk_index)
                sample_chunk_ids.add((article, section_index, chunk_index))
            
        sample_articles = [article for article, section_index, chunk_index in
                           sample_chunk_ids]
        
        # Load chunks
        with open(chunks_fname, 'rb') as chunks_file:
            chunks = pickle.load(chunks_file)
            
        # Load bias model
        logging.info('loading bias model from %s', bias_model_fname)
        with open(bias_model_fname, 'rb') as bias_model_file:
            bias_model = pickle.load(bias_model_file)
        bias_model.load()
            
        logging.info('scoring %d chunks', len(sample_chunk_ids))
        with open(scores_fname, 'w') as scores_file:
            scores_csv = csv.writer(scores_file)
            scores_csv.writerow(['article', 'section_index', 'chunk_index',
                                 'score'])
            for sample_article in sample_articles:
                for chunk in chunks[sample_article]:
                    if chunk.id in sample_chunk_ids:
                        article, section_index, chunk_index = chunk.id
                        # Covert chunk to document format to pass to
                        # bias_model.predict
                        chunk_sents = []
                        for paragraph in chunk.paragraphs:
                            for sentence in paragraph:
                                chunk_sents.append(tokenize(sentence))
                        score = bias_model.predict(chunk_sents, lang)
                        scores_csv.writerow([article, section_index,
                                             chunk_index, score]) 
