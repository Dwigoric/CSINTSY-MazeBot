import sys

from PyQt5.QtWidgets import QApplication, QLabel, QFileDialog, QWidget, QGridLayout, QPushButton, QVBoxLayout, \
    QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QPainter, QColor, QBrush, QFont
from PyQt5.QtCore import Qt

from helpers import *


class Square(QWidget):
    def __init__(self, color, parent=None):
        super().__init__(parent=parent)
        self.color = color
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Arial", 10))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(self.color)))
        painter.drawRect(self.rect())

    def set_text(self, text):
        self.label.setText(text)

    def resizeEvent(self, event):
        self.label.setGeometry(self.rect())

        label_width = self.label.width()
        label_height = self.label.height()
        square_width = self.width()
        square_height = self.height()

        x = (square_width - label_width) / 2
        y = (square_height - label_height) / 2

        self.label.setGeometry(int(x), int(y), label_width, label_height)


class MazeBot(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Maze Bot')
        self.setFixedWidth(720)

        self.size = None
        self.fileName = None
        self.txtMaze = None
        self.distances = None
        self.path_list = None
        self.start, self.goal = None, None

        """
        Create buttons and add them to the layout
        """
        hbox = QHBoxLayout()
        openTextFileButton = QPushButton('Open Text File')
        startButton = QPushButton('Start')

        hbox.addWidget(openTextFileButton)
        hbox.addWidget(startButton)

        openTextFileButton.clicked.connect(self.openFileNameDialog)
        startButton.clicked.connect(self.startFind)

        """
        Create the layout and add the buttons
        """
        self.vbox = QVBoxLayout()
        self.vbox.addLayout(hbox)
        self.setLayout(self.vbox)

        # Set minimum size of squares
        size = min(self.width(), self.height()) - 50
        for square in self.findChildren(Square):
            square.setMinimumSize(size // self.size, size // self.size)

    def resizeEvent(self, event):
        # Update minimum size of squares on resize
        size = min(self.width(), self.height()) - 50

        for square in self.findChildren(Square):
            square.setMinimumSize(size // self.size, size // self.size)

        self.update()

    """
    Create a grid of squares for the maze
    """

    def createGrid(self):
        grid = QGridLayout()
        grid.setSpacing(0)

        for i in range(self.size):
            for j in range(self.size):
                square = None
                if self.distances[i][j] == -2:
                    square = Square('black', self)
                elif self.goal[0] == i and self.goal[1] == j:
                    square = Square('red', self)
                elif self.start[0] == i and self.start[1] == j:
                    square = Square('green', self)
                else:
                    square = Square('white', self)

                square.setObjectName(f'square{i * self.size + j}')
                grid.addWidget(square, i, j)

        self.vbox.addLayout(grid)

    """
    Update the colors of the optimal path
    """

    def update_colors(self):
        for coord in self.path_list:
            i, j = coord

            if self.goal[0] == i and self.goal[1] == j:
                pass
            elif self.start[0] == i and self.start[1] == j:
                pass
            else:
                square = self.findChild(Square, f'square{i * self.size + j}')
                square.color = 'yellow'
                square.update()

    """
    Add the distances of each square from the goal
    """

    def addDistancesText(self):
        for i in range(self.size):
            for j in range(self.size):
                square = self.findChild(Square, f'square{i * self.size + j}')
                square.set_text(str(self.distances[i][j]))

    '''
    Button functions here
    '''

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "Text Files(*.txt)",
                                                  options=options)

        if fileName:
            if self.vbox.count() > 1:
                self.vbox.layout().removeItem(self.vbox.itemAt(1))

            self.size, self.txtMaze = read_maze(fileName)
            self.start, self.goal, self.distances = start_goal_distances(self.txtMaze)
            self.distances = flood_fill(self.txtMaze, self.goal, self.distances)
            self.createGrid()
            self.addDistancesText()

    """
    Start the path finding algorithm
    """

    def startFind(self):
        self.path_list = find_path(self.txtMaze, self.start, self.goal)
        self.update_colors()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mazeBot = MazeBot()
    mazeBot.show()
    sys.exit(app.exec_())
