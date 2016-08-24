"""Configure the python path to provide access to the Apache Spark. The
directory in which Spark is installed should be passed as the first
command-line argument to a script using this module."""

import sys, os
from os.path import sep

if len(sys.argv) < 2:
    print('Error: please specify the path to Apache Spark as the first argument.')
else:
    spark_home = sys.argv[1]
    os.environ['SPARK_HOME'] = spark_home
    os.environ['PYSPARK_PYTHON'] = sys.executable
    sys.path.append(sep.join([spark_home, 'python']))
