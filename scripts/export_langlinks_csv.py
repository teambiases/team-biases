import _path_config

import sys, os
from biases.wiki.langlinks import read_langlinks_from_db, write_langlinks_file
from biases.utils.mysql import connect_with_prompt

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: python3 export_langlinks_csv.py user@dbhost lang1 lang2... outdir')
        print('Export langlinks info from a database as CSV files in outdir')
    else:
        user_hostname = sys.argv[1]
        langs = sys.argv[2:-1]
        outdir = sys.argv[-1]
        
        db_cursor = connect_with_prompt(user_hostname).cursor()
        
        for from_lang in langs:
            to_langs = [lang for lang in langs if lang != from_lang]
            langlinks = read_langlinks_from_db(from_lang, to_langs, db_cursor)
            out_file = '{}{}{}_langlinks.csv'.format(outdir, os.path.sep,
                                                     from_lang)
            print('Writing {}'.format(out_file))
            write_langlinks_file([from_lang] + to_langs, langlinks, out_file)
