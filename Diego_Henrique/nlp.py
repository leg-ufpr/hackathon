# -*- coding: utf-8 -*-

'''
depois do preprocesasmento estar pronto, puxar as features de opinoes
'''

import nltk
import pandas as pd
import numpy as np
from string import punctuation
from collections import OrderedDict
import matplotlib.pyplot as plt
from operator import itemgetter

df = pd.read_csv("./data/comentarios.csv")
df.drop('ID', inplace = True, axis = 1)

df['Prós'] = df['Prós'].apply(lambda x: x[5:])
df['Contras'] = df['Contras'].apply(lambda x: x[8:])
df['Defeitos'] = df['Defeitos'].apply(lambda x: x[22:])
df['Opinião'] = df['Opinião'].apply(lambda x: x[14:])

opiniao_cols = ['Prós','Contras','Defeitos','Opinião']

with open('./stopwords.txt','r') as f:
    stop_words = f.read()

def clean_data(x):

   x =  ''.join([c for c in x if c not in punctuation])
   x = x.lower()
   x = x

   return x
   
def get_columns_len():
    
    for feature in opiniao_cols:        
        aux = list()
        for index,row in df[feature].iteritems():
            aux.append(len(row))
        
        aux = pd.Series(aux)
        df[feature+"_tamanho_letras"] = aux.values
            
def get_all_text(feature):
    
    words = list()

    for index,row in df[feature].iteritems():
        palavras = row.split()
        for word in palavras:
            words.append(word)
            
    return words

        
def get_vocab(bag):
    
    vocab_to_int = dict()
    counter = 1
    for word in bag:
        if word not in vocab_to_int.keys():    
            vocab_to_int[word] = counter
            counter+=1
        else:    
            pass
        
    return vocab_to_int

def get_word_frequency(bag):
    aux = dict()
    
    counter = 1
    for word in bag:
        
        if word not in aux.keys():
            aux[word] = counter
        else:
            aux[word] += 1
    
    return aux

def limit_set(aux,min_length,min_freq):
    '''
    Metodo para limitar o bag of Words, existem palavras com poucas frequencias
    e palavras nao muito uteis como artigos (e,as ,os), existem muitas palavras que são numeros
    relacionados a quilometragem, que contribuem para o ruído do dataset
    '''
    keys = []
    for key in aux.keys():
        if len(key) < min_length or aux[key] < min_freq or key.isdigit() or key in stop_words or key.find('km')!=-1 or key.find('mil')!=-1:
            keys.append(key)
            
    for key in keys:
        del aux[key]
        
    return aux
    
def plot_most_common_words(dic_freq, number):
    
    dic_freq = OrderedDict(sorted(dic_freq.items(), key=itemgetter(1), reverse=True))

    y = list(dic_freq.values())
    x = list(dic_freq.keys())
    
    y = y[:number]
    x = x[:number]
    
    plt.figure()
    plt.title('Top 10 Palavras Bag of Words Comentários Prós')
    plt.bar(x,y)
    plt.xticks(rotation = 45)
    
df['Prós'] = df['Prós'].apply(lambda x: clean_data(x))
df['Contras'] = df['Contras'].apply(lambda x: clean_data(x))
df['Defeitos'] = df['Defeitos'].apply(lambda x: clean_data(x))
df['Opinião'] = df['Opinião'].apply(lambda x: clean_data(x))

get_columns_len()

pros_bag = get_all_text('Prós')
contras_bag = get_all_text('Contras')
defeitos_bag = get_all_text('Defeitos')
opiniao_bag = get_all_text('Opinião')

'''
Filtramos o Bag of Words tanto por frequencia do uso de palavras
quando ao tamanho minimo das palavras
'''

pros_freq = limit_set(get_word_frequency(pros_bag),4,10)
defeitos_freq = limit_set(get_word_frequency(defeitos_bag),4,10)
contra_freq = limit_set(get_word_frequency(contras_bag),4,10)
opiniao_freq = limit_set(get_word_frequency(opiniao_bag),4,10)


plot_most_common_words(pros_freq,10)
plot_most_common_words(contra_freq,15)

bigramas = list(nltk.bigrams(opiniao_bag))

bigramas.most_common()









