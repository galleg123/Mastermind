
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QWidget, QVBoxLayout,QLabel,QLineEdit, QPushButton
import json

class SaveScore(QDialog):
    def __init__(self, guesses, succesful):
        super().__init__()

        self.guesses = guesses
        self.succesful = succesful

        self.setWindowTitle("Submit Score")
        self.setGeometry(100,100,200,100)

        self.layout = QVBoxLayout()

        self.label = QLabel("Enter name and click submit")

        self.text_field = QLineEdit(self)


        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.on_submit)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.text_field)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def on_submit(self):
        name = self.text_field.text()

        data = {
            "games": [
                {"name": f'{name}',
                 "guesses": f'{self.guesses}',
                 "succesful": f'{self.succesful}'
                 }
            ]
        }

        file_path = "scores.json"

        try:
            with open(file_path, 'r') as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            existing_data = {}

        if "games" in existing_data:
            existing_data["games"].append(data["games"][0])
        else: 
            existing_data["games"] = data["games"]

        with open(file_path, 'w') as file:
            json.dump(existing_data, file, indent=4)

        self.close()





