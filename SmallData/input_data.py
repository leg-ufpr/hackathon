import parse.parse as Parse
from collections import Counter
import numpy as np

STOP_WORDS = ['ao', 'as', 'com', 'como', 'da', 'de', 'do', 'dos', 'em',
'mais', 'na', 'no', 'não', 'os', 'para', 'por', 'que', 'se', 'um', 'uma',
'das', 'ele', 'era', 'isso', 'mas', 'me', 'mesmo', 'nos', 'ou', 'pela',
'pelo', 'quando', 'quem', 'ser', 'seu', 'sua', 'são', 'só', 'está', 'eu',
'foi', 'há', 'já', 'muito', 'nas', 'tem', 'sem', 'seus', 'até', 'ter',
'vai', 'todos', 'tudo', 'você', 'ainda', 'bem', 'também', 'às', 'pode',
'entre', 'sobre', 'assim', 'nem', 'será', 'estão', 'lá', 'onde', 'aos',
'ali', 'meu', 'ela', 'essa', 'esse', 'ciosa', 'vem', 'vão', 'uso',
'usar', 'tão', 'têm', 'dá', 'aí', 'e', 'o', 'a', 'é', '-'
]



data = Parse.parseToOneFile("hackathon/notas.csv", "hackathon/opinioes.json")

l = []


def feature_array(data, class_value):
    pros = []
    cons = []
    defects = []
    generalOpnion = []

    for line in data:
        if data[line]["Recomendação"] == class_value:
            pros.append(data[line]["pros"].replace(",", " ").replace(".", " ").replace("!", " ").replace("?", " ").split(" "))
            cons.append(data[line]["cons"].replace(",", " ").replace(".", " ").replace("!", " ").replace("?", " ").split(" "))
            defects.append(data[line]["defects"].replace(",", " ").replace(".", " ").replace("!", " ").replace("?", " ").split(" "))
            generalOpnion.append(data[line]["generalOpnion"].replace(",", " ").replace(".", " ").replace("!", " ").replace("?", " ").split(" "))
    text = []

    for list in pros:
        for items in list:
            text.append(items)

    for list in cons:
        for items in list:
            text.append(items)

    for list in defects:
        for items in list:
            text.append(items)

    for list in generalOpnion:
        for items in list:
            text.append(items)

    return Counter(text)


def selectWordsFeatures():
    dict = [None] * 11

    for i in range(11):
        dict[i] = feature_array(data, i)

    allDict = {}
    for i,x in enumerate(dict):

        for y in x:
            if (y in STOP_WORDS):
                continue
            if(y == ''):
                continue
            if(y in allDict):
                allDict[y][i]=x[y]
            else:
                allDict[y] = {i:x[y]}
    #print(dict[0])
    results = []
    for x in allDict:
        arr = np.zeros(len(dict),dtype=np.int)
        for y in allDict[x]:
            arr[int(y)] = allDict[x][y]
        #vari = np.array(allDict[x]).std()
        #print(arr.std(), arr,x)
        results.append((x,arr.std()))

    sor = sorted(results, key=lambda x: x[1], reverse=True)

    selectedWords = [x[0] for x in sor]
    return((selectedWords[:50], dict))

#print(dict[0])

#print(len(Counter(l)))
