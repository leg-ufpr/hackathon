
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
import json 
from unidecode import unidecode
from textblob import TextBlob
import sys

# ## Lendo Dados
column = int(sys.argv[1]) #1,5,6,7,8

js = np.array(json.load(open('../hackathon/opinioes.json')))
df_opinioes = pd.DataFrame.from_dict(js)
df = pd.read_csv('../hackathon/notas.csv',sep=';')

js_copy = js.copy()
opinioes = list()


## Lendo Dados

for i in range(js_copy.shape[0]):
    print(i,'/',js_copy.shape[0])
    #========================
    #Ajustando Dados
    
    text = js_copy[i][column]
    if column == 1:   #remove aspas
        text = text[1:-1]
    elif column == 5: #remove 'Pros:'
        text = text[5:]
    elif column == 6: #remove 'Contras:'
        text = text[8:]
    elif column == 7: #remove 'Defeitos apresentados:'
        text = text[22:]
    elif column == 8: #remove 'Opinião Geral:'
        text = text[14:]
    
    #========================
    #Analise de sentimentos
    
    try:
        #tentando analisar direto
        text = TextBlob(text)
        text = TextBlob(str(text.translate(from_lang='pt',to='en')))
        opinioes.append([js_copy[i][column],str(text),text.sentiment.polarity,text.sentiment.subjectivity])
        #print(opinioes[-1])
    except:
        try:
            #removendo acentos para tentar analisar
            text = TextBlob(unidecode(text))
            text = TextBlob(str(text.translate(from_lang='pt',to='en')))
            opinioes.append([js_copy[i][column],str(text),text.sentiment.polarity,text.sentiment.subjectivity])
            #print(opinioes[-1])
        except:
            opinioes.append([js_copy[i][column],str(text),None,None])
            print('ERRO: ',js_copy[i][column])   


# ## Salvando 
df_op = pd.DataFrame(opinioes,columns=['id','text','polarity','subjectivity'])
df_op.to_csv('sent_'+str(column)+'.csv',index=False)

