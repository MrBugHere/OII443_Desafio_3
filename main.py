from time import perf_counter
from kdtree import KDtree
from datainput import DataInput


def arr_distance_sqrd(point1, point2, dim):
    distance = []
    value = 0

    for k in range(0, dim):
        distance.append(point1[k] - point2[k])

    for k in range(0, dim):
        value += distance[k] ** 2

    return value


def arr_closest_point(all_points, new_point, dimensions):
    best_point = None
    best_distance = None

    for current_point in all_points:
        current_distance = arr_distance_sqrd(new_point, current_point, dimensions)

        if best_distance is None or current_distance < best_distance:
            best_distance = current_distance
            best_point = current_point

    return best_point


def bench1(testData, testPoint):
    result = arr_closest_point(testData, testPoint, 4)
    return result


def bench2(testData, testPoint):
    tree = KDtree(testData, 4)
    result = tree.knn(tree.rootNode, testPoint, 10, tree.distance_sqrd)
    return result


def bench3(testData, testPoint):
    tree = KDtree(testData, 4)
    result = tree.kd_closest_point(testPoint)
    return result

if __name__ == "__main__":
    print('Hola bienvenido')
    nombre_archivo = 'Desafio3.csv'
    # data = DataInput("\\Users\\Leonardo\\Documents\\Clases EDA Avanzada\\Desafio EDA\\desafio 3\\OII443_Desafio_3-Jose\\Desafio3.csv")
    data = DataInput(nombre_archivo)
    point = [22424, 12.99, 222, 3]

    t1_start = perf_counter()
    result1 = bench1(data.dataPoints, point)
    t1_stop = perf_counter()

    t2_start = perf_counter()
    result2 = bench2(data.dataPoints, point)
    t2_stop = perf_counter()

    t3_start = perf_counter()
    result3 = bench3(data.dataPoints, point)
    t3_stop = perf_counter()

    tree = KDtree(data.dataPoints, 4)
    tree.printTree()

    print("Tiempo usando array y fuerza bruta:", t1_stop - t1_start)
    print("Resultado:", result1)
    print()
    print("Tiempo usando kd_tree y 10 knn:", t2_stop - t2_start)
    print("Resultado:", result2)
    print()
    print("Tiempo usando kd_tree y el punto más cercano:", t3_stop - t3_start)
    print("Resultado:", result3)

