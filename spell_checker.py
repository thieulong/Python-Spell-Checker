from tqdm import tqdm
import codecs


class WordDistance(object):
    pass


class EnglishWordDistance(WordDistance):

    def decoder_ch(self, character):
        return character

    def decoder_str(self, str):
        return str

    def find_distance(self, check_s, s):
        if s == " ":
            return len(check_s)

        dp = [[0 for _ in range(len(check_s) + 1)] for _ in range(len(s) + 1)]
        for j in range(len(check_s) + 1):
            for i in range(len(s) + 1):
                if i == 0:
                    dp[i][j] = j
                    continue
                if j == 0:
                    dp[i][j] = i
                    continue
                sub_cost = 1
                if check_s[j - 1] == s[i - 1]:
                    sub_cost = 0
                dp[i][j] = min(dp[i-1][j] + 1, dp[i][j-1] + 1, dp[i-1][j-1] + sub_cost)
        return dp[-1][-1]


class VietnameseWordDistance(WordDistance):
    def __init__(self):

        self.alphabet_character = 'abcdefghijklmnopqrstuvwxyz1234567890 `~!@#$%^&*()+=-_/.,<>?;:[]{}|'
        self.lv1_character = 'ăâêôơưđ'

        self.eng_vowels_dict = {
            'a' : 'aăâ',
            'e' : 'eê',
            'i' : 'i',
            'o' : 'oôơ',
            'u' : 'uư',
            'd' : 'dđ'
        }

        self.vie_vowels_dict = {
            'a' : 'aáàảãạ',
            'ă' : 'ăắằẳẵặ',
            'â' : 'âấầẩẫậ',
            'e' : 'eéèẻẽẹ',
            'ê' : 'êếềểễệ',
            'i' : 'iíìỉĩị',
            'o' : 'oóòỏõọ',
            'ô' : 'ôốồổỗộ',
            'ơ' : 'ơớờởỡợ',
            'u' : 'uúùủũụ',
            'ư' : 'ưứừửữự',
            'd' : 'd',
            'đ' : 'đ'
        }

        self.sign_dict = {
            0 : 'aăâbcdđeêfghijklmnoôơpqrstuưvxyz1234567890 `~!@#$%^&*()+=-_.,<>?;:[]{}|/',
            1 : 'áắấéếíóốớúứ',
            2 : 'àằầèềìòồờùừ',
            3 : 'ảẳẩẻểỉỏổởủử',
            4 : 'ãẵẫẽễĩõỗỡũữ',
            5 : 'ạặậẹệịọộợụự',
        }

    def get_lv(self, character):
        if not self.get_vie_vowel(character):
            return 2
        if not character \
                or character in self.alphabet_character \
                or self.get_vie_vowel(character) in self.alphabet_character:
            return 0
        if self.get_vie_vowel(character) in self.lv1_character:
            return 1
        return 2

    def get_vie_vowel(self, character):
        for vie_vowel in self.vie_vowels_dict:
            if character in self.vie_vowels_dict[vie_vowel]:
                return vie_vowel
        return None

    def get_eng_vowel(self, character):
        for eng_vowel in self.eng_vowels_dict:
            if character in self.eng_vowels_dict[eng_vowel]:
                return eng_vowel
        return None

    def get_sign(self, character):
        for sign_num in self.sign_dict:
            if character in self.sign_dict[sign_num]:
                return sign_num
        return 0

    def ch_distance(self, ch1, ch2):
        if ch1 == ch2:
            return 0
        if ch1 in self.alphabet_character and ch2 in self.alphabet_character:
            return 1

        if not ch2 or ch2 == " ":
            if self.get_lv(ch1) >= 1:
                if self.get_sign(ch1) != 0:
                    return 2
                return 1.5
            if self.get_sign(ch1) != 0:
                return 1.5
            return 1


        vie_ch1, vie_ch2 = self.get_vie_vowel(ch1), self.get_vie_vowel(ch2)
        eng_ch1, eng_ch2 = None, None
        if vie_ch1:
            eng_ch1 = self.get_eng_vowel(vie_ch1)
        if vie_ch2:
            eng_ch2 = self.get_eng_vowel(vie_ch2)
        sign_ch1, sign_ch2 = self.get_sign(ch1), self.get_sign(ch2)
        tmp = 0
        if eng_ch1 == eng_ch2:
            if vie_ch1 != vie_ch2:
                tmp += 0.5
        else:
            tmp += 1
            if max(self.get_lv(ch1), self.get_lv(ch2)) >= 1:
                tmp += 0.5

        if sign_ch1 != sign_ch2:
            tmp += 0.5
        return tmp

    def decoder_ch(self, character):
        return character

    def decoder_str(self, str):
        return str

    def find_distance(self, check_s, s):
        if s == " ":
            return len(check_s)

        dp = [[0 for _ in range(len(check_s) + 1)] for _ in range(len(s) + 1)]
        for j in range(len(check_s) + 1):
            for i in range(len(s) + 1):
                if i == 0 and j == 0:
                    continue
                if i == 0:
                    dp[i][j] = dp[i][j-1] + self.ch_distance(check_s[j-1], "")
                    continue
                if j == 0:
                    dp[i][j] = dp[i][j-1] + self.ch_distance(s[i-1], "")
                    continue
                ins_to_s_cost, ins_to_check_s_cost = self.ch_distance(s[i-1], ""), self.ch_distance(check_s[j-1], "")

                sub_cost = self.ch_distance(check_s[j-1], s[i-1])
                dp[i][j] = min(dp[i - 1][j] + ins_to_s_cost, dp[i][j - 1] + ins_to_check_s_cost, dp[i - 1][j - 1] + sub_cost)
        return dp[-1][-1]


