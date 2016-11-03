"""Loads the config file to use in the rest of the program."""

import sys
import configparser
from os.path import dirname, realpath, sep, pardir

CONFIG_FILENAME = sep.join([dirname(realpath(__file__)), pardir, pardir,
                            pardir, 'config.ini'])
config = configparser.ConfigParser()
config.read(CONFIG_FILENAME)
if len(config.sections()) == 0:
    print('Error while loading config file at "{}"'.format(CONFIG_FILENAME))
    sys.exit(1)
