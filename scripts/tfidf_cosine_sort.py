import _path_config

import sys
import logging
import pickle
import gensim
import csv
from biases.utils.math import cosine_similarity

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: python3 tfidf_cosine_sort.py corpus.mm.bz2 sorted.csv article_title')
        print('Given a matrix market format corpus, sorts all the articles by their tfidf')
        print('cosine similarity to a given article (specified by article_title). Outputs as a')
        print('CSV file with similarity values and titles.')
    else:
        _, mm_fname, out_fname, seed_article_title = sys.argv
        
        # Get vector metadata and index
        meta_fname = mm_fname[:-4] + '.metadata.cpickle'
        with open(meta_fname, 'rb') as meta_file:
            metadata = pickle.load(meta_file)
        index_fname = mm_fname[:-4] + '.index'
        with open(index_fname, 'rb') as index_file:
            index = pickle.load(index_file)
        
        # Get offset of seed article
        seed_article_offset = None
        for article_index, offset in enumerate(index):
            article_id, article_title = metadata[article_index]
            if article_title == seed_article_title:
                seed_article_offset = offset
                
        # Load seed article
        mm = gensim.corpora.MmCorpus(mm_fname)
        if seed_article_offset is None:
            logging.error('Seed article "%s" not found', seed_article_title)
        else:
            logging.info('Loading seed article "%s"', seed_article_title)
            seed_article = dict(mm.docbyoffset(seed_article_offset))
            
            titles_similarities = [] # List of (title, similarity)
            logging.info('Calculating similarities to seed article')
            for article_index, article in enumerate(mm):
                article_id, article_title = metadata[article_index]
                article = dict(article)
                similarity = cosine_similarity(seed_article, article)
                titles_similarities.append((article_title, similarity))
            
            logging.info('Sorting articles by similarity')
            titles_similarities.sort(key = lambda x: x[1], reverse = True)
            
            logging.info('Writing results to %s', out_fname)
            with open(out_fname, 'w') as out_file:
                out = csv.writer(out_file)
                out.writerow(['Title', 'Similarity'])
                for row in titles_similarities:
                    out.writerow(row)
    