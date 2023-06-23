import csv
import pandas as pd
import numpy as np
from tools import methods

gender_list = ['female_male', 'female_male_job', 'male_female', 'male_female_job']
race_list = ['african_american', 'african_arab', 'african_asian', 'african_european', 'american_african', 'american_arab', 'american_asian',
             'american_european','arab_african','arab_american','arab_asian','arab_european','asian_african','asian_american',
             'asian_arab','asian_european','european_african','european_american','european_arab','european_asian','majority_minority',
             'majority_mixed','minority_majority','minority_mixed','mixed_majority','mixed_minority']
body_list = ['common_disorder', 'common_hair', 'common_uncommon', 'disorder_common', 'old_young', 'uncommon_common', 'young_old', 'hair_common']

list1 = body_list
list2 = gender_list
csv_result_file = '../output/rest_intersectional_stats_body+gender.csv'
column_overview = ['Technique', 'model', 'dataset', 'set', 'num_errors', 'num_occurrences', 'num_cases_modified', 'err_rate', 'time (s)']
columns = ['both_error', 'none_error', 'half_error', 'inhibited', 'both_error_combinaisons']

overall_rows = [column_overview]


paths = []
for i in ['ledgar', 'scotus', 'ecthr_a', 'ecthr_b', 'eurlex']:
    for j in ['bert-base-uncased', 'microsoft/deberta-base', 'roberta-base', 'nlpaueb/legal-bert-base-uncased']:
        for k in ['test', 'validation', 'train']:
            path = '/'.join(['../output', i, j, k])
            paths.append(path)


total_both_error = 0
total_none_error = 0
total_half_error = 0
total_inhibited = 0
total_both_error_combinaison = 0

rows = [columns]
for path in paths:
    both_error = 0
    none_error = 0
    half_error = 0
    inhibited = 0
    for e1 in list1:
        list1_path = path + '/error_details/replacement_all_occurrences-' + e1 + '.pkl'
        list1_content = methods.getFromPickle(list1_path, 'rb')
        for e2 in list2:
            intersectional_path = path + '/error_details/intersectional_all_occurrences-' + e1 + '+' + e2 + '.pkl'
            intersectional_content = methods.getFromPickle(intersectional_path, 'rb')
            list2_path = path + '/error_details/replacement_all_occurrences-' + e2 + '.pkl'
            list2_content = methods.getFromPickle(list2_path, 'rb')
            set_tuple1 = set([(x[0], x[1], x[4]) for x in list1_content])
            set_tuple2 = set([(x[0], x[1], x[4]) for x in list2_content])
            for line in intersectional_content:
                case = line[6]
                tuple1 = (line[0], line[1], case)
                tuple2 = (line[2], line[3], case)
                in_tuple1 = tuple1 in set_tuple1
                in_tuple2 = tuple2 in set_tuple2
                if in_tuple1 and in_tuple2 : both_error += 1
                elif not in_tuple1 and not in_tuple2 : none_error += 1
                else : half_error += 1

            set_intersectional = set([(x[0], x[1], x[2], x[3], x[6]) for x in intersectional_content])
            combinaison_same_case = set()
            for x in set_tuple1:
                for y in set_tuple2:
                        if x[2] == y[2]:
                            combinaison_same_case.add((x[0], x[1], y[0], y[1], y[2]))
            inhibited += len(combinaison_same_case.difference(set_intersectional))
            total_both_error_combinaison += len(combinaison_same_case)


    total_both_error += both_error
    total_none_error += none_error
    total_half_error += half_error
    total_inhibited += inhibited
    print("[{}, {}, {}, {}] [both errors, none errors, half errors, inhibited] in {}".format(total_both_error, total_none_error, total_half_error, total_inhibited, path))
    rows.append([both_error, none_error, half_error, inhibited, path])
rows.append([])
rows.append([total_both_error, total_none_error, total_half_error, total_inhibited, total_both_error_combinaison])

total = total_both_error + total_none_error + total_half_error
perc_both = round(total_both_error/total, 3)
perc_none = round(total_none_error/total, 3)
perc_half = round(total_half_error/total, 3)

perc_both_comb_error = round(inhibited/total_both_error_combinaison, 4)

rows.append([perc_both, perc_none, perc_half, perc_both_comb_error])

methods.writeCSV(csv_result_file, rows)

print("Terminated [{}, {}, {}, {}] \n [both errors, none errors, half errors, inhibited]".format(perc_both, perc_none, perc_half, perc_both_comb_error))

print('Exit successfully')
