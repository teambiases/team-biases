import _path_config

import sys
import csv

if __name__ == '__main__':
    if len(sys.argv) not in [3, 4]:
        print('Usage: python3 explore_dump_filter.py in.csv out.csv (threshold)')
        print('Filters the output of explore_dump.py by removing all rows that consist only of')
        print('values equal to or below the specified threshold (zero if not given.)')
    else:
        _, in_fname, out_fname = sys.argv[:3]
        threshold = float(sys.argv[3]) if len(sys.argv) == 4 else 0
        
        with open(in_fname, 'r') as in_file:
            in_csv = csv.reader(in_file)
            with open(out_fname, 'w') as out_file:
                out_csv = csv.writer(out_file)
                
                # Copy header row
                out_csv.writerow(next(in_csv))
                
                # Write only rows with at least one value above zero
                for row in in_csv:
                    if max(map(float, row[1:])) > threshold:
                        out_csv.writerow(row)
