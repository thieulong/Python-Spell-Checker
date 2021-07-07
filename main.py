import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel, QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import pyqtSlot
import spell_check
from spell_checker import *

class App(QMainWindow):

    def __init__(self, bk_tree_dict, wd):
        super().__init__()
        self.bk_tree = bk_tree
        self.wd = wd

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
        self.label.move(110,50)
        self.label.resize(700,50)

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

        self.definition = QLabel("", self)
        self.definition.setFont(QFont('Times',15))
        self.definition.move(30,250)
        self.definition.resize(600,50)
        self.definition.setHidden(True)

        self.suggest = QLabel("", self)
        self.suggest.setFont(QFont('Times',15))
        self.suggest.move(50,200)
        self.suggest.resize(1000,500)
        self.suggest.setHidden(True)
    
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 150)
        self.textbox.resize(500,40)
        self.textbox.setPlaceholderText('Enter a word')
        
        self.button = QPushButton('Check', self)
        self.button.move(550,150)
        self.button.resize(100,40)
        
        self.button.clicked.connect(self.show_results)
        self.show()
    

    def show_results(self):
        textboxValue = self.textbox.text()
        word = textboxValue.lower()

        # old
        # word_split = list(word)
        # word_list = spell_check.generate_word_list(file="5k-words.txt")
        # suggestions = spell_check.generate_suggestion(word=word, suggestions=spell_check.generate_suggest_points(word=word, word_split=word_split, suggest_dict=spell_check.generate_suggest_dict(word=word, word_split=word_split, word_list=word_list)))

        # new

        # coef for english word
        # N = (len(word) + 3) // 4

        # coef for vietnamese word
        N = 0.5 * ((len(word) + 2) // 3) + 1

        suggestions = bk_tree.get_suggestions(word, N, wd, no_suggestions=10)

        if not word.strip():
            self.correct.setHidden(True)
            self.incorrect.setHidden(True)
            self.definition.setHidden(True)
            self.suggest.setHidden(True)

        if not suggestions:
            self.correct.setHidden(True)
            self.incorrect.setHidden(False)
            self.definition.setHidden(True)
            self.suggest.setHidden(True)

        elif word == suggestions[0]:
            self.incorrect.setHidden(True)
            self.correct.setHidden(False)
            self.definition.setHidden(True)
            self.suggest.setHidden(True)
            
        elif suggestions != 0:
            for i in range(len(suggestions)):
                suggestions[i] = "{i}. {suggest}".format(i=i+1, suggest=suggestions[i])

            self.correct.setHidden(True)
            self.incorrect.setHidden(False)
            self.definition.setText("Suggestions for '{}':".format(word))
            self.definition.setHidden(False)
            self.suggest.setText('\n'.join(suggestions))
            self.suggest.setHidden(False)
            

        self.textbox.setText("")


if __name__ == '__main__':
    # Vietnamese
    wd = VietnameseWordDistance()

    bk_tree = BKNode(" ")
    bk_tree.generate_from_file(filename='word/vie/Viet22K.txt', word_distance=wd, unicode=True)

    # # English
    # wd = EnglishWordDistance()
    #
    # bk_tree = BKNode(" ")
    # bk_tree.generate_from_file(filename='word/en/5k-words.txt', word_distance=wd, unicode=False)

    app = QApplication(sys.argv)
    ex = App(bk_tree, wd)
    sys.exit(app.exec_())


# suggestions co the tra ve 1 list rong, nho handle tinh huong nay nha!
