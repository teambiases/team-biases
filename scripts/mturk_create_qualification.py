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
        overview.append(SimpleField('Title', 'Resumen de la prueba de calificación'))
        overview.append(SimpleField('Text',
                '''Hola, Muchas gracias por dedicar tu tiempo y participar en \
                esta encuesta. La encuesta busca detectar y entender la \
                tendencia de la parcialidad en una frase o oración en español.\
                Para el propósito de esta encuesta, parcialidad tiene la \
                definición de existencia de  imbalance, lo que conlleva a \
                sugerir la existencia de preferencia o preconcepción. Se
                requiere que Ud. remarque la parcialidad en dos frases cortas.

                Para poder aprobar en esta calificación, Ud. deberá completar \
                el siguiente test con una exactitud de 80 %.'''))
        qual_test.append(overview)
        
        for selection_index, selection in \
                enumerate(qual_test_json['selections']):
            selection_overview = Overview()
            selection_overview.append(SimpleField('Title', 'Selección de texto {}'
                    .format(selection_index + 1)))
            selection_overview.append(SimpleField('Text',
                    '''Por favor lea el siguiente texto :'''))
            selection_overview.append(SimpleField('Text',
                    ' '.join(selection['sentences'])))
            selection_overview.append(SimpleField('Text',
                    '''Marcar que frases muestran parcialidad. Por cada \
                    sentencia, decidir si la parcialidad es hacia los \
                    Estados Unidos or hacia la Unión Soviética, o si no \
                    existe parcialidad. Cabe resaltar que muchas de las \
                    frases no demuestran parcialidad.'''))
            qual_test.append(selection_overview)
            
            for sentence_index, sentence in enumerate(selection['sentences']):
                question_identifier = 'selection-{}-sentence-{}' \
                        .format(selection_index, sentence_index)
                question_content = QuestionContent()
                question_content.append(SimpleField('Text', sentence))
                answer_spec = AnswerSpecification(SelectionAnswer(
                        style = 'radiobutton',
                        selections = [
                            ('No Parcialidad', 'none'),
                            ('Parcialidad hacia los Estados Unidos', 'us-towards'),
                            ('Parcialidad contra los Estados Unidoss', 'us-against'),
                            ('Parcialidad hacia la Unión Soviética', 'soviet-towards'),
                            ('Parcialidad contra la Unión Soviética', 'soviet-against'),
                        ]))
                        
                sentence_question = Question(question_identifier,
                                             question_content,
                                             answer_spec)
                qual_test.append(sentence_question)
            
            bias_overview = Overview()
            bias_overview.append(SimpleField('Text',
                    '''Contestar las dos preguntas siguientes acerca de la \
                    parcialidad en general en el texto. (Todas las frases)'''))
            qual_test.append(bias_overview)
            
            for country_id, country_name in [('us', 'los Estados Unidos'),
                                             ('soviet', 'la Unión Soviética')]:
                question_identifier = 'selection-{}-bias-{}' \
                        .format(selection_index, country_id)
                question_content = QuestionContent()
                question_content.append(SimpleField('Text',
                        'Cual es el sentido de la parcialidad en el texto? '
                        + 'Favorable o desfavorable hacia {}?'
                        .format(country_name)))
                answer_spec = AnswerSpecification(SelectionAnswer(
                        style = 'radiobutton',
                        selections = [
                            ('Totalmente en contra', '-3'),
                            ('Moderadamente en contra', '-2'),
                            ('Ligeramente en contra', '-1'),
                            ('No existe parcialidad', '0'),
                            ('Ligeramente parcial a favor', '1'),
                            ('Moderadamente parcial a favor', '2'),
                            ('Totalmente parcial a favor', '3')
                        ]))
                        
                bias_question = Question(question_identifier, question_content,
                                         answer_spec)
                qual_test.append(bias_question)
        
        mturk_connection.create_qualification_type(qual_name,
                '''Capaz de leer y entender parcialidad en espanol.''',
                status = 'Active',
                keywords = ['Spanish', 'bias', 'Espa\xf1ol', 'tag'],
                test = qual_test,
                test_duration = 60 * 60) # an hour
        