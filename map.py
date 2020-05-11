import time
from random import randint
from threading import Thread, Lock

from PyQt5.QtCore import *
from PyQt5.QtGui import *

from snake import Snake, Node


class Map:
    def __init__(self, parent):
        super().__init__()

        self.thread = Thread(target=self.play)
        self.lock = Lock()
        self.run_game = True
        self.keyboard_twice = True
        self.game_status = False
        self.food_count = 0
        self.lines = 15
        self.snake = Snake(self.lines)
        self.food = Node(-1, -1)
        self.parent = parent
        self.out_rectangle = parent.rect()
        self.in_rectangle = self.out_rectangle.adjusted(20, 20, -20, -20)

        self.width = self.in_rectangle.width() / self.lines
        self.height = self.in_rectangle.height() / self.lines

        self.left = self.in_rectangle.left()
        self.top = self.in_rectangle.top()
        self.right = self.in_rectangle.right()
        self.bottom = self.in_rectangle.bottom()

        self.rect = [[QRectF for _ in range(self.lines)] for _ in range(self.lines)]

        top_left = QPoint(self.left, self.top)
        size = QSize(self.width, self.height)

        for i in range(self.lines):
            for j in range(self.lines):
                self.rect[i][j] = QRect(self.left + (j * self.width)
                                        , self.top + (i * self.height)
                                        , self.width
                                        , self.height)
                self.rect[i][j].adjust(2, 2, -2, -2)

    def restart(self):
        del self.thread
        self.thread = Thread(target=self.play)

        self.run_game = True
        self.game_status = False
        self.keyboard_twice = True
        self.food_count = 0

        del self.snake
        self.snake = Snake(self.lines)

        del self.food
        self.food = Node(-1, -1)

    def draw(self, qp):
        i = 0
        self.lock.acquire()

        for node in self.snake.node:
            if i == 0:
                qp.setBrush(QColor(135, 206, 250))
            else:
                qp.setBrush(QColor(10, 15, 90, 60))

            if self.run_game:
                qp.drawRect(self.rect[node.y][node.x])

            i += 1

        self.lock.release()

        self.lock.acquire()
        if self.food.x != -1 and self.food.y != -1:
            qp.setBrush(QColor(255, 0, 0))
            qp.drawRect(self.rect[self.food.y][self.food.x])
        self.lock.release()

        qp.setFont(QFont('Monospace', 10))
        qp.drawText(self.in_rectangle, Qt.AlignTop | Qt.AlignLeft, 'SCORE:' + str(self.food_count))

        if not self.game_status:
            qp.setFont(QFont('Monospace', 20))
            qp.drawText(self.in_rectangle, Qt.AlignCenter, 'Press arrow key to start the game')

    def keypress(self, key):
        if (key == Qt.Key_Right or key == Qt.Key_Up or key == Qt.Key_Down) and not self.game_status:
            self.game_status = True
            self.snake.change_direction(key)
            self.thread.start()

        if (key == Qt.Key_Left or key == Qt.Key_Right or key == Qt.Key_Up or key == Qt.Key_Down) and self.game_status:
            if self.keyboard_twice:
                self.snake.change_direction(key)
                self.keyboard_twice = False

    def generate_food(self):
        if self.food.x != -1 and self.food.y != -1:
            return

        count = 0
        while True:
            x = randint(0, self.lines - 1)
            y = randint(0, self.lines - 1)
            node = Node(x, y)

            difference = False

            for snake_node in self.snake.node:
                if node == snake_node:
                    difference = True
                    break

            if not difference:
                self.food = node
                break

            if count >= self.lines * self.lines:
                break

            count += 1

    def ate_food(self, node):
        if self.food == node:
            return True
        else:
            return False

    def check_if_out(self, head):
        if head.x < 0 or head.x >= self.lines:
            return True
        elif head.y < 0 or head.y >= self.lines:
            return True
        else:
            return False

    def play(self):
        while self.run_game:
            self.lock.acquire()

            if not self.snake.move() or self.check_if_out(self.snake.node[0]):
                self.parent.update()
                self.run_game = False
                self.game_status = False
                self.lock.release()
                break

            self.generate_food()

            eat = self.ate_food(self.snake.node[0])

            if eat:
                self.snake.node_add()
                self.food_count += 1
                self.food.x = -1
                self.food.y = -1

            self.lock.release()

            self.keyboard_twice = True

            self.parent.update()
            time.sleep(0.3)

        if not self.game_status:
            self.parent.finish_signal.emit()
