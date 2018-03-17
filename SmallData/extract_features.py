import input_data
from collections import Counter



import numpy as np

import csv
import sys
import json
import parse.parse as Parse

# ~ attrNames = [
# ~ "Estilo",
# ~ "Acabamento",
# ~ "Posição de dirigir",
# ~ "Instrumentos",
# ~ "Interior",
# ~ "Porta-malas",
# ~ "Desempenho",
# ~ "Motor",
# ~ "Câmbio",
# ~ "Freios",
# ~ "Suspensão",
# ~ "Consumo",
# ~ "Estabilidade",
# ~ "Custo-Benefício",
# ~ "Recomendação",
# ~ "Estilo"
# ~ ]

def extract():
    attrNames = [
        "Custo-Benefício",
        "Recomendação"
    ]

    data = Parse.parseToOneFile("hackathon/notas.csv", "hackathon/opinioes.json")
    wordFeatures, texts = input_data.selectWordsFeatures()

    def groupBy(data, key):
        ret = {}
        for x in data:
            val = data[x][key]
            if (val in ret):
                ret[data[x][key]].append(data[x])
            else:
                ret[data[x][key]] = [data[x]]
        return ret


    grupos = groupBy(data, "Recomendação")

    dicioIndex = {}
    for i, word in enumerate(wordFeatures):
        dicioIndex[word] = i

    print(wordFeatures)

    features = []
    for g in grupos:
        for x in grupos[g]:
            texto = x["pros"].replace(",", " ").replace(".", " ").replace("!", " ").replace("?", " ").split(" ")
            texto += x["cons"].replace(",", " ").replace(".", " ").replace("!", " ").replace("?", " ").split(" ")
            texto += x["defects"].replace(",", " ").replace(".", " ").replace("!", " ").replace("?", " ").split(" ")
            texto += x["generalOpnion"].replace(",", " ").replace(".", " ").replace("!", " ").replace("?", " ").split(" ")
            vetCaracs = np.zeros(len(wordFeatures)+1)
            vetCaracs[-1] = x["Recomendação"]
            counter = Counter(texto)
            for i,palavra in enumerate(wordFeatures):
                if(palavra in counter):
                    vetCaracs[i] = counter[palavra]
            features.append(vetCaracs)
    return features