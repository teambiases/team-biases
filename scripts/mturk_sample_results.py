import _path_config

import sys
import csv
import random
from collections import defaultdict

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: python3 mturk_sample_results.py results.csv sampled.csv sample_size')
        print('Given a bunch of Mechanical Turk results, samples sample_size results for each')
        print('HIT. This is useful if not all HITs have been completed by the same number of')
        print('Turkers, to normalize the data.')
    else:
        _, in_fname, out_fname, sample_size = sys.argv
        sample_size = int(sample_size)
        
        results = defaultdict(list)
        with open(in_fname, 'r') as in_file:
            in_csv = csv.reader(in_file)
            header = next(in_csv)
            assert header[0] == 'HITId'
            for row in in_csv:
                hit_id = row[0]
                results[hit_id].append(row)
                
        with open(out_fname, 'w') as out_file:
            out_csv = csv.writer(out_file)
            out_csv.writerow(header)
            for hit_id, rows in results.items():
                for row in random.sample(rows, sample_size):
                    out_csv.writerow(row)
           