import _path_config

import sys
import csv
import logging
import numpy as np

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 correlate_scores.py scores1.csv scores2.csv')
        print('Reads the two files of chunk bias scores (as output by score_chunks.py or')
        print('mturk_results_to_scores.py) and logs the correlation between them to stdout.')
    else:
        scores_fnames = sys.argv[1:]
        
        scores_dicts = []
        for scores_fname in scores_fnames:
            scores_dict = {}
            with open(scores_fname, 'r') as scores_file:
                scores_csv = csv.reader(scores_file)
                next(scores_csv) # Ignore header
                for article, section_index, chunk_index, score in scores_csv:
                    score = float(score)
                    scores_dict[(article, section_index, chunk_index)] = score
            scores_dicts.append(scores_dict)
                    
        if scores_dicts[0].keys() != scores_dicts[1].keys():
            logging.error('scores are not over the same chunks')
        else:
            chunk_ids = list(scores_dicts[0].keys())
            scores_vectors = [[scores_dict[chunk_id] for chunk_id in chunk_ids]
                              for scores_dict in scores_dicts]
            r = np.corrcoef(*scores_vectors)[0,1]
            logging.info('r = %f', r)
            logging.info('r^2 = %f', r ** 2)
