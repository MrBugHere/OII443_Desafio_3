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

    def knn(self, point, k):
        pass


if __name__ == "__main__":
    points = [[5,8,7],[3,4,9],[9,2,7],[7,8,1],[0,9,9],[1,1,2],[8,7,9],[2,5,7],[0,1,5],[1,5,2],[6,5,3],[3,3,3],[7,7,4],[5,4,5],[0,0,0]]
    alt = [[7,2],[2,3],[5,4],[9,6],[4,7],[8,1]]
    orderedData = sorted(points, key=operator.itemgetter(0))
    kd = KDtree(points, 3)
    kd.printTree()
