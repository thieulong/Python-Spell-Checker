from tqdm import tqdm
import codecs


class WordDistance(object):

    def decoder_str(self, str):
        return str

    def ch_distance(self, ch1, ch2):
        if ch1 == ch2:
            return 0
        return 1

    def find_distance(self, check_s, s):
        if not check_s.strip():
            return sum([self.ch_distance(ch, '') for ch in s])
        if not s.strip():
            return sum([self.ch_distance(ch, '') for ch in check_s])

        check_s, s = self.decoder_str(check_s), self.decoder_str(s)

        dp = [[0 for _ in range(len(check_s) + 1)] for _ in range(len(s) + 1)]
        for j in range(len(check_s) + 1):
            for i in range(len(s) + 1):
                ins_to_s_cost = self.ch_distance(s[i - 1], "")
                ins_to_check_s_cost = self.ch_distance(check_s[j - 1], "")

                if i == 0 and j == 0:
                    continue
                if i == 0:
                    dp[i][j] = dp[i][j - 1] + ins_to_check_s_cost
                    continue
                if j == 0:
                    dp[i][j] = dp[i][j - 1] + ins_to_s_cost
                    continue

                sub_cost = self.ch_distance(check_s[j - 1], s[i - 1])
                dp[i][j] = min(dp[i - 1][j] + ins_to_s_cost, dp[i][j - 1] + ins_to_check_s_cost,
                               dp[i - 1][j - 1] + sub_cost)
        return dp[-1][-1]


class EnglishWordDistance(WordDistance):

    def find_distance(self, check_s, s):
        return super().find_distance(check_s, s)


class VietnameseWordDistance(WordDistance):
    def __init__(self):
        self.character_decoder_dict = {
            'a': 'a  ', 'á': 'a s', 'à': 'a f', 'ả': 'a r', 'ã': 'a x', 'ạ': 'a j',
            'ă': 'aw ', 'ắ': 'aws', 'ằ': 'awf', 'ẳ': 'awr', 'ẵ': 'awx', 'ạ': 'awj',
            'â': 'aa ', 'ấ': 'aas', 'ầ': 'aaf', 'ẩ': 'aar', 'ẫ': 'aax', 'ậ': 'aaj',
            'e': 'e  ', 'é': 'e s', 'è': 'e f', 'ẻ': 'e r', 'ẽ': 'e x', 'ẹ': 'e j',
            'ê': 'ee ', 'ế': 'ees', 'ề': 'eef', 'ể': 'eer', 'ễ': 'eex', 'ệ': 'eej',
            'i': 'i  ', 'í': 'i s', 'ì': 'i f', 'ỉ': 'i r', 'ĩ': 'i x', 'ị': 'i j',
            'o': 'o  ', 'ó': 'o s', 'ò': 'o f', 'ỏ': 'o r', 'õ': 'o x', 'ọ': 'o j',
            'ô': 'oo ', 'ố': 'oos', 'ồ': 'oof', 'ổ': 'oor', 'ỗ': 'oox', 'ộ': 'ooj',
            'ơ': 'ow ', 'ớ': 'ows', 'ờ': 'owf', 'ở': 'owr', 'ỡ': 'owx', 'ợ': 'owj',
            'u': 'u  ', 'ú': 'u s', 'ù': 'u f', 'ủ': 'u r', 'ũ': 'u x', 'ụ': 'u j',
            'ư': 'uw ', 'ứ': 'uws', 'ừ': 'uwf', 'ử': 'uwr', 'ữ': 'uwx', 'ự': 'uwj',
            'y': 'y  ', 'ý': 'y s', 'ỳ': 'y f', 'ỷ': 'y r', 'ỹ': 'y x', 'ỵ': 'u j',
            'd': 'd  ', 'đ': 'dd ',
        }

        self.consonant = {
            1 : ['b', 'c', 'd', 'đ', 'g', 'h', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'x'],
            2 : ['ch', 'gh', 'kh', 'nh', 'ng', 'ph', 'th', 'tr', ]
        }

    def decoder_ch(self, character):
        if character not in self.character_decoder_dict:
            return [character, ' ', ' ']
        return list(self.character_decoder_dict[character])

    def decoder_word(self, word):
        if word[:2] in self.consonant[2]:
            return [word[:2]] + list(word[2:])
        return word

    def decoder_str(self, str):
        words = str.split(" ")
        tmp = []
        for word in words:
            for ch in self.decoder_word(word):
                tmp.append(ch)
            tmp.append(" ")
        return tmp[:-1]

    def ch_distance(self, ch1, ch2):
        if ch1 == ch2:
            return 0
        if len(ch1) == 2 and len(ch2) == 2:
            if (ch1 == 'ch' and ch2 == 'tr') or (ch1 == 'tr' and ch2 == 'ch'):
                return 0.5
            return 1
        if len(ch1) == 2:
            if ch2 and ch2 in ch1:
                return 0.5
        if len(ch2) == 2:
            if ch1 and ch1 in ch2:
                return 0.5

        tmp = 0
        dec1, dec2 = self.decoder_ch(ch1), self.decoder_ch(ch2)
        if dec1[0] != dec2[0]:
            tmp += 1
        if dec1[1] != dec2[1]:
            tmp += 0.5
        if dec1[2] != dec2[2]:
            tmp += 0.5
        return tmp


