"""MySQL-related utility functions."""

import getpass
import re
import ast
import gzip

def cursor_iterator(cursor, batch_size = 1000):
    """Iterates over the results of a MySQL query such that the entire results
    aren't loaded into memory at once."""
    
    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        for row in rows:
            yield row

def connect_with_prompt(user_hostname, charset = 'utf8', **connect_params):
    """Given a user/hostname combination in the form user@hostname, prompts
    for a password and then returns a connection to the given MySQL server."""
    
    import MySQLdb as mysql

    user, hostname = user_hostname.split('@')
    password = getpass.getpass('Password for {}: '.format(user_hostname))
    
    return mysql.connect(host = hostname, user = user, passwd = password,
                         charset = charset, **connect_params)
    
SQL_DUMP_REGEX = re.compile('INSERT INTO (`.*`|[^\s]*) VALUES (.*);',
                            flags = re.IGNORECASE)
    
def read_sql_dump(dump_fname):
    """Given a MySQL dump file, iterates over the rows in the table. Yields a
    tuple for each row."""
    
    fopen_func = open
    if dump_fname.endswith('.gz'):
        fopen_func = gzip.open
    
    with fopen_func(dump_fname, 'rb') as dump_file:
        for line in dump_file:
            if isinstance(line, bytes):
                line = line.decode('utf-8', 'ignore').strip()
            match = SQL_DUMP_REGEX.fullmatch(line)
            if match is not None:
                rows = ast.literal_eval('[' + match.group(2) + ']')
                for row in rows:
                    yield row
