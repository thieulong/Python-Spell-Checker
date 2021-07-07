import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import codecs


filename = 'word/vie/Viet22K.txt'
list_words  = []

with codecs.open(filename, encoding='utf-8') as f:
    for line in f:
        list_words.append(line.strip().lower())

l = []
for words in list_words:
    for word in words.split(' '):
        if word not in l:
            l.append(word)

l2 = [len(w) for w in l]
df = pd.DataFrame(
    data = {
        'Length of word' : l2
    }
)
sns.countplot(data=df, x='Length of word')
plt.show()

