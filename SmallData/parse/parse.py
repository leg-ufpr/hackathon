import csv
import sys
import json


def parseToOneFile(csvName, jsonName):
    cars = {}
    csvFile = open(csvName)
    csvData = list(csv.reader(csvFile))

    for x in range(1, len(csvData)):
        line = csvData[x][0].replace("\"", "").split(";")
        idCar = line[0]
        attr = line[1]
        value = int(line[2])
        if (idCar in cars):
            cars[idCar][attr] = value
        else:
            cars[idCar] = {attr: value}

    data = json.load(open(jsonName))
    for x in data:

        if (len(x[4].split("Carro anterior")[0]) != 2):
            timeUsed = x[4].split(" - ")[0]
            distanceTraveled = x[4].split(" - ")[0]
            previousCar = ""
        else:
            timeUsed = x[4].split("Carro anterior")[0].split(" - ")[0]
            distanceTraveled = x[4].split("Carro anterior")[0].split(" - ")[1]
            previousCar = x[4].split("Carro anterior")[1]

        nameCar = x[2].split(" ")
        carYear = nameCar[-1]
        del nameCar[-1]
        nameCar = " ".join(nameCar)
        line = {
            "idCar": x[0],
            "shortDescrp": x[1].replace("\"", ""),
            "nameCar": " ".join(nameCar.split(" ")[:2]).lower(),
            "carYear": str(carYear.split("/")[-1]),
            "name": x[3].split(" - ")[1],
            "place": x[3].split(" - ")[1],
            "timeUsed": timeUsed,
            "distanceTraveled": distanceTraveled,
            "previousCar": previousCar,
            "pros": x[5].replace("Prós:", ""),
            "cons": x[6].replace("Contras:", ""),
            "defects": x[7].replace("Defeitos apresentados:", ""),
            "generalOpnion": x[8].replace("Opinião Geral:", ""),
            "date": x[9]
        }
        for y in line:
            if (line["idCar"] in cars):
                cars[line["idCar"]][y] = line[y]
            else:
                cars[line["idCar"]] = {y: line[y]}
    return cars
