import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.multiclass import OutputCodeClassifier

from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import BaggingClassifier
from itertools import product
from sklearn.ensemble import VotingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree

import sys
import extract_features
import random
#~ random.shuffle(array)


aux = extract_features.extract()
data = []
labels = []
for x in aux:
	data.append(x[-1])
	labels.append(x[:-1])
	
print(labels)


mlp = BaggingClassifier(MLPClassifier(
 solver='lbfgs',
 alpha=1e-5,
 activation=('logistic'),
 hidden_layer_sizes=(30),
 learning_rate_init=0.001,
 max_iter=100000, random_state=1
))

mlp.fit(data, labels)

knnT = BaggingClassifier(KNeighborsClassifier(n_neighbors=5))
parameters = {'n_neighbors': [1, 15]}
knn = GridSearchCV(knnT, parameters)
knn.fit(data, labels)

rdfT = RandomForestClassifier(max_depth=2, random_state=0, n_estimators=20)
parameters = {'max_depth': [2, 10], 'n_estimators': [10, 30]}
rdf = GridSearchCV(rdfT, parameters)
rdf.fit(data, labels)

parameters = {'kernel': ('linear', 'rbf'), 'C': [1, 5]}
svr = svm.SVC(probability=True)
clf = GridSearchCV(svr, parameters)
clf.fit(data, labels)

eclf = VotingClassifier(estimators=[('rdf', rdf), ('svm', clf), ('knn', knn), ('mlp', mlp)], voting='soft',
					 weights=[2.5, 1, 1, 3])
eclf = eclf.fit(data, labels)

file = open(sys.argv[2])
file.readline()
acertos = 0.0
erros = 0.0


testX = []


testY = []

for line in file:
 line = line.replace("\n", "")
 line = line.split(" ")
 label = int(line[-1])
 del line[-1]
 for i, x in enumerate(line):
	 line[i] = float(x)
 testX.append(line)
 testY.append(label)
file.close()

cKnn = []
cmlp = []
cSvm = []
cRdf = []
ultimoPredict = []

for x in testX:
 cSvm.append(clf.predict(np.array(x).reshape(1, -1))[0])
 cKnn.append(knn.predict(np.array(x).reshape(1, -1)))
 cmlp.append(mlp.predict(np.array(x).reshape(1, -1)))
 cRdf.append(rdf.predict(np.array(x).reshape(1, -1)))
 ultimoPredict.append(eclf.predict(np.array(x).reshape(1, -1)))

if len(sys.argv) > 3 and sys.argv[3].split("=")[0].lower() == "debug" and sys.argv[3].split("=")[1].lower() == "true":
 print("rdf")
 print(rdf.score(testX, testY))
 print(confusion_matrix(cRdf, testY))
 print("")
 print("knn")
 print(knn.score(testX, testY))
 print(confusion_matrix(cKnn, testY))
 print("")
 print("mlp")
 print(mlp.score(testX, testY))
 print(confusion_matrix(cmlp, testY))
 print("")
 print("svm")
 print(clf.score(testX, testY))
 print(confusion_matrix(cSvm, testY))
 print("")

 print("classificacao")
 print(eclf.score(testX, testY))
 confusion_matrix(ultimoPredict, testY)

else:
 print(ultimoPredict)

