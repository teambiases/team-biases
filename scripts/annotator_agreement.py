"""
Uses nltk's metrics.agreement module to calculate the inter-annotator agreement.
The values will be written in the 'agreement_output.txt' file.
For now, the csv file is hardcoded as 
'prelim_batch_results.csv' in the data/csv folder, which may not exist or
can be accessed properly depending on operating system. 
"""
from nltk.metrics.agreement import AnnotationTask
import csv


assignments = []
with open ('../data/csv/prelim_batch_results.csv','r') as f:
    c = csv.DictReader(f)
    for row in c:
        assignments.append([row['Input.article'],
            row['Input.section_index'], 
            row['Input.chunk_index'], 
            row['Input.sentences'], 
            row['Answer.sentences'], 
            row['Answer.soviet_bias'],
            row['Answer.us_bias'],
            row['WorkerId']])
    
    payloads = {}
    for item in assignments: 
        payloads[','.join([item[0],item[1],item[2]])] = []

    for item in assignments:
        item[3] = item[3].split('</span>')
        item[4] = [x for x in item[4]]
        z = zip(item[3],item[4])
        for i in z:
            payloads[','.join([item[0],item[1],item[2]])].append((item[7],i[0],i[1]))
        payloads[','.join([item[0],item[1],item[2]])].append((item[7],'soviet_bias',item[5]))
        payloads[','.join([item[0],item[1],item[2]])].append((item[7],'us_bias',item[6]))

    with open ('agreement_output.txt','w') as g:
        for payload in payloads:
            task = AnnotationTask(payloads[payload])
            g.write(' '.join([payload,str(task.avg_Ao()),'\n']))

