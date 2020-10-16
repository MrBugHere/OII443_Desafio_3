## OII443_Desafio_3

### Descripción
Manuel está interesado en el mercado del desarrollo móvil, por lo que comenzó a recopilar toda la información de las aplicaciones más descargadas de una tienda. Manuel le pide a su equipo (uds.) que le hagan un programa que, a partir de los datos recopilados, obtenga información de aplicaciones similares a las que se encuentra desarrollando.

### Solución

Para realizar el programa solicitado por manuel, el equipo acordó utilizar la estructura KDTree para determinar que aplicaciones son similares y poder analizar de mejor manera los datos recopilados por manuel.

### Preprocesamiento de datos

El preprocesado que se utiliza es el one hot encoding, en el caso de la columna Genre, se obtienen los elementos únicos para generar la matriz de ceros y unos. Por ejemplo la fila 1 referencia al elemento 1 del dataset y las columnas se refieren a todos los géneros que se encuentran en el dataset. Si el elemento pertenece al género 7, en la matriz se inserta un 1 en la fila 1 columna 7 para indicar ese género. Esto se aplica también a los datos ratingUser, price y contentRating.

### Implementación de KDTree

Para la implementación se utilizaron las clases KDnode y KDtree. La primera contiene la información que se está analizando. Luego la clase KDtree cuenta con los atributos: Nodo raíz, la data que se está analizando y las dimensiones. Dentro también se encuentra la función generateTree(), la cual es la encargada de crear el árbol que buscará los elementos de mayor similitud.

```python
class KDnode:
    def __init__(self, content, depth, split):
        self.content = content
        self.depth = depth
        self.split = split
        self.left = None
        self.right = None
``` 

```python
class KDtree:
    def __init__(self, data, dimensions):
        self.rootNode = None
        self.data = []
        self.data = data
        self.dimensions = dimensions
        self.generateTree()
```
La función generateTree() crea el nodo raíz y luego mediante la función expandNode() se expande, donde se itera este proceso dependiendo de los niveles que se deseen.


