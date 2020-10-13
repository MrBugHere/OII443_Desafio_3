import pandas as pd
import numpy as np
from sklearn.neighbors import KDTree




class DataInput:
    def __init__(self, filePath):
        # Recibe como argumento la direcccion del documento CSV (filepath) y crea DataFrame con un numpy array 2D

        self.dataPD = pd.read_csv(filePath)
        self.dataNP = self.dataPD.to_numpy()
        
    def createGenreMatrix(self):
        # Crea Matriz genre y array de generos detectados en el csv

        self.genres =  self.dataPD.prime_genre.unique()
        rows = len(self.dataPD.axes[0])
        colums = len(self.genres)
        self.genreMatrix = np.zeros((rows, colums), dtype=int)

        for i in range(0,rows):
            for j in range(0,colums):
                if  self.dataNP[i][12] == self.genres[j]:
                    self.genreMatrix[i][j] = 1
                    break


    def createPriceMatrix(self):
        #  Crea Matriz Price y array de precios detectados en el csv

        self.prices = np.sort(self.dataPD.price.unique())
        rows = len(self.dataPD.axes[0])
        colums = len(self.prices)
        self.priceMatrix = np.zeros((rows, colums), dtype=int)

        for i in range(0,rows):
            for j in range(0,colums):
                if  self.dataNP[i][5] == self.prices[j]:
                    self.priceMatrix[i][j] = 1
                    break

    def createRatingUserMatrix(self):
        # Crea Matriz ratingsUser array de ratings detectados en el csv
  
        self.ratingUser = np.sort(self.dataPD.user_rating.unique())
        rows = len(self.dataPD.axes[0])
        colums = len(self.ratingUser)
        self.ratingUserMatrix =np.zeros((rows, colums), dtype=int)

        for i in range(0,rows):
            for j in range(0,colums):
                if  self.dataNP[i][8] == self.ratingUser[j]:
                    self.ratingUserMatrix[i][j] = 1
                    break

    def createContentRatingMatrix(self):

        # Crea Matriz contentRating y array de los ratings de los contenidos detectados en el csv

        self.contentRating = self.dataPD.cont_rating.unique()
        rows = len(self.dataPD.axes[0])
        colums = len(self.contentRating)
        self.contentRatingMatrix = np.zeros((rows,colums), dtype=int)

        for i in range(0,rows):
            for j in range(0,colums):
                if  self.dataNP[i][11] == self.contentRating[j]:
                    self.contentRatingMatrix[i][j] = 1
                    break
    
    def imprimirDataPD(self):
        print(self.dataPD['rating_count_ver'])
    
    def imprimirDataNP(self):
        print(self.dataNP)
    
    def getElementoPD_id(self,id):
        for ids,group in self.dataPD.groupby('id'):
            if ids == id:
                new_df = group
        return new_df
    
def diez_mas_cercanos(genreMatrix):
        
    #print('datos en el arreglo',self.contentRatingMatrix)
    tree = KDTree(genreMatrix,leaf_size=2)
    dist,ind = tree.query(genreMatrix[:1], k=10)
    print(ind)
    print(dist)


def main():
    print('Hola bienvenido')
    nombre_archivo = '\\Users\\Leonardo\\Documents\\Clases EDA Avanzada\\Desafio EDA\\desafio 3\\OII443_Desafio_3-Jose\\Desafio3.csv'
    #data = DataInput("\\Users\\Leonardo\\Documents\\Clases EDA Avanzada\\Desafio EDA\\desafio 3\\OII443_Desafio_3-Jose\\Desafio3.csv") 
    data = DataInput(nombre_archivo)
    data.createGenreMatrix()
    data.createContentRatingMatrix()

    #data.imprimirDataPD()
    #elemento = data.getElementoPD_id(282935706)
    #print(elemento)
    diez_mas_cercanos(data.genreMatrix)
    #data.imprimirDataNP()
if __name__ == "__main__":
    main()
    pass