import _path_config

import sys
import json
import time
import logging
import csv
import os


from biases.utils.config import config

import boto3
import xml.etree.ElementTree as ET


# Load access/secret keys from config file so we don't keep sensitive
# information in the repository
ACCESS_ID = config['AWS']['AccessKey']
SECRET_KEY = config['AWS']['SecretKey']
 
mturk_connection = boto3.client('mturk',aws_access_key_id=ACCESS_ID,
                                   aws_secret_access_key=SECRET_KEY,
                                   region_name = 'us-east-1')



qual_id = ' . . . . . . '


requests = mturk_connection.list_qualification_requests(QualificationTypeId=qual_id, MaxResults = 100)
i = 1
for r in requests['QualificationRequests']:
	if i > 80:
		print(i)
		print('QualificationRequestId', r['QualificationRequestId'])
		print('QualificationTypeId',r['QualificationTypeId'])
		print('WorkerId', r['WorkerId'])
		print('SubmitTime', r['SubmitTime'])
		print('Answer', r['Answer'])
	i += 1

'''
Old boto: 
http://boto.cloudhackers.com/en/latest/ref/mturk.html

New boto:
http://boto3.readthedocs.io/en/latest/reference/services/mturk.html#paginators
'''