import csv
import re

import pandas as pd
import numpy as np
from tools import methods

gender_list = ['female_male', 'female_male_job', 'male_female', 'male_female_job']
race_list = ['african_american', 'african_arab', 'african_asian', 'african_european', 'american_african', 'american_arab', 'american_asian',
             'american_european','arab_african','arab_american','arab_asian','arab_european','asian_african','asian_american',
             'asian_arab','asian_european','european_african','european_american','european_arab','european_asian','majority_minority',
             'majority_mixed','minority_majority','minority_mixed','mixed_majority','mixed_minority']
body_list = ['common_disorder', 'common_hair', 'common_uncommon', 'disorder_common', 'old_young', 'uncommon_common', 'young_old', 'hair_common']

list1 = race_list
list2 = gender_list

list1_folder = 'race'
list2_folder = 'gender'

csv_result_file = '../output/intersection_detailed_'+list1_folder+'-'+list2_folder+'.csv'
column_overview = ['description', 'dataset', 'model', 'set', 'error_'+list1_folder+'_only_error', 'error_'+list2_folder+'_only_error', 'error_both_error',
                   'error_intersection_only_error', 'not_'+list1_folder+'_only_error', 'not_'+list2_folder+'_only_error', 'not_both_error', 'not_no_error']

overall_rows = [column_overview]

