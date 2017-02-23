import _path_config

import csv
import sys
import itertools
from collections import Counter, defaultdict
import numpy as np

from biases.annotation.agreement import average_agreement

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 annotator_agreement.py results.csv out.txt')
        print('Uses nltk\'s metrics.agreement module to calculate the inter-annotator')
        print('agreement in the given Mechanical Turk results and writes it to the output')
        print('text file.')
    else:
        _, results_fname, out_fname = sys.argv
        
        results = defaultdict(list)
        with open(results_fname, 'r') as results_file:
            results_csv = csv.reader(results_file)
            header = next(results_csv)
            for row in results_csv:
                row_dict = dict(zip(header, row))
                hit_id = row_dict['HITId']
                results[hit_id].append(row_dict)
                
        with open(out_fname, 'w') as out_file:
            out_file.write('= SENTENCE TAGS =\n')
            sentence_tags = []
            for hit_id, rows in results.items():
                sentences_answers = [map(int, row['Answer.sentences'])
                                     for row in rows]
                sentence_tags.extend(map(list, zip(*sentences_answers)))
            out_file.write('== Agreement ==\n')
            out_file.write('All sentences: {:0.3f}\n'.format(
                    average_agreement(sentence_tags)))
            out_file.write('Sentences with >=1 non-neutral tag: {:0.3f}\n'
                    .format(average_agreement([tags for tags in sentence_tags
                                               if len(set(tags) - {0}) > 0])))
            out_file.write('Sentences with >=2 different non-neutral tags: {:0.3f}\n'
                    .format(average_agreement([tags for tags in sentence_tags
                                               if len(set(tags) - {0}) >= 2])))
            tag_counts = Counter()
            for tags in sentence_tags:
                tag_counts += Counter(tags)
            total_tags = sum(tag_counts.values())
            out_file.write('== Distribution ==\n')
            for tag_id, tag in enumerate(['Neutral',
                    'Towards the United States', 'Against the United States',
                    'Towards the Soviet Union', 'Against the Soviet Union']):
                out_file.write('{}: {:0.1f}%\n'.format(tag,
                        tag_counts[tag_id] / total_tags * 100))
                
            out_file.write('= SPECTRUM =\n')
            for endpoint in ['us', 'soviet']:
                out_file.write('== {} ==\n'.format(endpoint))
                bias_scores = []
                for hit_id, rows in results.items():
                    bias_scores.append([int(row['Answer.' + endpoint +
                                        '_bias']) for row in rows])
                out_file.write('Mean standard deviation: {:0.2f}\n'
                        .format(np.mean(list(map(np.std, bias_scores)))))
                out_file.write('Interannotator agreement: {:0.3f}\n'
                        .format(average_agreement(bias_scores)))
                
                out_file.write('=== Distribution ===\n')
                score_counts = Counter(itertools.chain(*bias_scores))
                total_scores = sum(score_counts.values())
                for score in range(-3, 4):
                    out_file.write('{}: {:0.1f}%\n'.format(score,
                            score_counts[score] / total_scores * 100))
