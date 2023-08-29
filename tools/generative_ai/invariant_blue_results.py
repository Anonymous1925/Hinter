import argparse
import re

import numpy
from nltk.translate.bleu_score import sentence_bleu

import sememe_coref as sc
import datasets

from tools import methods

sc.init_dependency_model()
pick = methods.getFromPickle( "../generative_ai/ecthr_a_selected_bias.pkl", "rb")
file_lines = [[]]

atomic_error = pick['body']+pick['race']+pick['gender']
intersectional_error = pick['body_race']+pick['race_gender']+pick['body_gender']

invariance_columns = ['nb cases', 'nb sentences', 'nb sentences modified', 'rate modified sentences',
                          'nb right POS', 'nb wrong POS', 'rate wrong POS',
                          'nb right DEP', 'nb wrong DEP','rate wrong DEP',
                          'nb mutants similar (strict)', 'nb mutants not similar (strict)',
                          'rate not similar mutants (strict)',
                          'nb mutants similar (lazy)', 'nb mutants not similar (lazy)',
                          'rate not similar mutants (lazy)']

##########ATOMIC##################
a_nb_sentences = 0
a_sentences_mutated = 0
a_nb_right_pos = 0
a_nb_wrong_pos = 0
a_nb_right_dep = 0
a_nb_wrong_dep = 0
a_strict_similar = 0
a_strict_not_similar = 0
a_notstrict_similar = 0
a_notstrict_not_similar = 0
a_blue_score_sentences = 0
a_blue_score_cases = []
total_used_sentence = 0


for k in range(0, len(atomic_error)):
    print("Atomic ", k, "/", len(atomic_error))
    line = atomic_error[k]
    original = line[3][5]
    regex = r"\b" + line[3][0].lower() + r"\b"
    insensitive_word = re.compile(regex)
    modified_text = insensitive_word.sub(line[3][1].lower(), original)
    original_sentences = sc.split_into_sentences(original)
    modified_sentences = sc.split_into_sentences(modified_text)

    #Invariance comparison
    a_nb_sentences += len(original_sentences)
    temp_array = [None]*len(original_sentences)
    similar, temp_array, pos_list, dep_list = (
        sc.isTextStructureSimilar(original_sentences, temp_array, modified_sentences))
    a_sentences_mutated += len(pos_list)
    for x in pos_list : a_nb_right_pos += x[2]; a_nb_wrong_pos += x[1]
    for x in dep_list : a_nb_right_dep += x[2]; a_nb_wrong_dep += x[1]
    if similar : a_strict_similar += 1
    else : a_strict_not_similar += 1
    notstrict_similar = sc.isTextStructureSimilar(original_sentences, temp_array, modified_sentences, strict=False)[0]
    if notstrict_similar : a_notstrict_similar+=1
    else : a_notstrict_not_similar += 1
    #Blue score

    case_used_sentence = 0
    local_blue_score = 0
    for x in range(0, len(original_sentences)) :
        original_split = original_sentences[x].split()
        modified_sentences_split = modified_sentences[x].split()
        if len(original_split) < 5 or len(modified_sentences_split) < 5 : continue
        if original_split == modified_sentences_split : continue
        case_used_sentence += 1
        total_used_sentence += 1
        local_blue_score += sentence_bleu([original_split], modified_sentences_split)
    a_blue_score_cases.append(local_blue_score/case_used_sentence) if case_used_sentence != 0 else 1
    a_blue_score_sentences += local_blue_score if local_blue_score != 0 else 1
a_mean_blue_cases = numpy.sum(numpy.array(a_blue_score_cases))/len(atomic_error)
a_mean_blue_sentences = a_blue_score_sentences/total_used_sentence

file_lines.append(['Atomic'])
file_lines.append(invariance_columns)
file_lines.append([len(atomic_error), a_nb_sentences, a_sentences_mutated, round(a_sentences_mutated/a_nb_sentences,2),
                      a_nb_right_pos, a_nb_wrong_pos, round(a_nb_wrong_pos/(a_nb_right_pos+a_nb_wrong_pos),2),
                      a_nb_right_dep, a_nb_wrong_dep, round(a_nb_wrong_dep /(a_nb_right_dep + a_nb_wrong_dep), 2),
                      a_strict_similar, a_strict_not_similar,
                       round(a_strict_not_similar/(a_strict_similar + a_strict_not_similar),2),
                       a_notstrict_similar, a_notstrict_not_similar,
                       round(a_notstrict_not_similar / (a_notstrict_similar + a_notstrict_not_similar), 2),
                      ])
