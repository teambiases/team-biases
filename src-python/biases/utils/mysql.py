"""MySQL-related utility functions."""

import MySQLdb as mysql
import getpass

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
    
    user, hostname = user_hostname.split('@')
    password = getpass.getpass('Password for {}: '.format(user_hostname))
    
    return mysql.connect(host = hostname, user = user, passwd = password,
                         charset = charset, **connect_params)