class BKNode(object):
    def __init__(self, word):
        self.word = word
        self.parent = None
        self.distance_to_parent = 0
        self.dic_child = {}

    def insert(self, new_word, word_distance):
        # # Khu de quy
        # if not self.word:
        #     self.word = new_word
        #     return
        # cur_node = self
        # while cur_node:
        #     distance = word_distance.find_distance(new_word, cur_node.word)
        #     if distance == 0:
        #         return
        #     if distance not in cur_node.dic_child:
        #         new_node = BKNode(new_word)
        #         new_node.parent = cur_node
        #         new_node.distance_to_parent = distance
        #         cur_node.dic_child[distance] = new_node
        #     else:
        #         child_node = cur_node.dic_child[distance]
        #         cur_node = child_node

        # De quy
        if self.word:
            distance = word_distance.find_distance(new_word, self.word)
            if distance == 0:
                return
            if distance not in self.dic_child:
                new_node = BKNode(new_word)
                new_node.parent = self
                new_node.distance_to_parent = distance
                self.dic_child[distance] = new_node
            else:
                child_node = self.dic_child[distance]
                child_node.insert(new_word, word_distance)
        else:
            self.word = new_word

    def generate_from_file(self, filename, word_distance, unicode):
        if not unicode:
            with open(filename) as f:
                for line in tqdm(f):
                    self.insert(line.strip().lower(), word_distance)
            return

        with codecs.open(filename, encoding='utf-8') as f:
            for line in tqdm(f):
                self.insert(line.strip().lower(), word_distance)

    def generate_from_list(self, list_word, word_distance):
        for word in tqdm(list_word):
            self.insert(word, word_distance)

    def __print_tree(self, block):
        print("  "*block + self.word)
        for child in self.dic_child.values():
            child.__print_tree(block + 1)

    def print_tree(self):
        self.__print_tree(0)

    def check(self, check_word, word_distance, d_max):
        return_dict = {}
        if not self:
            return
        S = [self]
        while S:
            cur_node = S.pop()
            du = word_distance.find_distance(check_word, cur_node.word)
            if du <= d_max and cur_node.parent:
                if du not in return_dict:
                    return_dict[du] = [cur_node.word]
                else:
                    return_dict[du].append(cur_node.word)
            for child_distance in cur_node.dic_child:
                if abs(child_distance - du) <= d_max:
                    S.append(cur_node.dic_child[child_distance])
        return return_dict

    def get_suggestions(self, check_word, N_pivot, word_distance, no_suggestions):
        count, suggestions = 0, []
        return_dict = self.check(check_word, word_distance, N_pivot)

        for index in sorted(list(return_dict)):
            if count >= no_suggestions:
                break
            for w in return_dict[index]:
                suggestions.append(w)
                count += 1
                if count >= no_suggestions:
                    break
        return suggestions


# import time
# wd = VietnameseWordDistance()
#
#
# bk_tree = BKNode(" ")
# bk_tree.generate_from_file(filename='word/vie/Viet22K.txt', word_distance=wd, unicode=True)
# # bk_tree.print_tree()
#
# count = 0
# check_w = 'a'
# while check_w:
#     check_w = input("Enter a word: ").lower()
#     N = 0.5 * ((len(check_w) + 3) // 4) + 1
#
#     pTime = time.time()
#     suggestions_list = bk_tree.get_suggestions(check_w, N, wd, no_suggestions=10)
#     for num in range(len(suggestions_list)):
#         print(f'{num + 1} -- {suggestions_list[num]}')
#     cTime = time.time()
#     print(f'Time for calculations: {int(1000*(cTime - pTime))} ms, number of calculations {count}')
#     count = 0
#
#     print()
#     print()