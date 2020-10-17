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
            value += distance[k] ** 2

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

    def knn(self, node, point, k, dist_func, return_distances=True, i=0, heap=None):
        import heapq
        is_root = not heap
        if is_root:
            heap = []
        if node is not None:
            dist = dist_func(point, node.content)
            dx = node.content[i] - point[i]
            if len(heap) < k:
                heapq.heappush(heap, (-dist, node.content))
            elif dist < -heap[0][0]:
                heapq.heappushpop(heap, (-dist, node.content))
            i = (i + 1) % self.dimensions
            # Goes into the left branch, and then the right branch if needed
            nextNode = [node.left, node.right]
            for b in [dx < 0] + [dx >= 0] * (dx * dx < -heap[0][0]):
                self.knn(nextNode[b], point, k, dist_func, return_distances, i, heap)
        if is_root:
            neighbors = sorted((-h[0], h[1]) for h in heap)
            return neighbors if return_distances else [n[1] for n in neighbors]