class VietnameseWordDistance2(WordDistance):

    def __init__(self):
        self.character_decoder_dict = {
            'a' : 'a', 'á' : 'as', 'à' : 'af', 'ả' : 'ar', 'ã' : 'ax', 'ạ' : 'aj',
            'ă' : 'aw', 'ắ' : 'aws', 'ằ' : 'awf', 'ẳ' : 'awr', 'ẵ' : 'awx', 'ạ' : 'awj',
            'â' : 'aa', 'ấ' : 'aas', 'ầ' : 'aaf', 'ẩ' : 'aar', 'ẫ' : 'aax', 'ậ' : 'aaj',
            'e' : 'e', 'é': 'es', 'è': 'ef', 'ẻ': 'er', 'ẽ': 'ex', 'ẹ': 'ej',
            'ê' : 'ee', 'ế' : 'ees', 'ề' : 'eef', 'ể' : 'eer', 'ễ' : 'eex', 'ệ' : 'eej',
            'i' : 'i', 'í' : 'is', 'ì' : 'if', 'ỉ' : 'ir', 'ĩ' : 'ix', 'ị' : 'ij',
            'o' : 'o', 'ó': 'os', 'ò': 'of', 'ỏ': 'or', 'õ': 'ox', 'ọ': 'oj',
            'ô' : 'oo', 'ố': 'oos', 'ồ': 'oof', 'ổ': 'oor', 'ỗ': 'oox', 'ộ': 'ooj',
            'ơ' : 'ow', 'ớ': 'ows', 'ờ': 'owf', 'ở': 'owr', 'ỡ': 'owx', 'ợ': 'owj',
            'u' : 'u', 'ú': 'us', 'ù': 'uf', 'ủ': 'ur', 'ũ': 'ux', 'ụ': 'uj',
            'ư' : 'uw', 'ứ': 'uws', 'ừ': 'uwf', 'ử': 'uwr', 'ữ': 'uwx', 'ự': 'uwj',
            'd' : 'd', 'đ' : 'dd'
        }

    def decoder_ch(self, character):
        if character not in self.character_decoder_dict:
            return character
        return self.character_decoder_dict[character]

    def decoder_str(self, str):
        return "".join([self.decoder_ch(ch) for ch in str])

    def find_distance(self, check_s, s):
        check_s, s = self.decoder_str(check_s), self.decoder_str(s)
        if s == " ":
            return len(check_s)

        dp = [[0 for _ in range(len(check_s) + 1)] for _ in range(len(s) + 1)]
        for j in range(len(check_s) + 1):
            for i in range(len(s) + 1):
                if i == 0:
                    dp[i][j] = j
                    continue
                if j == 0:
                    dp[i][j] = i
                    continue
                sub_cost = 1
                if check_s[j - 1] == s[i - 1]:
                    sub_cost = 0
                dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + sub_cost)
        return dp[-1][-1]


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
            du = word_distance.find_distance(word_distance.decoder_str(check_word), word_distance.decoder_str(cur_node.word))
            if du < d_max and cur_node.parent:
                if du not in return_dict:
                    return_dict[du] = [cur_node.word]
                else:
                    return_dict[du].append(cur_node.word)
            for child_distance in cur_node.dic_child:
                if abs(child_distance - du) < d_max:
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
# wd = VietnameseWordDistance2()
#
#
# bk_tree = BKNode(" ")
# bk_tree.generate_from_file(filename='word/vie/Viet22K.txt', word_distance=wd, unicode=True)
# bk_tree.print_tree()
#
# count = 0
# check_w = 'a'
# while check_w:
#     check_w = input("Enter a word: ").lower()
#     N = (len(check_w) + 3) // 4 + 1
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