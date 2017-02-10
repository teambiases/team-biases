import _path_config

import sys
import csv
from collections import defaultdict

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 mturk_sample_results.py results.csv scores.csv')
        print('Given a Mechanial Turk batch results CSV, computes bias scores for the chunks')
        print('annotated in those HITs and outputs them to scores.csv.')
    else:
        _, results_fname, scores_fname = sys.argv
        
        scores = defaultdict(list)
        with open(results_fname, 'r') as results_file:
            results_csv = csv.reader(results_file)
            header = next(results_csv)
            for row in results_csv:
                row_dict = dict(zip(header, row))
                chunk_id = (row_dict['Input.article'],
                            int(row_dict['Input.section_index']),
                            int(row_dict['Input.chunk_index']))
                scores[chunk_id].append(int(row_dict['Answer.us_bias']) -
                                        int(row_dict['Answer.soviet_bias']))
                
        with open(scores_fname, 'w') as scores_file:
            scores_csv = csv.writer(scores_file)
            scores_csv.writerow(['article', 'section_index', 'chunk_index',
                                 'score'])
            for (article, section_index, chunk_index), scores in \
                    scores.items():
                average_score = sum(scores) / len(scores)
                # Normalize from [-6, 6] to [0, 1]
                average_score = (average_score / 12) + 0.5
                scores_csv.writerow([article, section_index, chunk_index,
                                     average_score])
           