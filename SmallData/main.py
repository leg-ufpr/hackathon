import numpy as np
import matplotlib.pyplot as plt


def plotBar(bars, namePlot):
    # bars = [ [name, size,std]] ]
    N = len(bars)
    men_means = []
    men_std = []
    names = []

    for x in bars:
        names.append(x[0])
        men_means.append(x[1])
        men_std.append(x[2])

    ind = np.arange(N)  # the x locations for the groups
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    # ~ rects1 = ax.bar(ind, men_means, width, color='r', yerr=men_std)
    rects1 = ax.bar(ind, men_means, width, color='r')
    for i, rect in enumerate(rects1):
        # ~ print(rect)
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., 1.01 * height,
                men_std[i],
                ha='center', va='bottom')

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Scores')
    ax.set_title(namePlot)
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(names)

    # ~ ax.legend([rects1[0]], ['Men'])
    # ~ autolabel(rects1)
    # ~ autolabel(rects2)

    plt.show()


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

attrNames = [
    "Custo-Benefício",
    "Recomendação"
]
cars = Parse.parseToOneFile(sys.argv[1], sys.argv[2])

placeNote = {}
for x in cars:
    averageNote = 0
    for y in attrNames:
        averageNote += cars[x][y]
    averageNote /= len(attrNames)
    place = cars[x]["place"].split(" ")[-1]
    # ~ place = cars[x]["place"]

    if (not (place in placeNote)):
        placeNote[place] = [
            averageNote,
            1
        ]
    else:
        placeNote[place][0] += averageNote
        placeNote[place][1] += 1

arrayToPlot = []
for p in placeNote:
    placeNote[p][0] /= placeNote[p][1]
    arrayToPlot.append(
        [
            p,
            placeNote[p][0],
            placeNote[p][1]
        ]
    )

# ~ print(placeNote)
plotBar(arrayToPlot, "Distribuição espacial (estado) com índices de satisfação (recomendação e custo benefício)")
