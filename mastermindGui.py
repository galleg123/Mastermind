import sys
import random
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout,QHBoxLayout,QLabel, QPushButton
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPainter, QColor, QMouseEvent


# Draw up a circle
class CircleWidget(QWidget):
    def __init__(self, color=QColor(255,255,255)):
        super().__init__()
        self.color = color
        self.setFixedSize(15,15)

    def set_color(self, color):
        self.color = color
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self.color)
        painter.drawEllipse(0,0,self.width(), self.height())
        painter.end()


# Circle childclass that makes a circle for the submittion row with special mousePressEvent
class SubmitCircleWidget(CircleWidget):
    def __init__(self, color=QColor(255,255,255)):
        super().__init__(color)
    
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.set_color(QColor(255,255,255))

# Circle childclass that makes a circle for one of the selectable colors, with special mousePressEvent
class SelectionCircleWidget(CircleWidget):
    colorSelected = Signal(QColor)
    def __init__(self, color=QColor(255,255,255)):
        super().__init__(color)
    
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.colorSelected.emit(self.color)

    
# Class that initiates 4 circles that it can set the colors for. These are the history of submitted guesses
class RowWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.circles = [CircleWidget() for _ in range(4)]
        for circle in self.circles:
            self.layout.addWidget(circle)
        self.text = QLabel("", alignment=Qt.AlignCenter)
        self.layout.addWidget(self.text)
        self.setLayout(self.layout)
        
    def set_row_colors(self, colors):
        for index, circle in enumerate(self.circles):
            circle.set_color(colors[index])
    
    def set_row_text(self,correct_color, correct_placement):
        self.text.setText(f'Correct Colors: {correct_color}\nCorrect Placement: {correct_placement}')

# Class for a Row with the currently selected colors that are ready to be submitted
class SubmitRowWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.circles = [SubmitCircleWidget() for _ in range(4)]
        for circle in self.circles:
            self.layout.addWidget(circle)
        self.setLayout(self.layout)
    
    def set_circle_color(self, color):
        for circle in self.circles:
            if circle.color == QColor(255,255,255):
                circle.set_color(color)
                break

# Row with the Color selection palette, these can be clicked and will be added to the submit row.
class ColorSelectionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()

        self.colorOptions = [QColor(255,0,0), QColor(0,255,0),QColor(0,0,255), QColor(255,255,0), QColor(255,165,0), QColor(255,0,255)]

        self.circles = [SelectionCircleWidget(x) for x in self.colorOptions]
        for circle in self.circles:
            self.layout.addWidget(circle)

        self.setLayout(self.layout)

# Widget containing the currently selected colors row, aswell as the colors that can be selected. And the button to submit.
class SubmitWidget(QWidget):
    submitGuess = Signal(list)
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.submit_layout = QHBoxLayout()
        self.selection_row = QHBoxLayout()
        
        self.colorOptions = [QColor(255,0,0), QColor(0,255,0),QColor(0,0,255), QColor(255,255,0), QColor(255,165,0), QColor(255,0,255)]
        self.submit_row = SubmitRowWidget()

        self.selectionCircles = [SelectionCircleWidget(x) for x in self.colorOptions]
        for circle in self.selectionCircles:
            self.selection_row.addWidget(circle)
            circle.colorSelected.connect(self.submit_row.set_circle_color)

        self.submit_layout.addWidget(self.submit_row)
        self.submit_button = QPushButton("Submit guess")
        self.submit_layout.addWidget(self.submit_button)
        self.submit_button.clicked.connect(self.submit_guess)
        self.layout.addLayout(self.submit_layout)
        self.layout.addLayout(self.selection_row)


        self.setLayout(self.layout)

    def submit_guess(self):
        guess = []
        for circle in self.submit_row.circles:
            if not circle.color == QColor(255,255,255):
                guess.append(circle.color)
            else:
                return
        self.submitGuess.emit(guess)
        for circle in self.submit_row.circles:
            circle.set_color(QColor(255,255,255))




class MastermindWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.colorOptions = [QColor(255,0,0), QColor(0,255,0),QColor(0,0,255), QColor(255,255,0), QColor(255,165,0), QColor(255,0,255)]
        self.guesses = 0
        self.maxGuesses = 12
        self.secretSequence = self.generateSequence()
        self.correctAnswer = False

        self.setWindowTitle("Mastermind")

        self.main_layout = QVBoxLayout()

        self.text = QLabel("", alignment=Qt.AlignCenter)

        self.main_layout.addWidget(self.text)
        self.rows = [RowWidget() for _ in range(12)]
        for row in self.rows:
            self.main_layout.addWidget(row)

        self.submit = SubmitWidget()
        self.submit.submitGuess.connect(self.color_row)

        self.main_layout.addWidget(self.submit)


        self.setLayout(self.main_layout)

    def generateSequence(self):

        secret = random.choices(self.colorOptions, k=4)

        return secret
    
    def checkColors(self, guess):
        colorChecker = {"R":0, 
                        "G":0, 
                        "B":0, 
                        "Y":0, 
                        "O":0, 
                        "P":0}

        # Subtract one from each dictionary entry for each appearence in the secret sequence
        for color in self.secretSequence:
            if color == QColor(255,0,0):
                colorChecker["R"] -=1
            elif color == QColor(0,255,0):
                colorChecker["G"] -=1
            elif color == QColor(0,0,255):
                colorChecker["B"] -=1
            elif color == QColor(255,255,0):
                colorChecker["Y"] -=1
            elif color == QColor(255,165,0):
                colorChecker["O"] -=1
            elif color == QColor(255,0,255):
                colorChecker["P"] -=1
            
        
        # Adds 1 to the dictionary colors that has been guessed(where correct guesses will move towards 0 and wrong guesses away from 0)
        for color in guess:
            if color == QColor(255,0,0):
                colorChecker["R"] +=1
            elif color == QColor(0,255,0):
                colorChecker["G"] +=1
            elif color == QColor(0,0,255):
                colorChecker["B"] +=1
            elif color == QColor(255,255,0):
                colorChecker["Y"] +=1
            elif color == QColor(255,165,0):
                colorChecker["O"] +=1
            elif color == QColor(255,0,255):
                colorChecker["P"] +=1
            

        # Sums the values stored in colorChecker.
        colorSum = 0
        for color in colorChecker:
            colorSum += abs(colorChecker[color])

        # The amount of correct colors will be 4 (max amount) with the colorSum divided by two subtracted (Division by 2 is due to each wrong having both a color not being set to 0 and a color being removed from 0)
        correctColors = 4 - (colorSum / 2)

        return correctColors

    def checkPlacement(self, guess):
        placementSum = 0

        for i in range(len(guess)):
            placementSum += self.secretSequence[i] == guess[i]

        return placementSum
    

    def color_row(self, colors):
        # Change the color of row
        self.rows[self.guesses].set_row_colors(colors)
        
        correctColors = self.checkColors(colors)
        correctPlacement = self.checkPlacement(colors)

        self.rows[self.guesses].set_row_text(correctColors, correctPlacement)

        if correctPlacement == 4:
            self.text.setText("Congratulation you guessed the sequence")
            

        self.guesses += 1

        if self.guesses == 12:
            self.text.setText("Unfortunately you failed to guess the sequence")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MastermindWindow()
    window.show()
    sys.exit(app.exec())