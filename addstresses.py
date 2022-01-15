import os
import csv
import time
import re
import PyQt5.QtWidgets as qtw
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from helpers import needs_stress, is_russian, remove_punct, gen_replacement_text, remove_vertical

process = CrawlerProcess(get_project_settings())
baseurl = 'https://' + 'где-ударение.рф/в-слове-'

if os.path.exists('stresses.csv'):
    os.remove('stresses.csv')


class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Stresses")
        self.setLayout(qtw.QVBoxLayout())
        self.label = qtw.QLabel("Enter Russian text in the box below and press the button")
        self.layout().addWidget(self.label)
        self.text_edit = qtw.QTextEdit()
        self.text_edit.setObjectName("text_field")
        self.layout().addWidget(self.text_edit)
        self.button = qtw.QPushButton("Mark stresses")
        self.button.clicked.connect(self.get_stresses)
        self.layout().addWidget(self.button)
        self.show()

    def get_stresses(self):
        self.text_edit.setDisabled(True)
        self.button.setDisabled(True)
        text = self.text_edit.toPlainText()
        text_list = text.split()
        target_url_list = []
        target_word_list = []
        # figure out which words need to be stressed and create a list of URLS
        # to scrape accordingly
        for word in text_list:
            if '|' in word:
                modword = remove_vertical(word)
            else:
                modword = word
            if is_russian(remove_punct(modword)):
                target_word = remove_punct(modword)
                # because examples generated from Reverso Context extractor are
                # separated from their translations by just a vertical bar with
                # no spaces, we need to check for this bar and remove it
                # print(target_word)
                target_word = target_word.lower()
                if needs_stress(target_word):
                    target_url_list.append(baseurl + target_word + '/')
                    target_word_list.append(target_word)
        target_url_list = set(target_url_list)

        process.crawl('stressspider', start_url=target_url_list)
        process.start()

        with open('stresses.csv') as f:
            stressreader = csv.DictReader(f)
            # make a dictionary from the resulting CSV file where the keys are
            # unstressed words and the values are lists of possible stresses
            stress_dict = {}
            for row in stressreader:
                if row['clean'] in stress_dict.keys():
                    stress_dict[row['clean']].append(row['stressed'])
                else:
                    stress_dict[row['clean']] = [row['stressed'], ]
            # make another dictionary where the keys are unstressed words
            # and the values is a string of possible stress options separated by \\
            stress_dict_str = {}
            for word in stress_dict.keys():
                stress_dict_str[word] = gen_replacement_text(stress_dict[word])
            # make a list in which each item is a line from the text input by the user
            line_list = text.split('\n')
            # make a list where every item will be that same line with stresses added
            stressed_line_list = []
            for line in line_list:
                # make a list of words in each line
                word_list = line.split()
                # make a list where each word will be a word from word_list
                # with stress added
                stressed_word_list = []
                for wrd in word_list:
                    cap = wrd[0].isupper()
                    if '|' in wrd:
                        # if the word has a bar, target the first half
                        dict_target = remove_punct(remove_vertical(wrd.lower()))
                    else:
                        dict_target = remove_punct(wrd.lower())
                    if dict_target in stress_dict_str.keys():
                        if cap:
                            stressed_word_list.append(
                                wrd.replace(
                                    remove_punct(dict_target.capitalize()),
                                    stress_dict_str[dict_target].capitalize()
                                    )
                                )
                        else:
                            stressed_word_list.append(
                                wrd.replace(
                                    remove_punct(dict_target),
                                    stress_dict_str[dict_target]
                                )
                            )
                    else:
                        stressed_word_list.append(wrd)
                stressed_line_list.append(" ".join(stressed_word_list))
            stressed_text = '\n'.join(stressed_line_list)
            with open('results.txt', 'w') as r:
                r.write(stressed_text)
            self.text_edit.setText("Text output to results.txt")
            self.label.setText("Stresses retrieved!")
            self.text_edit.setDisabled(False)


app = qtw.QApplication([])
ms = MainWindow()
app.exec_()
