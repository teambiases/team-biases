import _path_config

import sys
import csv
import logging
import numpy as np
from scipy.stats.mstats import zscore

if __name__ == '__main__':
    if len(sys.argv) not in range(3, 5):
        print('Usage: python3 correlate_scores.py scores1.csv scores2.csv (verbose)')
        print('Reads the two files of chunk bias scores (as output by score_chunks.py or')
        print('mturk_results_to_scores.py) and logs the correlation between them to stdout.')
        print('If the argument verbose is specified then it will also print a list of')
        print('chunks in which the normalized bias (z-)scores deviated by the most to')
        print('assist in determining why the algorithm performed well or badly.')
    else:
        scores_fnames = sys.argv[1:3]
        verbose = len(sys.argv) >= 4 and sys.argv[3] == 'verbose'
        
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
            
            if verbose:
                zscores_vectors = [zscore(scores) for scores in scores_vectors]
                print('')
                print('{:<70} {:>10} {:>10}'.format('Chunk ID', 'Score 1',
                                                    'Score 2'))
                print('-' * 92)
                for index, score_diff in sorted(enumerate(np.abs(np.subtract(
                        *zscores_vectors))), reverse=True, key=lambda x: x[1]):
                    print('{:<70} {:>10.2f} {:>10.2f}'.format(
                            ' '.join(chunk_ids[index]), zscores_vectors[0][index],
                            zscores_vectors[1][index]))
