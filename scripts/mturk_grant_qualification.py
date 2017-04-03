import _path_config

import sys
import json
import time
import logging
import csv
import os

from biases.utils.mturk import mturk_connection

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: python3 mturk_grant_qualification.py qualificiation-test.json|password qual_id log.csv')
        print('Continually checks for submitted qualification tests for the qualification')
        print('with the given ID and grants or rejects them based on the answers in')
        print('qualification-test.json. Writes a log of the results of log.csv. If')
        print('password is specified instead of a qualification test file, then just checks')
        print('the password field of the qualification test.')
    else:
        _, qual_test_fname, qual_id, log_fname = sys.argv
        
        if not qual_test_fname.endswith('.json'):
            qual_password = qual_test_fname
            qual_test_fname = None
        
        if qual_test_fname is not None:
            with open(qual_test_fname, 'r') as qual_test_file:
                qual_test_json = json.load(qual_test_file)
        else:
            qual_test = None
            
        log_already_exists = os.path.isfile(log_fname)
        with open(log_fname, 'a' if log_already_exists else 'w') as log_file:
            log_csv = csv.writer(log_file)
            if qual_test is not None:
                log_headers = ['worker', 'request-id', 'time', 'granted', 
                               'tags-correct']
                for selection_index, selection in \
                        enumerate(qual_test_json['selections']):
                    for sentence_index in range(len(selection['correct_tags'])):
                        log_headers.append('selection-{}-sentence-{}'.format(
                                selection_index, sentence_index))
                    for endpoint in selection['correct_bias'].keys():
                        log_headers.append('selection-{}-bias-{}'.format(
                                selection_index, endpoint))
                if not log_already_exists:
                    log_csv.writerow(log_headers)
            
            while True:
                requests = mturk_connection.get_qualification_requests(qual_id)
                for request in requests:
                    answers = {answer.qid: (answer.fields[0] if
                               len(answer.fields) > 0 else None)
                               for answer in request.answers[0]}
                    if qual_test is not None:
                        grant_qualification = True
                        
                        tags_total, tags_correct = 0, 0
                        for selection_index, selection in \
                                enumerate(qual_test_json['selections']):
                            
                            # Check bias tags
                            for sentence_index, tag in \
                                    enumerate(selection['correct_tags']):
                                qid = 'selection-{}-sentence-{}'.format(
                                        selection_index, sentence_index)
                                if answers[qid] == tag:
                                    tags_correct += 1
                                tags_total += 1
                                
                            # Check bias scores
                            for endpoint, correct_bias in \
                                    selection['correct_bias'].items():
                                qid = 'selection-{}-bias-{}'.format(
                                        selection_index, endpoint)
                                # Reject qualification if bias score is off by
                                # more than 1
                                try:
                                    answer_bias = int(answers[qid])
                                    if abs(answer_bias - correct_bias) > 1:
                                        grant_qualification = False
                                # If they didn't give an answer
                                except TypeError: 
                                    grant_qualification = False
                                logging.info('%s on %s: answer=%s, correct=%d',
                                        request.SubjectId, qid, answers[qid],
                                        correct_bias)
                         
                        logging.info('%s: %d / %d tags correct (%d%%)',
                                request.SubjectId, tags_correct, tags_total,
                                round(tags_correct / tags_total * 100))
                        # Reject qualification if less than 80% of tags are
                        # correct           
                        if tags_correct / tags_total < 0.8:
                            grant_qualification = False
                            
                        # Make a copy of answers to log
                        log_info = dict(answers)
                        log_info['worker'] = request.SubjectId
                        log_info['request-id'] = request.QualificationRequestId
                        log_info['time'] = request.SubmitTime
                        log_info['granted'] = grant_qualification
                        log_info['tags-correct'] = tags_correct
                        log_csv.writerow([log_info[header] for header in
                                          log_headers])
                        log_file.flush()
                    else:
                        grant_qualification = answers['password'] == \
                                qual_password
                            
                    if grant_qualification:
                        mturk_connection.grant_qualification(
                                request.QualificationRequestId)
                        logging.info('%s: granted qualification', 
                                request.SubjectId)
                    else:
                        mturk_connection._process_request(
                                'RejectQualificationRequest',
                                {'QualificationRequestId':
                                 request.QualificationRequestId})
                        logging.info('%s: rejected qualification',
                                request.SubjectId)
                        
                time.sleep(10)