file_lines.append([])
file_lines.append(['Blue_score_cases','Blue_score_sentences'])
file_lines.append([a_mean_blue_cases, a_mean_blue_sentences])
###########################################################

##########INTERSECTIONAL##################
i_nb_sentences = 0
i_sentences_mutated = 0
i_nb_right_pos = 0
i_nb_wrong_pos = 0
i_nb_right_dep = 0
i_nb_wrong_dep = 0
i_strict_similar = 0
i_strict_not_similar = 0
i_notstrict_similar = 0
i_notstrict_not_similar = 0
i_blue_score_sentences = 0
i_blue_score_cases = []
total_used_sentence = 0

for k in range(0, len(intersectional_error)):
    print("intersectional ", k, "/", len(intersectional_error))
    line = intersectional_error[k]
    original = line[3][7]
    regex = r"\b" + line[3][0].lower() + r"\b"
    insensitive_word = re.compile(regex)
    modified_text = insensitive_word.sub(line[3][1].lower(), original)
    regex_2 = r"\b" + line[3][2].lower() + r"\b"
    insensitive_word_2 = re.compile(regex_2)
    modified_text_w1_w2 = insensitive_word_2.sub(line[3][3], modified_text)
    original_sentences = sc.split_into_sentences(original)
    modified_sentences = sc.split_into_sentences(modified_text_w1_w2)

    #Invariance comparison
    i_nb_sentences += len(original_sentences)
    temp_array = [None]*len(original_sentences)
    similar, temp_array, pos_list, dep_list = (
        sc.isTextStructureSimilar(original_sentences, temp_array, modified_sentences))
    i_sentences_mutated += len(pos_list)
    for x in pos_list : i_nb_right_pos += x[2]; i_nb_wrong_pos += x[1]
    for x in dep_list : i_nb_right_dep += x[2]; i_nb_wrong_dep += x[1]
    if similar : i_strict_similar += 1
    else : i_strict_not_similar += 1
    notstrict_similar = sc.isTextStructureSimilar(original_sentences, temp_array, modified_sentences, strict=False)[0]
    if notstrict_similar : i_notstrict_similar+=1
    else : i_notstrict_not_similar += 1
    #Blue score

    case_used_sentence = 0
    local_blue_score = 0
    for x in range(0, len(original_sentences)) :
        original_split = original_sentences[x].split()
        modified_sentences_split = modified_sentences[x].split()
        if len(original_split) < 5 or len(modified_sentences_split) < 5 : continue
        if original_split == modified_sentences_split: continue
        case_used_sentence += 1
        total_used_sentence += 1
        local_blue_score += sentence_bleu([original_split], modified_sentences_split)
    i_blue_score_cases.append(local_blue_score/case_used_sentence) if case_used_sentence != 0 else 1
    i_blue_score_sentences += local_blue_score if local_blue_score != 0 else 1
i_mean_blue_cases = numpy.sum(numpy.array(i_blue_score_cases))/len(intersectional_error)
i_mean_blue_sentences = i_blue_score_sentences/total_used_sentence

file_lines.append([])
file_lines.append(['intersectional'])
file_lines.append(invariance_columns)
file_lines.append([len(intersectional_error), i_nb_sentences, i_sentences_mutated, round(i_sentences_mutated/i_nb_sentences,2),
                      i_nb_right_pos, i_nb_wrong_pos, round(i_nb_wrong_pos/(i_nb_right_pos+i_nb_wrong_pos),2),
                      i_nb_right_dep, i_nb_wrong_dep, round(i_nb_wrong_dep /(i_nb_right_dep + i_nb_wrong_dep), 2),
                      i_strict_similar, i_strict_not_similar,
                       round(i_strict_not_similar/(i_strict_similar + i_strict_not_similar),2),
                       i_notstrict_similar, i_notstrict_not_similar,
                       round(i_notstrict_not_similar / (i_notstrict_similar + i_notstrict_not_similar), 2),
                      ])
file_lines.append([])
file_lines.append(['Blue_score_cases','Blue_score_sentences'])
file_lines.append([i_mean_blue_cases, i_mean_blue_sentences])
###########################################################



methods.writeCSV("../output/Blue_Invariant_similarity.csv", file_lines)
print("Done")