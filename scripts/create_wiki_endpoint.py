import _path_config

import sys
import pickle
import logging
import nltk

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 create_wiki_endpoint.py chunks.pickle endpoint.txt')
        print('Extracts all the sentences in the given chunks and writes them to endpoint.txt,')
        print('one sentence per line, tokenized with spaces between tokens. This output can')
        print('then be passed to train_gentzkow_shapiro.py.')
    else:
        _, chunks_fname, endpoint_fname = sys.argv
        
        logging.info('reading chunks from %s...', chunks_fname)
        with open(chunks_fname, 'rb') as chunks_file:
            chunks = pickle.load(chunks_file)
            
        logging.info('writing sentences to %s...', endpoint_fname)
        with open(endpoint_fname, 'w') as endpoint_file:
            for _, article_chunks in chunks.items():
                for chunk in article_chunks:
                    for paragraph in chunk.paragraphs:
                        for sentence in paragraph:
                            endpoint_file.write(' '.join(
                                    nltk.word_tokenize(sentence)) + '\n')
            
