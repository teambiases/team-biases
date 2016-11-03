from boto.mturk.connection import MTurkConnection

from biases.utils.config import config

# Load access/secret keys from config file so we don't keep sensitive
# information in the repository
ACCESS_ID = config['AWS']['AccessKey']
SECRET_KEY = config['AWS']['SecretKey']
HOST = 'mechanicalturk.sandbox.amazonaws.com'
 
mturk_connection = MTurkConnection(aws_access_key_id=ACCESS_ID,
                                   aws_secret_access_key=SECRET_KEY,
                                   host=HOST)

#print(mtc.get_account_balance())

#see how to compare test results and then depending on how close 
#they get to being right grant or deny requests
#might have to set up a server so this is done continuously? 

