import pandas as pd
import numpy as np
#from sklearn.neighbors import KDTree

import operator


class KDnode:
    def __init__(self, content, depth, split):
        self.content = content
        self.depth = depth
        self.split = split
        self.left = None
        self.right = None


def split_list(originalList):
    half = len(originalList) // 2
    return originalList[:half], originalList[half + 1:]


class KDtree:
    def __init__(self, data, dimensions):
        self.rootNode = None
        self.data = []
        self.data = data
        self.dimensions = dimensions
        self.generateTree()

    def generateTree(self):
        orderedData = sorted(self.data,
                             key=operator.itemgetter(0))  # Ordena la lista con respecto a la primera dimension
        median = orderedData[len(orderedData) // 2]  # Se consigue la mediana de la lista
        rootNode = KDnode(median, 0, len(orderedData) // 2)  # Se crea el nodo raíz usando el valor obtenido
        self.rootNode = rootNode
        leftlist, rightlist = split_list(orderedData)
        self.expandNode(rootNode, leftlist, 0, 0)
        self.expandNode(rootNode, rightlist, 0, 1)

    def expandNode(self, node, points, dim, direction):
        if not points:
            return
        orderedData = sorted(points, key=operator.itemgetter((dim + 1) % self.dimensions))
        median = orderedData[len(orderedData) // 2]  # Se consigue la mediana de la lista
        newNode = KDnode(median, dim+1, len(orderedData) // 2)  # Se crea el nodo raíz usando el valor obtenido
        if direction == 0:
            node.left = newNode
        else:
            node.right = newNode
        leftlist, rightlist = split_list(orderedData)
        self.expandNode(newNode, leftlist, dim+1, 0)
        self.expandNode(newNode, rightlist, dim+1, 1)

    def printTree(self):
        print(self.rootNode.content)


'''if __name__ == "__main__":
    points = [[5,8,7],[3,4,9],[9,2,7],[7,8,1],[0,9,9],[1,1,2],[8,7,9],[2,5,7],[0,1,5],[1,5,2],[6,5,3],[3,3,3],[7,7,4],[5,4,5],[0,0,0]]
    alt = [[7,2],[2,3],[5,4],[9,6],[4,7],[8,1]]
    orderedData = sorted(points, key=operator.itemgetter(0))
    kd = KDtree(points, 3)
    kd.printTree()'''


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
    
'''def diez_mas_cercanos(genreMatrix):
        
    #print('datos en el arreglo',self.contentRatingMatrix)
    tree = KDTree(genreMatrix,leaf_size=2)
    dist,ind = tree.query(genreMatrix[:1], k=10)
    print(ind)
    print(dist)'''

def diez_mas_cercanos_KDTree(genreMatrix):
    tree = KDtree(genreMatrix,10)
    tree.printTree()

def main():
    print('Hola bienvenido')
    nombre_archivo = 'Desafio3.csv'
    #data = DataInput("\\Users\\Leonardo\\Documents\\Clases EDA Avanzada\\Desafio EDA\\desafio 3\\OII443_Desafio_3-Jose\\Desafio3.csv") 
    data = DataInput(nombre_archivo)
    data.createGenreMatrix()
    data.createContentRatingMatrix()

    #data.imprimirDataPD()
    #elemento = data.getElementoPD_id(282935706)
    #print(elemento)
    diez_mas_cercanos_KDTree(data.contentRating)
    #data.imprimirDataNP()
if __name__ == "__main__":
    main()
    pass