import _path_config

import sys
import json

from biases.utils.mturk import mturk_connection
from boto.mturk.question import *

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 mturk_create_qualification.py qualificiation-test.json qual_name')
    else:
        _, qual_test_fname, qual_name = sys.argv
        
        with open(qual_test_fname, 'r') as qual_test_file:
            qual_test_json = json.load(qual_test_file)
            
        qual_test = QuestionForm()
        
        overview = Overview()
        overview.append(SimpleField('Title', 'Qualification test overview'))
        overview.append(SimpleField('Text',
                '''Hello! Thank you for taking the time to be a part of this \
                survey. The following survey is looking to detect and \
                understand bias at a sentence level in Spanish texts. For the \
                purposes of this survey, bias is defined as imbalances in \
                presentation that would suggest a preference or prejudice. \
                You will be required to tag bias in two short selections \
                of text. \
                In order to be approved for this qualificiation, you must \
                complete the below test with 80% accuracy.'''))
        qual_test.append(overview)
        
        for selection_index, selection in \
                enumerate(qual_test_json['selections']):
            selection_overview = Overview()
            selection_overview.append(SimpleField('Title', 'Text selection {}'
                    .format(selection_index + 1)))
            selection_overview.append(SimpleField('Text',
                    '''Please read the following text:'''))
            selection_overview.append(SimpleField('Text',
                    ' '.join(selection['sentences'])))
            selection_overview.append(SimpleField('Text',
                    '''Now, mark which sentences are biased. For each sentence, \
                    decide whether it is biased towards the United States, \
                    towards the Soviet Union, or if it is not biased. Note that \
                    most sentences are not biased.'''))
            qual_test.append(selection_overview)
            
            for sentence_index, sentence in enumerate(selection['sentences']):
                question_identifier = 'selection-{}-sentence-{}' \
                        .format(selection_index, sentence_index)
                question_content = QuestionContent()
                question_content.append(SimpleField('Text', sentence))
                answer_spec = AnswerSpecification(SelectionAnswer(
                        style = 'radiobutton',
                        selections = [
                            ('Not biased', 'none'),
                            ('Biased towards the United States', 'us-towards'),
                            ('Biased against the United States', 'us-against'),
                            ('Biased towards the Soviet Union', 'soviet-towards')
                            ('Biased against the Soviet Union', 'soviet-against'),
                        ]))
                        
                sentence_question = Question(question_identifier,
                                             question_content,
                                             answer_spec)
                qual_test.append(sentence_question)
            
            bias_overview = Overview()
            bias_overview.append(SimpleField('Text',
                    '''Now, answer the following two questions about the \
                    overall bias of the text (all the sentences).'''))
            qual_test.append(bias_overview)
            
            for country_id, country_name in [('us', 'United States'),
                                             ('soviet', 'Soviet Union')]:
                question_identifier = 'selection-{}-bias-{}' \
                        .format(selection_index, country_id)
                question_content = QuestionContent()
                question_content.append(SimpleField('Text',
                        'How biased is the text towards or against the {}?'
                        .format(country_name)))
                answer_spec = AnswerSpecification(SelectionAnswer(
                        style = 'radiobutton',
                        selections = [
                            ('Very biased against', '-3'),
                            ('Moderately biased against', '-2'),
                            ('Slightly biased against', '-1'),
                            ('Not biased', '0'),
                            ('Slightly biased towards', '1'),
                            ('Moderately biased towards', '2'),
                            ('Very biased towards', '3')
                        ]))
                        
                bias_question = Question(question_identifier, question_content,
                                         answer_spec)
                qual_test.append(bias_question)
        
        mturk_connection.create_qualification_type(qual_name,
                '''Able to read and understand bias in Spanish.''',
                status = 'Active',
                keywords = ['Spanish', 'bias', 'Espa\xf1ol', 'tag'],
                test = qual_test,
                test_duration = 60 * 60) # an hour
        