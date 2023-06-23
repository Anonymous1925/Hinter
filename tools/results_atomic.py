import csv
import pandas as pd
import numpy as np
from tools import methods

paths = []
for i in ['ledgar', 'scotus', 'ecthr_a', 'ecthr_b', 'eurlex']:
    for j in ['bert-base-uncased', 'microsoft/deberta-base', 'roberta-base', 'nlpaueb/legal-bert-base-uncased']:
        for k in ['test', 'validation', 'train']:
            path = '/'.join(['../output', i, j, k]) + '/result.csv'
            paths.append(path)

# rows.sort(key=lambda pair: pair[3], reverse=True)

categorys = ['atomic_body']

csv_result_file = '../output/atomic_results_overview_body.csv'

gender_list = ['female_male', 'female_male_job', 'male_female', 'male_female_job']
race_list = ['african_american', 'african_arab', 'african_asian', 'african_european', 'american_african', 'american_arab', 'american_asian',
             'american_european','arab_african','arab_american','arab_asian','arab_european','asian_african','asian_american',
             'asian_arab','asian_european','european_african','european_american','european_arab','european_asian','majority_minority',
             'majority_mixed','minority_majority','minority_mixed','mixed_majority','mixed_minority']
body_list = ['common_disorder', 'common_hair', 'common_uncommon', 'disorder_common', 'old_young', 'uncommon_common', 'young_old', 'hair_common']
list_to_test = body_list

column_overview = ['Technique', 'model', 'dataset', 'set', 'num_errors', 'num_occurrences', 'num_cases_modified', 'err_rate', 'time (s)']
overall_rows = [column_overview]
categorys_overview = [[] for x in categorys]
nb_line = 0
for path in paths:
    set_type = 'test' if '/test/' in path else ('validation' if '/validation/' in path else 'train')
    file_content = pd.read_csv(path, delimiter=';', index_col=False)
    columns = file_content.columns.to_numpy()
    lines_file = file_content.to_numpy()
    #paragraphs = [[x for x in lines_file if str(x[8]).startswith(category) and 'replacement_all_occurrences' in x[0]] for category in categorys]#categorys
    # paragraphs = [[x for x in lines_file if
    # any(y in str(x[8]) for y in categorys) and 'replacement_all_occurrences' in x[0]]]#replacement
    #paragraphs = [[x for x in lines_file if
    #                any(y in str(x[8]) for y in categorys) and 'replacement_wi_to_word' in x[0]]]#wi_to_word
    #paragraphs = [[x for x in lines_file if
    #               any(y in str(x[8]) for y in categorys) and 'replacement_word_to_wi' in x[0]]]  # word_to_wi
    #paragraphs = [[x for x in lines_file if
    #               any(y in str(x[8]) for y in categorys) and 'replacement_wi_to_wi' in x[0]]]  # wi_to_wi
    # paragraphs = [[x for x in lines_file if
    #  any(y in str(x[8]) for y in categorys) and 'deletion_all_occurrences' in x[0]]]#deletion
    # paragraphs = [[x for x in lines_file if str(x[0]).startswith("intersectional")
    #                and any(y == str(x[8]).split('+')[0] for y in race_list)
    #                and any(y == str(x[8]).split('+')[1] for y in gender_list)]]#intersectional
    paragraphs = [[x for x in lines_file if x[0] == 'replacement_all_occurrences' and x[8] in list_to_test]]#replacement
    if nb_line == 0:
        nb_line = len(paragraphs[0])
        print("{} lines in first result file".format(nb_line))
    elif nb_line != len(paragraphs[0]) : print('Error, results not similar !')
    for i in range(len(paragraphs)):
        average_row = []
        paragraph = paragraphs[i]
        nb_row_paragraph = len(paragraph)

        average_row.append('overview_' + categorys[i])
        average_row.append(paragraph[0][1])
        average_row.append(paragraph[0][2])

        sum_nb_error = np.array([paragraph[x][3] for x in range(nb_row_paragraph)]).sum()
        average_row.append(sum_nb_error)

        nb_occurrences = np.array([paragraph[x][4] for x in range(nb_row_paragraph)]).sum()
        average_row.append(nb_occurrences)

        sum_case_modified = np.array([paragraph[x][5] for x in range(nb_row_paragraph)]).sum()
        average_row.append(sum_case_modified)

        error_rate = round(sum_nb_error / sum_case_modified, 3) if sum_case_modified != 0 else 'None'
        average_row.append(error_rate)

        sum_time = round(np.array([paragraph[x][7] for x in range(nb_row_paragraph)]).sum(), 3)
        average_row.append(sum_time)

        paragraph.append(average_row)

        paragraph.append([])
        overall = ['overview_' + categorys[i], paragraph[0][1], paragraph[0][2], set_type, sum_nb_error,
                   nb_occurrences, sum_case_modified, error_rate, sum_time]
        categorys_overview[i].append(overall)
        overall_rows.append(overall)

overall_rows.append([])
overall_rows.append(['Technique', 'num_errors', 'num_occurrences', 'num_cases_modified', 'err_rate', 'time (s)'])
for i in categorys_overview:
    if i == [] : continue
    sum_sum_nb_error = np.array([x[4] for x in i]).sum()
    sum_sum_cases_modified = np.array([x[6] for x in i]).sum()
    line = [i[0][0],
            sum_sum_nb_error,
            np.array([x[5] for x in i]).sum(),
            sum_sum_cases_modified,
            round(sum_sum_nb_error/sum_sum_cases_modified, 3) if sum_sum_cases_modified != 0 else 'None',
            int(np.array([x[8] for x in i]).sum())]
    overall_rows.append(line)


methods.writeCSV(csv_result_file, overall_rows)

print('Exit')
