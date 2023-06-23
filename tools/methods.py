import numpy
import numpy as np
import pandas as pd
import torch
import transformers
import datasets
import re
import cuda
import os.path
import csv
import pickle
import time


def predict(text, tokenizer, model, isMulti, max_length, device):
    inputs = tokenizer(text, truncation=True, return_tensors='pt', max_length=max_length).to(device)
    with torch.no_grad():
        logits = model(**inputs).logits
    positive = (logits >= 0.) if isMulti else (logits == max(logits[0]))
    predicted_class_id_tensor = positive[0].nonzero()  # return predicted class (multiclass)
    predicted_class_id = [predicted_class_id_tensor[i].item() for i in range(len(predicted_class_id_tensor))]
    return predicted_class_id


# Load predictions of the model from the file, or make them
def getPrediction(path, string_array, tokenizer, model, isMulti, max_length, device):
    size = len(string_array)
    prediction_file = path + "base_prediction.npy"
    if os.path.isfile(prediction_file):
        model_base_prediction = np.load(prediction_file, allow_pickle=True)
    else:
        print("Creating base predictions ...")
        model_base_prediction = [[]] * size
        for i in range(size):
            predicted_class_id = predict(string_array[i], tokenizer, model, isMulti, max_length, device)
            model_base_prediction[i] = predicted_class_id
        createDir(prediction_file)
        np.save(prediction_file, model_base_prediction)
    return model_base_prediction


def getLabelsCount(predictions, nb_label):
    labels_counter = [0] * nb_label
    for x in range(len(predictions)):
        for y in predictions[x]:
            labels_counter[y] += 1
    return labels_counter


def getTruncated(path, string_array, tokenizer, max_length):
    array_size = len(string_array)
    file_name = path + "truncated_text.pkl"
    if os.path.isfile(file_name):
        file = open(file_name, 'rb')
        truncated_text = pickle.load(file)
    else:
        print("Creating truncated text ...")
        truncated_text = [None] * array_size
        for i in range(array_size):
            encoded = tokenizer.encode(string_array[i], padding=True, truncation=True, max_length=max_length)
            truncated_text[i] = tokenizer.decode(encoded, skip_special_tokens=True)  # TODO better way ?
        file = createOpen(file_name, 'wb')
        pickle.dump(truncated_text, file)
    file.close()
    return truncated_text


def getFileName(path):
    index = path.rfind("/")
    index_point = path.rfind(".")
    if index_point == -1:
        index_point = None
    return path[index + 1:index_point]


def createDir(path):
    index = path.rfind("/")
    if (index != -1):
        os.makedirs(path[:index], exist_ok=True)


def createOpen(path, mode):
    createDir(path)
    if 'b' in mode:
        return open(path, mode)
    else:
        return open(path, mode, newline='', encoding='utf-8')


def swap_file_words(s, x, y):
    split = s.split('_')
    for word in range(len(split)):
        if split[word] == x:
            split[word] = y
        elif split[word] == y:
            split[word] = x
    return '_'.join(split)


def getMaskWords(text, tokenizer_bert, model_bert, n_prediction, device):
    inputs = tokenizer_bert(text, return_tensors="pt", truncation=True).to(device)
    with torch.no_grad():
        logits = model_bert(**inputs).logits
    mask_token_index = (inputs.input_ids == tokenizer_bert.mask_token_id)[0].nonzero(as_tuple=True)[0]
    list_logits = (logits[0, mask_token_index])[0]
    logits_sorted = list_logits.sort(descending=True)[0][0:n_prediction]
    index_words = [((list_logits == x).nonzero(as_tuple=True)[0]) for x in logits_sorted]
    return [tokenizer_bert.decode(index_words[x]) for x in range(len(index_words))]


def getFromPickle(pickle_file_path, mode):
    file = open(pickle_file_path, mode)
    file_content = pickle.load(file)
    file.close()
    return file_content

def writePickle(data, pickle_file_path, mode):
    file = createOpen(pickle_file_path, mode)
    pickle.dump(data, file)
    file.close()


def writeCSV(path, rows):
    csvfile = createOpen(path, 'w')
    csv_writer = csv.writer(csvfile, delimiter=';')
    csv_writer.writerows(rows)
    csvfile.close()


def getFiles(path):
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            files.append(os.path.join(r, file))
    return files

def lowerPriority(seen_words, words):
    set_words = set(words)
    for seen_word in seen_words:
        if seen_word in set_words:
            words.append(words.pop(words.index(seen_word)))
    return words

def getWordlist(path):
    word_list = pd.read_csv(path, delimiter=';', header=None).to_numpy() if os.stat(path).st_size != 0 else []
    a = word_list[:, 0] if len(word_list) != 0 else []
    b = word_list[:, 1] if len(word_list) != 0 else []
    file_name = getFileName(path)
    return file_name, a, b




