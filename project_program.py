import yaml
import pandas as pd
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch
from itertools import groupby
import csv
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from transformers import RobertaTokenizer, RobertaConfig, RobertaModel
import nltk
import nltk.data
nltk.download('punkt')
import string
import re
from joblib import dump, load
from sys import argv
import math
import time

tokenizer = AutoTokenizer.from_pretrained("microsoft/unixcoder-base")
model = AutoModel.from_pretrained("microsoft/unixcoder-base")


#  Загрузка обученной модели кандидата пароля
model1_candpass = load('NEW_ML1_CatBOOST')

# Загрузка обученной контекстной модели
Context_model = load('SVM_context_model.joblib')


# Считывание кода с файла
def code_to_str(file_text):
    code = str()
    if '.csv' in file_text:
        file = csv.reader(open(file_text, encoding="utf8"), delimiter=",")
        for line in file:
            code += str(line)
        return code
    else:
        for line in open(file_text, encoding='utf8'):
            code += str(line)
        return code


def input_for_context_model(path_to_file, ntokens = 30):
    code = code_to_str(path_to_file).split()
    snippets_mas = []
    tokens_mas = []
    c = 0
    for i, token in enumerate(code):
        if c < ntokens - 1 and ntokens <= len(code) - i:
            tokens_mas.append(token)
            c += 1
        elif ntokens > len(code) - i:
            tokens_mas.extend(code[i:len(code)])
            snippets = " ".join(tokens_mas)
            snippets_mas.append(snippets)
            break
        else:
            tokens_mas.append(token)
            c = 0
            snippets = " ".join(tokens_mas)
            snippets_mas.append(snippets)
            tokens_mas = []
    return snippets_mas


def tokenization(file_text):
    tokens = []
    tokens += nltk.word_tokenize(file_text)
    #Очистка от знаков препинания:
    tokens = [i for i in tokens if check_ascii(i)]
    #Очистка от пустых элементов и элементов длинной <= 3:
    tokens = [i for i in tokens if len(i) > 3 and len(i) < 20]
    return tokens


#Проверка на ASCII-символы
def check_ascii(text):
    for each_char in text:
        if each_char not in string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation:
            return False
    else:
        return True


# Счетчик символов
def count(token, chartype):
    c = 0
    for char in token:
        if char in chartype:
            c += 1
    return c


#Функция вычисления энтропии слова    
def entropy(token):
    p = 0
    Ent = 0
    for char in token:
        if char in string.ascii_uppercase:
            p = 1/26                   # англ.буквы
        elif char in string.ascii_lowercase:
            p = 1/26                   # англ.буквы
        elif char in string.digits:
            p = 1/10                   # цифры
        elif char in string.punctuation:
            p = 1/32
        Ent += p * math.log2(1/p)               
    return round(Ent, 2)


#Функции вычисления количества заглавных, строчных букв, цифр и спец.символов:
upper_letters_count = lambda token: round(len(re.findall('[A-Z]', token)) / len(token), 2)
lower_letters_count = lambda token: round(len(re.findall('[a-z]', token)) / len(token), 2)
digit_count = lambda token: round(len(re.findall("[0-9]", token)) / len(token), 2)
special_count = lambda token: round(count(token, string.punctuation) / len(token), 2)


#Подготовка токенов к обработки в ML1
def tokens_prepare_ML1(tokens):
    df = pd.DataFrame(tokens)
    df = df.rename(columns={0: 'Input'})
    df = df.drop_duplicates()
    df.dropna()
    df['Length'] = df['Input'].apply(len)
    df['Uppercase'] = df['Input'].apply(upper_letters_count)
    df['Lowercase'] = df['Input'].apply(lower_letters_count)
    df['Digits'] = df['Input'].apply(digit_count)
    df['Special'] = df['Input'].apply(special_count)
    df['Entropy'] = df['Input'].apply(entropy)
    df = df.reindex(columns=['Input', 'Length', 'Uppercase', 'Lowercase', 'Digits', 'Special', 'Entropy'])
    df = df.reset_index(drop=True)
    return df


# Кастомный тресхолд
def custom_predict(X, threshold):
    probs = model1_candpass.predict_proba(X) 
    return (probs[:, 1] > threshold).astype(int)


# Векторизация для берта
def tokenize_for_BERT(snippet):
    code_tokens=tokenizer.tokenize(snippet)
    tokens = [tokenizer.cls_token]+code_tokens+[tokenizer.sep_token]
    tokens_ids = tokenizer.convert_tokens_to_ids(tokens)
    return tokens_ids


# Удаление дубликатов в массиве
def drop_duplicates(list):
    n = []
    for i in list:
        if i not in n:
            n.append(i)
    return n


# Функция работы модели кандидата пароля
def model_cand_pass(path):
    input = tokens_prepare_ML1(tokenization(model_context(path)))
    X_for_Model1 = input.drop('Input', axis = 1).values
    model1_candpass.predict(X_for_Model1)
    new_preds = custom_predict(X=X_for_Model1, threshold=0.5)
    results = {'Snippet': input['Input'].tolist(), 'Target': new_preds}
    df = pd.DataFrame(results)
    passwords_mas = df[df['Target'] == 1]['Snippet'].tolist()
    return passwords_mas


# Функция работы модели анализа окружения:
def model_context(path):
    check_file = input_for_context_model(path)
    preds_for_snippets = []
    snippet_mas = []
    for snippet in check_file:
        tokens_ids = tokenize_for_BERT(snippet)
        context_embeddings = model(torch.tensor(tokens_ids)[None,:])[0]
        pred =  Context_model.predict([context_embeddings[0][0][:].detach().numpy()])
        if pred == 1:
            snippet_mas.append(snippet)
    return " ".join(snippet_mas)


def find_secrets(path):
    result = {}
    passwords_mas = model_cand_pass(path)
    with open(path) as f:
        mylist = [line.rstrip('\n') for line in f]
        for i, string in enumerate(mylist):
            for password in passwords_mas:
                if password in string:
                    result.update({i:string})
    return(result)


# if __name__ == '__main__':
#     while True:
#         # Проверка наличия нового файла
#         if new_file_available(): #ФУНКЦИЯ ПОЛУЧЕНИЯ НОВОГО ФАЙЛА(НЕОБХОДИМО ПРОПИСАТЬ)
#             # Обработка нового файла
#             with open(work_dir + 'pathes.txt', 'r') as f:
#                 var = f.readline().split()
#             for path in var:
#                 path = path.rstrip()
#                 # Работа первой модели
#                 passwords_mas = model1(path)
#                 # Работа второй модели
#                 res_preds = model2(path)
#                 #Файл json с результатом
#                 snippets_with_pass = res_preds[res_preds['Target'] == 1]['Snippet']
#                 snippets_with_pass.to_json('FindPasswords.json')

#                 #Вывод результата с именем файла и единичками в лог
#                 print(path,'Найденные пароли:', res_preds[res_preds['Target'] == 1]['Snippet'], sep = '\n')
#         else:
#             # Задержка на 1 секунду
#             time.sleep(1)

