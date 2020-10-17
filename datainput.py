import pandas as pd
import numpy as np


class DataInput:
    def __init__(self, filePath):
        # Recibe como argumento la direcccion del documento CSV (filepath) y crea DataFrame con un numpy array 2D

        self.dataPD = pd.read_csv(filePath)
        self.dataNP = self.dataPD.to_numpy()
        self.dataPoints = []
        self.dataNames = []
        self.createData()

    def createData(self):
        for i in range(0, len(self.dataPD.axes[0])):
            data = [self.dataNP[i][3], self.dataNP[i][5], self.dataNP[i][6], self.dataNP[i][8]]
            name = [self.dataNP[i][2], data]
            self.dataNames.append(name)
            self.dataPoints.append(data)

    def createGenreMatrix(self):
        # Crea Matriz genre y array de generos detectados en el csv

        self.genres = self.dataPD.prime_genre.unique()
        rows = len(self.dataPD.axes[0])
        colums = len(self.genres)
        self.genreMatrix = np.zeros((rows, colums), dtype=int)

        for i in range(0, rows):
            for j in range(0, colums):
                if self.dataNP[i][12] == self.genres[j]:
                    self.genreMatrix[i][j] = 1
                    break
