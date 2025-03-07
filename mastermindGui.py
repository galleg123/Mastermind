import sys
import random
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout,QHBoxLayout,QLabel, QPushButton
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPainter, QColor, QMouseEvent
from module.save_score import SaveScore


# Draw up a circle
class CircleWidget(QWidget):
    def __init__(self, color=QColor(255,255,255)):
        super().__init__()
        self.color = color
        self.setFixedSize(15,15)

    def set_color(self, color):
        self.color = color
        self.update()


    # Used for drawing the circles
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
    # Signal is used to trigger methods in other classes
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
        self.text = QLabel("", alignment=Qt.AlignLeft)
        self.layout.addWidget(self.text)
        self.setLayout(self.layout)
    

    def set_row_colors(self, colors):
        for index, circle in enumerate(self.circles):
            circle.set_color(colors[index])
    
    # Shows the information about the guess
    def set_row_text(self,correct_color, correct_placement):
        self.text.setText(f'Correct Color Wrong Placement: {correct_color} | Correct Color and Placement: {correct_placement}')

    def reset_row_text(self):
        self.text.setText("")

# Class for a Row with the currently selected colors that are ready to be submitted
class SubmitRowWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.circles = [SubmitCircleWidget() for _ in range(4)]
        for circle in self.circles:
            self.layout.addWidget(circle)
        self.setLayout(self.layout)
    
    # Function used for setting the colors, takes the first circle that is white and colors that one
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


        # Creates the circles used for selecting colors by iterating through the colors in the colorOptions variable
        self.selectionCircles = [SelectionCircleWidget(x) for x in self.colorOptions]
        for circle in self.selectionCircles:
            self.selection_row.addWidget(circle)
            circle.colorSelected.connect(self.submit_row.set_circle_color)

        self.submit_layout.addWidget(self.submit_row)
        self.submit_button = QPushButton("Submit guess")
        self.submit_layout.addWidget(self.submit_button)

        # Connects the button to submit guess method
        self.submit_button.clicked.connect(self.submit_guess)


        self.layout.addLayout(self.submit_layout)
        self.layout.addLayout(self.selection_row)
        self.setLayout(self.layout)

    # Submits the guess
    def submit_guess(self):
        guess = []

        # Makes sure there is no unset circles in the guess
        for circle in self.submit_row.circles:
            if not circle.color == QColor(255,255,255):
                guess.append(circle.color)
            else:
                return
        
        # Sends out the guess through the submitGuess signal and clears the colors
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
        

        self.setWindowTitle("Mastermind")

        self.main_layout = QVBoxLayout()

        # Text box that will be used later to display the outcome of the game.
        self.text = QLabel("", alignment=Qt.AlignCenter)
        self.main_layout.addWidget(self.text)

        # Adds i the rows used for guess history
        self.rows = [RowWidget() for _ in range(12)]
        for row in self.rows:
            self.main_layout.addWidget(row)


        # Adds in the submit widget section, aswell as binds the signal from the submit widget to the color_row method
        self.submit = SubmitWidget()
        self.submit.submitGuess.connect(self.color_row)
        self.main_layout.addWidget(self.submit)


        # Restart button
        self.restart_button = QPushButton("Restart Game")
        self.restart_button.clicked.connect(self.restart_game)
        self.main_layout.addWidget(self.restart_button)
        self.restart_button.setVisible(False)



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
        correctColors = int( 4 - (colorSum / 2))

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

        self.rows[self.guesses].set_row_text(correctColors-correctPlacement, correctPlacement)

        self.guesses += 1
        if correctPlacement == 4:
            self.text.setText("Congratulation you guessed the sequence")
            self.submit.setVisible(False)
            self.restart_button.setVisible(True)
            score_submit = SaveScore(self.guesses, True)
            score_submit.exec()

            


        if self.guesses == 12 and correctPlacement != 4:
            self.text.setText("Unfortunately you failed to guess the sequence")
            self.submit.setVisible(False)
            self.restart_button.setVisible(True)
            score_submit = SaveScore(self.guesses, False)
            score_submit.exec()
    
    def restart_game(self):
        self.guesses = 0
        self.secretSequence = self.generateSequence()

        # Reset the guess history and other widgets
        for row in self.rows:
            row.set_row_colors([QColor(255,255,255)]*4)
            row.reset_row_text()
        
        for circle in self.submit.submit_row.circles:
            circle.set_color(QColor(255,255,255))

        self.submit.setVisible(True)
        self.submit.adjustSize()
        self.submit.updateGeometry()
        self.restart_button.setVisible(False)
        self.text.setText("")
        self.adjustSize()
        self.updateGeometry()
        




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MastermindWindow()
    window.resize(400,700)
    window.show()
    sys.exit(app.exec())
