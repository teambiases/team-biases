import _path_config

import sys
import pickle
import csv
import numpy as np
import gensim

# Use same number of words as lda_to_csv.py uses
from lda_to_csv import NUM_WORDS

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: python3 analyze_topics_corpus.py corpus.topics.pickle lda.pickle output.csv')
        print('Analyzes the topic distribution across the languages present in corpus.topics.pickle')
        print('as outputted by build_topics_corpus.py. Outputs the prevalence of each topic in each')
        print('language, along with representative words for that topic, to output.csv.')
    else:
        _, topics_corpus_fname, lda_fname, output_fname = sys.argv
        
        with open(topics_corpus_fname, 'rb') as topics_corpus_file:
            topics_corpus = pickle.load(topics_corpus_file)
        lda = gensim.models.LdaModel.load(lda_fname)
            
        langs = [lang for lang, titles, topics in topics_corpus]
            
        with open(output_fname, 'w') as output_file:
            csv_out = csv.writer(output_file)
            
            header_row = ['Topic ID']
            header_row += ['{} average prevalence'.format(lang.upper())
                           for lang in langs]
            header_row += ['{} highest article'.format(lang.upper())
                           for lang in langs]
            header_row += ['Top words']
            
            csv_out.writerow(header_row)
            for topic_id in range(lda.num_topics):
                prevalences = []
                highest_articles = []
                
                for lang, titles, topics in topics_corpus:
                    # Calculate average prevalence
                    prevalences.append(float(np.mean(topics[:, topic_id])))
                    # Calculate highest article
                    highest_article_index = np.argmax(topics[:, topic_id])
                    highest_article_title = titles[highest_article_index]
                    highest_article_prevalence = \
                            topics[highest_article_index, topic_id]
                    highest_articles.append('{} ({:.2f})'.format(
                            highest_article_title, highest_article_prevalence))
                    
                row = [topic_id]
                row += prevalences
                row += highest_articles
                row += [word for word, prob in
                        lda.show_topic(topic_id, topn = NUM_WORDS)]
                csv_out.writerow(row)
