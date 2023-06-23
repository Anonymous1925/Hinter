import re

import datasets

from tools import methods
from random import randint

gender_list = ['female_male', 'female_male_job', 'male_female', 'male_female_job']
race_list = ['african_american', 'african_arab', 'african_asian', 'african_european', 'american_african', 'american_arab', 'american_asian',
             'american_european','arab_african','arab_american','arab_asian','arab_european','asian_african','asian_american',
             'asian_arab','asian_european','european_african','european_american','european_arab','european_asian','majority_minority',
             'majority_mixed','minority_majority','minority_mixed','mixed_majority','mixed_minority']
body_list = ['common_disorder', 'common_hair', 'common_uncommon', 'disorder_common', 'old_young', 'uncommon_common', 'young_old', 'hair_common']
rows = [['Dataset', 'Model', 'Set', 'Case Number', 'Case', 'Mutant']]
data= ['scotus', 'ecthr_a', 'ecthr_b', 'eurlex']
dict_datasets = dict()
for d in data:
    complete_dataset = datasets.load_dataset('lex_glue', name=d, data_dir='data', split="train")
    complete_dataset_size = len(complete_dataset)
    dict_datasets[d] = [''.join(complete_dataset[i][('text')]) for i in
                range(complete_dataset_size)]

#intersectional
# for k in [[body_list, gender_list], [body_list, race_list], [race_list, gender_list]]:
#     for i in data:
#         for j in ['bert-base-uncased', 'microsoft/deberta-base', 'roberta-base', 'nlpaueb/legal-bert-base-uncased']:
#             temp_list = 0
#             while temp_list<2:
#                 list1_name = k[0][randint(0,len(k[0])-1)]
#                 list2_name = k[1][randint(0,len(k[1])-1)]
#                 if list1_name == list2_name : continue
#                 list_file_name = 'intersectional_intersectionality-'+list1_name+'+'+list2_name+'.pkl'
#                 path = '../output/'+i+'/'+j+'/train/error_details/'+list_file_name
#                 errors = methods.getFromPickle(path, 'rb')
#                 if len(errors) == 0 : continue
#                 error = errors[randint(0,len(errors)-1)]
#                 w1 = error[0]
#                 r1 = error[1]
#                 w2 = error[2]
#                 r2 = error[3]
#                 c_n= error[6]
#                 c =  dict_datasets[i][c_n]
#                 if c_n in [z[3] for z in rows] : continue
#                 if len(c) > 32767: continue
#                 regex1 = r"\b" + w1 + r"\b"
#                 insensitive_word1 = re.compile(regex1, re.IGNORECASE)
#                 temp_text = insensitive_word1.sub(r1,c)
#                 regex2 = r"\b" + w2 + r"\b"
#                 insensitive_word2 = re.compile(regex2, re.IGNORECASE)
#                 mutant = insensitive_word2.sub(r2, temp_text)
#                 temp_list+=1
#                 rows.append([i, j, 'train',c_n, c, mutant])
# methods.writeCSV('grammarly_cases_intersectional.csv', rows)
for k in [body_list,gender_list,race_list]:
    for i in data:
        for j in ['bert-base-uncased', 'microsoft/deberta-base', 'roberta-base', 'nlpaueb/legal-bert-base-uncased']:
            temp_list = 0
            while temp_list<2:
                list1_name = k[randint(0,len(k)-1)]
                list_file_name = 'replacement_replacement_atomic-'+list1_name+'.pkl'
                path = '../output/'+i+'/'+j+'/train/error_details/'+list_file_name
                errors = methods.getFromPickle(path, 'rb')
                if len(errors) == 0 : continue
                error = errors[randint(0,len(errors)-1)]
                w1 = error[0]
                r1 = error[1]
                c_n= error[4]
                c =  dict_datasets[i][c_n]
                if c_n in [z[4] for z in rows]: continue
                if len(c) > 32767: continue
                regex1 = r"\b" + w1 + r"\b"
                insensitive_word1 = re.compile(regex1, re.IGNORECASE)
                mutant = insensitive_word1.sub(r1,c)
                temp_list+=1
                rows.append([i, j, 'train',c_n, c, mutant])
methods.writeCSV('grammarly_cases_atomic.csv', rows)
print('Hee-Hoo !')
