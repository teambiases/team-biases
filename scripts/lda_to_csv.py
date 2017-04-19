import _path_config

import sys, gensim, csv

from biases.utils.gensim import load_lda_model

NUM_WORDS = 100

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 lda_to_csv.py model.lda.pickle topics.csv')
        print('Given an LDA topic model, generate a human-readable CSV representation')
    else:
        _, lda_fname, csv_fname = sys.argv
        
        lda = load_lda_model(lda_fname)
        with open(csv_fname, 'w') as csv_file:
            csv_out = csv.writer(csv_file)
            csv_out.writerow(['Topic ID', 'Top words'])
            for topic_id in range(lda.num_topics):
                row = [topic_id]
                row += [word for word, prob in
                        lda.show_topic(topic_id, num_words = NUM_WORDS)]
                csv_out.writerow(row)
    