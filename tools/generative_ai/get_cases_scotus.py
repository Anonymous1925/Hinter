import datasets
from tools import methods
from nltk.tokenize import word_tokenize
gender_list = ['female_male', 'female_male_job', 'male_female', 'male_female_job']
race_list = ['african_american', 'african_arab', 'african_asian', 'african_european', 'american_african', 'american_arab', 'american_asian',
             'american_european','arab_african','arab_american','arab_asian','arab_european','asian_african','asian_american',
             'asian_arab','asian_european','european_african','european_american','european_arab','european_asian','majority_minority',
             'majority_mixed','minority_majority','minority_mixed','mixed_majority','mixed_minority']
body_list = ['common_disorder', 'common_hair', 'common_uncommon', 'disorder_common', 'old_young', 'uncommon_common', 'young_old', 'hair_common']
rows = [['Dataset', 'Model', 'Set', 'Case Number', 'Case', 'Mutant']]
data_name= "ecthr_a"
models = ['bert-base-uncased', 'microsoft/deberta-base', 'roberta-base', 'nlpaueb/legal-bert-base-uncased']
sets = ["train", "validation", "test"]

atomic_comment = "replacement_replacement_atomic"
intersectional_comment = "intersectional_intersectionality"

dict_dataset = dict()
for s in sets:
    dataset = datasets.load_dataset('lex_glue', name=data_name, data_dir='data', split=s)
    dict_dataset[s] = [''.join(dataset[i][('text')]) for i in
                range(len(dataset))]

dict_errors = dict()

###############Atomic errors###############################
error_list = []
for m in models:
    for s in sets:
        for g in gender_list+race_list+body_list:
            error_file_name = atomic_comment+"-"+g+".pkl"
            path = "/".join(["..","output",data_name, m, s, "error_details", error_file_name])
            content = methods.getFromPickle(path, 'rb')
            [error_list.append([m,s,[None, g],x]) for x in content]
dict_errors[atomic_comment] = error_list
###########################################################
############Intersectional errors##########################
error_list = []
for m in models:
    for s in sets:
        for l in [[race_list, gender_list], [body_list, gender_list], [body_list, race_list]]:
            for o  in l[0]:
                for g in l[1]:
                    error_file_name = intersectional_comment+"-"+o+"+"+g+".pkl"
                    path = "/".join(["..","output",data_name, m, s, "error_details", error_file_name])
                    content = methods.getFromPickle(path, 'rb')
                    [error_list.append([m,s,[o,g],x]) for x in content]
dict_errors[intersectional_comment] = error_list
###########################################################

print("Starting comparison ...")

atomic_cases = []
intersectional_cases = []
set_atomic = set([(x[0], x[1], x[2][1], x[3][4]) for x in dict_errors[atomic_comment]])
temp_atomic = set()
for x in dict_errors[intersectional_comment]:
    inter_ids1 = (x[0], x[1], x[2][0], x[3][6])
    inter_ids2 = (x[0], x[1], x[2][1], x[3][6])
    if inter_ids1 in set_atomic and inter_ids2 in set_atomic:
        intersectional_cases.append(x)
        temp_atomic.add(inter_ids1)
        temp_atomic.add(inter_ids2)
    elif inter_ids1 in set_atomic:
        intersectional_cases.append(x)
        temp_atomic.add(inter_ids1)
    elif inter_ids2 in set_atomic:
        intersectional_cases.append(x)
        temp_atomic.add(inter_ids2)

for x in dict_errors[atomic_comment]:
    atomic_id = (x[0], x[1], x[2][1], x[3][4])
    if atomic_id in temp_atomic:
        atomic_cases.append(x)

print("Creating sets ...")
set_cases_atomic = set([(x[3][4], x[1]) for x in atomic_cases])
set_cases_intersectional = set([(x[3][6], x[1]) for x in intersectional_cases])



def search_cases(name, set_list):
    i = 0
    while (len(dict_taken[name]) < treshold) and i < len(atomic_cases):
        case = atomic_cases[i]
        ids = (case[3][4], case[1])
        if ids not in taken_cases and ids in set_list:
            taken_cases.add(ids)
            dict_taken[name].append(case)
        i += 1

def finalize_cases(name, set_list):
    for case in atomic_cases:
        ids = (case[3][4], case[1])
        if ids not in taken_cases and ids in set_list:
            taken_cases.add(ids)
            dict_taken[name].append(case)

def search_intersectional_cases(name1, name2, set_list):
    for case in intersectional_cases:
        ids = (case[3][6], case[1])
        if ids not in taken_cases and ids in set_list and (
                ids in dict_atomic_set_taken[name1] or ids in dict_atomic_set_taken[name2]):
            taken_cases.add(ids)
            dict_taken[name1+"_"+name2].append(case)
treshold = 700
#######################################
###Atomic selection###################
body = set()
race = set()
gender = set()
body_race = set()
body_gender = set()
race_gender = set()

for case in atomic_cases:
    id = case[3][4]
    s = case[1]
    l = case[2][1]
    if l in race_list : race.add((id, s))
    elif l in gender_list : gender.add((id, s))
    else : body.add((id, s))

taken_cases = set()
dict_taken = dict()
dict_taken['body'] = []
dict_taken['race'] = []
dict_taken['gender'] = []

search_cases('gender', gender)
search_cases('body', body)
finalize_cases('race', race)
finalize_cases('body', body)
finalize_cases('gender', gender)


print("Taken atomic body :", len(dict_taken['body']))
print("Taken atomic race :", len(dict_taken['race']))
print("Taken atomic gender :", len(dict_taken['gender']))

#####intersectional selection

for case in intersectional_cases:
    id = case[3][6]
    s = case[1]
    l2 = case[2][1]
    l1 = case[2][0]
    if (l1 in body_list and l2 in race_list) or (l2 in body_list and l1 in race_list) : body_race.add((id, s))
    elif (l1 in body_list and l2 in gender_list) or (l2 in body_list and l1 in gender_list) : body_gender.add((id, s))
    else : race_gender.add((id, s))

taken_cases = set()
dict_atomic_set_taken = dict()
dict_atomic_set_taken['body'] = set([(x[3][4], x[1]) for x in dict_taken['body']])
dict_atomic_set_taken['race'] = set([(x[3][4], x[1]) for x in dict_taken['race']])
dict_atomic_set_taken['gender'] = set([(x[3][4], x[1]) for x in dict_taken['gender']])
dict_taken['body_race'] = []
dict_taken['race_gender'] = []
dict_taken['body_gender'] = []

search_intersectional_cases("body", "race", body_race)
search_intersectional_cases("body", "gender", body_gender)
search_intersectional_cases("race", "gender", race_gender)


print("body_race :", len(dict_taken['body_race']))
print("body_gender :", len(dict_taken['body_gender']))
print("race_gender :", len(dict_taken['race_gender']))

methods.writePickle(dict_taken, "../generative_ai/ecthr_a_selected_bias.pkl", "wb")




