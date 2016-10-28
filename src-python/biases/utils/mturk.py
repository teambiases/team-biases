from boto.mturk.connection import MTurkConnection

#Access Key ID:
#AKIAIK2VPYKSBVTE2DKA
#Secret Access Key:
#DumhVHYugLQGwIX8sAxndIaPgoo60E0qYxyAvUfl

ACCESS_ID ='AKIAIK2VPYKSBVTE2DKA'
SECRET_KEY = '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'
HOST = 'mechanicalturk.sandbox.amazonaws.com'
 
mtc = MTurkConnection(aws_access_key_id=ACCESS_ID,
                      aws_secret_access_key=SECRET_KEY,
                      host=HOST)


#print(mtc.get_account_balance())

#see how to compare test results and then depending on how close 
#they get to being right grant or deny requests
#might have to set up a server so this is done continuously? 

