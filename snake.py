from PyQt5.QtCore import Qt


class Node:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False


class Snake:
    def __init__(self, lines):
        self.node = []
        self.add_block = False
        self.direction = Qt.Key_Right
        self.initialize(lines)

    def initialize(self, lines):
        x_coordinate = lines // 2
        y_coordinate = lines // 2
        for i in range(3):
            self.node.append(Node(x_coordinate, y_coordinate))
            x_coordinate -= 1

    def change_direction(self, key):
        self.direction = key

    def crashed(self):
        if self.node_count():
            return False

        head = Node(self.node[0].x, self.node[0].y)
        body_list = self.node[4:]

        for body in body_list:
            if head == body:
                return True

        return False

    def move(self):
        if self.crashed():
            return False

        head = Node(self.node[0].x, self.node[0].y)

        if self.direction == Qt.Key_Left:
            head.x -= 1
        elif self.direction == Qt.Key_Right:
            head.x += 1
        elif self.direction == Qt.Key_Up:
            head.y -= 1
        elif self.direction == Qt.Key_Down:
            head.y += 1

        self.node.insert(0, head)

        if self.add_block:
            self.add_block = False
        else:
            self.node.pop()

        return True

    def node_add(self):
        self.add_block = True

    def node_count(self):
        return len(self.node)