dict_lists = dict()
methods.createDir('../output/intersection_generated/')
datasets_to_test = ['ledgar', 'scotus', 'ecthr_a', 'ecthr_b', 'eurlex']
sets = ['train','test', 'validation' ]
models = ['bert-base-uncased','nlpaueb/legal-bert-base-uncased', 'microsoft/deberta-base', 'roberta-base' ]
rows = [column_overview]
# for i in datasets_to_test:
#     print(">>Doing {} / {} ...".format(datasets_to_test.index(i) + 1, len(datasets_to_test)))
#     for z in models:
#         print(">>>>Doing {} / {} ...".format(models.index(z) + 1, len(models)))
#         for k in sets:
#             print(">>>>>>Doing {} / {} ...".format(sets.index(k) + 1, len(sets)))
#             path = '/'.join(['../output', i, z, k])
#             truncated_text = methods.getTruncated(path+'/', i, None, None)
#             is_word_in_case = dict()
#             #generating tested pairs
#             #for each file in this folder
#             for l in list1:
#                 # print(">>>>>>Doing {} / {} ...".format(list1.index(l)+1, len(list1)))
#                 if l not in dict_lists : dict_lists[l] = methods.getWordlist('../data/'+list1_folder+'/'+l+'.csv')
#                 list1_content = dict_lists[l]
#                 # for each file in this folder
#                 for m in list2:
#                     index_l2 = list2.index(m)
#                     # print(">>>>>>>>Doing {} / {} ...".format(index_l2 + 1, len(list2)))
#                     if m not in dict_lists: dict_lists[m] = methods.getWordlist(
#                         '../data/' + list2_folder + '/' + m + '.csv')
#                     list2_content = dict_lists[m]
#                     mutants = [None]*len(truncated_text)
#                     # for each case
#                     for p in range(len(truncated_text)):
#                         mutants[p] = set()
#                         # is_stored = True if is_word_in[list2.index(m)] != None else False
#                         # is_in = is_word_in[list2.index(m)][p]
#                         #for each pair in the file
#                         for n in range(len(list1_content[1])):
#                             pair1=[list1_content[1][n], list1_content[2][n]]
#                             word_id = pair1[0]+str(p)
#                             if not word_id in is_word_in_case:
#                                 regex_1 = r"\b" + pair1[0] + r"\b"
#                                 is_word_in_case[word_id] = False if len(re.findall(regex_1, truncated_text[p])) == 0 else True
#                             if is_word_in_case[word_id] == False: continue
#                             # for each pair in the file (we have all the combinaisons of pair here)
#                             for o in range(len(list2_content[1])):
#                                 pair2 = [list2_content[1][o], list2_content[2][o]]
#                                 word_id = pair2[0] + str(p)
#                                 regex_2 = r"\b" + pair2[0] + r"\b"
#                                 if not word_id in is_word_in_case:
#                                     is_word_in_case[word_id] = False if len(re.findall(regex_2, truncated_text[p])) == 0 else True
#                                 if is_word_in_case[word_id] == False and len(re.findall(regex_2, pair1[1])) == 0: continue
#                                 new_element = (pair1[0], pair1[1], pair2[0], pair2[1], p)
#                                 mutants[p].add(new_element)
#                     methods.writePickle(mutants, '../output/intersection_generated/'+i+'-'+z.replace('/','_')+'-'+k+'-'+l+'-'+m+'.pkl', 'wb')
#
# print("Hee-Hoo !")
#
for i in ['ledgar', 'scotus', 'ecthr_a', 'ecthr_b', 'eurlex']:
    dataset_error_list1_only_error = 0
    dataset_error_list2_only_error = 0
    dataset_error_both_error = 0
    dataset_error_intersection_only_error = 0
    dataset_not_list1_only_error = 0
    dataset_not_list2_only_error = 0
    dataset_not_both_error = 0
    dataset_not_no_error = 0

    for j in ['bert-base-uncased', 'microsoft/deberta-base', 'roberta-base', 'nlpaueb/legal-bert-base-uncased']:
        for k in ['test', 'validation', 'train']:
            error_list1_only_error = 0
            error_list2_only_error = 0
            error_both_error = 0
            error_intersection_only_error = 0
            not_list1_only_error = 0
            not_list2_only_error = 0
            not_both_error = 0
            not_no_error = 0
            path = '/'.join(['../output', i, j, k])
            for e1 in list1:
                list1_path = path + '/error_details/replacement_replacement_atomic-' + e1 + '.pkl'
                list1_content = methods.getFromPickle(list1_path, 'rb')
                set_tuple1 = set([(x[0], x[1], x[4]) for x in list1_content])
                for e2 in list2:
                    list2_path = path + '/error_details/replacement_replacement_atomic-' + e2 + '.pkl'
                    list2_content = methods.getFromPickle(list2_path, 'rb')
                    set_tuple2 = set([(x[0], x[1], x[4]) for x in list2_content])
                    intersectional_error_path = path + '/error_details/intersectional_intersectionality-' + e1 + '+' + e2 + '.pkl'
                    intersectional_error_content = methods.getFromPickle(intersectional_error_path, 'rb')
                    intersectional_gen_path = '../output/intersection_generated/'+i+'-'+j.replace('/','_')+'-'+k+'-'+e1+'-'+e2+'.pkl'
                    intersectional_gen_content = methods.getFromPickle(intersectional_gen_path, 'rb')
                    if len(intersectional_error_content) != 0 and len(intersectional_gen_content) == 0 : print("Error while nothing Generated ! This seems very bad.")
                    #for each case
                    for l in range(len(intersectional_gen_content)):
                        set_generated = intersectional_gen_content[l]
                        set_errors = set([(x[0], x[1], x[2], x[3], x[6]) for x in intersectional_error_content if x[6] == l])
                        # if not set_errors.issubset(set_generated):
                        #     print("Error not subset of Generated ! This seems very bad.")
                        for m in set_generated:
                            tuple1 = (m[0], m[1], m[4])
                            tuple2 = (m[2], m[3], m[4])
                            in_tuple1 = tuple1 in set_tuple1
                            in_tuple2 = tuple2 in set_tuple2
                            if m in set_errors:
                                if in_tuple1 and in_tuple2 :
                                    error_both_error += 1
                                elif in_tuple1 :
                                    error_list1_only_error += 1
                                elif in_tuple2 :
                                    error_list2_only_error += 1
                                else : error_intersection_only_error += 1
                            else:
                                if in_tuple1 and in_tuple2 : not_both_error += 1
                                elif in_tuple1 : not_list1_only_error += 1
                                elif in_tuple2 : not_list2_only_error += 1
                                else : not_no_error += 1
            rows.append(['intersectionality', i, j, k, error_list1_only_error, error_list2_only_error, error_both_error, error_intersection_only_error,
                          not_list1_only_error, not_list2_only_error, not_both_error, not_no_error])
            print("{}/{}/{} : 1/2/1-2/0 {}/{}/{}/{} {}/{}/{}/{}".format(i, j, k, error_list1_only_error, error_list2_only_error, error_both_error, error_intersection_only_error,
                          not_list1_only_error, not_list2_only_error, not_both_error, not_no_error))
            dataset_error_list1_only_error +=error_list1_only_error
            dataset_error_list2_only_error +=error_list2_only_error
            dataset_error_both_error +=error_both_error
            dataset_error_intersection_only_error +=error_intersection_only_error
            dataset_not_list1_only_error +=not_list1_only_error
            dataset_not_list2_only_error +=not_list2_only_error
            dataset_not_both_error +=not_both_error
            dataset_not_no_error +=not_no_error
    rows.append(['total_'+i, i, '', '', dataset_error_list1_only_error, dataset_error_list2_only_error, dataset_error_both_error,
                  dataset_error_intersection_only_error, dataset_not_list1_only_error, dataset_not_list2_only_error, dataset_not_both_error, dataset_not_no_error])
    rows.append([])
methods.writeCSV(csv_result_file, rows)
print("Hee-Hoo !")