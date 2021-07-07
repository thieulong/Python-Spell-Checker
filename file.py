from tqdm import tqdm
import codecs

list = []
count = 0
filename = 'word/vie/Viet22K.txt'
with codecs.open(filename, encoding='utf-8') as f:
    for line in tqdm(f):
        word = line.strip().lower()
        count += 1
        if word not in list:
            list.append(word)

print(len(list))
print(count)

