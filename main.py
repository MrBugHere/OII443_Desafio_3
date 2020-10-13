import math
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
        newNode = KDnode(median, dim + 1, len(orderedData) // 2)  # Se crea el nodo raíz usando el valor obtenido
        if direction == 0:
            node.left = newNode
        else:
            node.right = newNode
        leftlist, rightlist = split_list(orderedData)
        self.expandNode(newNode, leftlist, dim + 1, 0)
        self.expandNode(newNode, rightlist, dim + 1, 1)

    def distance_sqrd(self, point1, point2):
        distance = []
        value = 0

        for k in range(0, self.dimensions):
            distance.append(point1[k] - point2[k])

        for k in range(0, self.dimensions):
            value += distance[k] * distance[k]

        return value

    def closer_distance(self, pivot, p1, p2):
        if p1 is None:
            return p2

        if p2 is None:
            return p1

        d1 = self.distance_sqrd(pivot, p1)
        d2 = self.distance_sqrd(pivot, p2)

        return p1 if d1 < d2 else p2

    class Printer:
        def __init__(self, text):
            self.text = text

    def printTree(self):
        print(self.traversePreOrder(self.rootNode))

    def traversePreOrder(self, root):
        printer = self.Printer('')
        printer.text = ''.join([printer.text, str(root.content)])

        pointerRight = "└──"
        pointerLeft = "├──" if root.right is not None else "└──"

        sibling = True if root.right is not None else False

        self.traverseNodes(printer, "", pointerLeft, root.left, sibling)
        self.traverseNodes(printer, "", pointerRight, root.right, False)

        return printer.text

    def traverseNodes(self, printer, padding, pointer, node, hasRightSibling):
        if node is not None:
            printer.text = ''.join([printer.text, '\n', padding, pointer, str(node.content)])
            padding = ''.join([padding, "│  "]) if hasRightSibling else ''.join([padding, "   "])
            pointerRight = "└──"
            pointerLeft = "├──" if node.right is not None else "└──"
            sibling = True if node.right is not None else False
            self.traverseNodes(printer, padding, pointerLeft, node.left, sibling)
            self.traverseNodes(printer, padding, pointerRight, node.right, False)

    def arr_closest_point(self, all_points, new_point):
        best_point = None
        best_distance = None

        for current_point in all_points:
            current_distance = self.distance_sqrd(new_point, current_point)

            if best_distance is None or current_distance < best_distance:
                best_distance = current_distance
                best_point = current_point

        return best_point

    def kd_closest_point(self, point):
        return self.closest_point(self.rootNode, point)

    def closest_point(self, root, point, depth=0):
        if root is None:
            return None

        axis = depth % self.dimensions

        next_branch = None
        opposite_branch = None

        if point[axis] < root.content[axis]:
            next_branch = root.left
            opposite_branch = root.right
        else:
            next_branch = root.right
            opposite_branch = root.left

        best = self.closer_distance(point,
                                    self.closest_point(next_branch,
                                                       point,
                                                       depth + 1),
                                    root.content)

        if self.distance_sqrd(point, best) > (point[axis] - root.content[axis]) ** 2:
            best = self.closer_distance(point,
                                        self.closest_point(opposite_branch,
                                                           point,
                                                           depth + 1),
                                        best)

        return best

    def knn(self, point, k):
        pass


if __name__ == "__main__":
    points = [[5, 8, 7], [3, 4, 9], [9, 2, 7], [7, 8, 1], [0, 9, 9], [1, 1, 2], [8, 7, 9], [2, 5, 7], [0, 1, 5],
              [1, 5, 2], [6, 5, 3], [3, 3, 3], [7, 7, 4], [5, 4, 5], [0, 0, 0]]
    alt = [[7, 2], [2, 3], [5, 4], [9, 6], [4, 7], [8, 1]]
    test = [[4,7],[11,10],[9,4],[15,3],[7,13],[16,10],[14,11]]
    orderedData = sorted(test, key=operator.itemgetter(0))
    kd = KDtree(test, 2)
    kd.printTree()

    point = [14,9]
    print(kd.arr_closest_point(test, point))
    found = kd.kd_closest_point(point)
    print(found)
    distance = math.sqrt(kd.distance_sqrd(point, found))
    print("distance: %f" % distance)
