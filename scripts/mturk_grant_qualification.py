import _path_config

import sys
import json
import time
import logging

from biases.utils.mturk import mturk_connection

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 mturk_grant_qualification.py qualificiation-test.json qual_id')
        print('Continually checks for submitted qualification tests for the qualification')
        print('with the given ID and grants or rejects them based on the answers in')
        print('qualification-test.json.')
    else:
        _, qual_test_fname, qual_id = sys.argv
        
        with open(qual_test_fname, 'r') as qual_test_file:
            qual_test_json = json.load(qual_test_file)
            
        while True:
            requests = mturk_connection.get_qualification_requests(qual_id)
            for request in requests:
                answers = {answer.qid: answer.fields[0] for answer in
                           request.answers[0]}
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
                        qid = 'selection-{}-bias-{}'.format(selection_index,
                                                            endpoint)
                        # Reject qualification if bias score is off by more
                        # than 1
                        answer_bias = int(answers[qid])
                        if abs(answer_bias - correct_bias) > 1:
                            grant_qualification = False
                        logging.info('%s on %s: answer=%d, correct=%d',
                                request.SubjectId, qid, answer_bias,
                                correct_bias)
                 
                logging.info('%s: %d / %d tags correct (%d%%)',
                        request.SubjectId, tags_correct, tags_total,
                        round(tags_correct / tags_total * 100))
                # Reject qualification if less than 80% of tags are correct           
                if tags_correct / tags_total < 0.8:
                    grant_qualification = False
                    
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
