import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel, QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import pyqtSlot
import spell_check

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Spell Checker'
        self.left = 600
        self.top = 200
        self.width = 700
        self.height = 700
        self.initUI()

    
    def initUI(self):
        info = "Python Spell Checker Program".upper()

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.label = QLabel(info, self)
        self.label.setFont(QFont('Times',20))
        self.label.move(120,50)
        self.label.resize(500,50)

        self.correct = QLabel("This word is correctly spelled!", self)
        self.correct.setFont(QFont('Times',15))
        self.correct.move(30,200)
        self.correct.resize(600,50)
        self.correct.setHidden(True)

        self.incorrect = QLabel("Oops! It seems like this word doesn't existed!", self)
        self.incorrect.setFont(QFont('Times',15))
        self.incorrect.move(30,200)
        self.incorrect.resize(600,50)
        self.incorrect.setHidden(True)
    
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 150)
        self.textbox.resize(500,40)
        
        self.button = QPushButton('Check', self)
        self.button.move(550,150)
        self.button.resize(100,40)
        
        self.button.clicked.connect(self.show_results)
        self.show()
    

    def show_results(self):
        textboxValue = self.textbox.text()
        word = textboxValue.lower()
        word_split = list(word)
        word_list = spell_check.generate_word_list(file="5k-words.txt")
        suggestions = spell_check.generate_suggestion(word=word, suggestions=spell_check.generate_suggest_points(word=word, word_split=word_split, suggest_dict=spell_check.generate_suggest_dict(word=word, word_split=word_split, word_list=word_list)))
        
        if suggestions == 0:
            self.incorrect.setHidden(True)
            self.correct.setHidden(False)
            
        else:
            self.correct.setHidden(True)
            self.incorrect.setHidden(False)
            

        self.textbox.setText("")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())