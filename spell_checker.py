class WordDistance(object):
    def __init__(self, ins_cost, del_cost, sub_cost):
        self.ins_cost = ins_cost
        self.del_cost = del_cost
        self.sub_cost = sub_cost

    def find_distance(self, check_s, s):
        dp = [[0 for _ in range(len(check_s) + 1)] for _ in range(len(s) + 1)]
        for j in range(len(check_s) + 1):
            for i in range(len(s) + 1):
                if i == 0:
                    dp[i][j] = j * self.ins_cost
                    continue
                if j == 0:
                    dp[i][j] = i * self.del_cost
                    continue
                sub_cost = self.sub_cost
                if check_s[j - 1] == s[i - 1]:
                    sub_cost = 0
                dp[i][j] = min(dp[i-1][j] + self.ins_cost, dp[i][j-1] + self.del_cost, dp[i-1][j-1] + sub_cost)
        return dp[-1][-1]


class BKNode(object):
    def __init__(self, word):
        self.word = word
        self.parent = None
        self.distance_to_parent = 0
        self.dic_child = {}

    def insert(self, new_word, word_distance):
        if self.word:
            distance = word_distance.find_distance(self.word, new_word)
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

    def generate_from_file(self, filename, word_distance):
        with open(filename) as f:
            for line in f:
                self.insert(line.strip().lower(), word_distance)

    def generate_from_list(self, list_word, word_distance):
        for word in list_word:
            self.insert(word, word_distance)

    def print_tree(self, block):
        print("  "*block + self.word)
        for child in self.dic_child.values():
            child.print_tree(block + 1)

    def check(self, check_word, N_pivot, word_distance, lower, upper, result_dic):
        if self.word:
            distance = word_distance.find_distance(check_word, self.word)

            if distance <= N_pivot:
                if distance not in result_dic:
                    result_dic[distance] = [self.word]
                else:
                    result_dic[distance].append(self.word)
                for child_distance in self.dic_child:
                    if lower <= child_distance <= upper:
                        self.dic_child[child_distance].check(check_word, N_pivot, word_distance, distance - N_pivot, distance + N_pivot, result_dic)
        return result_dic

    def get_suggestions(self, check_word, N_pivot, word_distance, no_suggestions):
        count, suggestions = 0, []
        return_dic = self.check(check_word, N_pivot, word_distance, 0, 20, {})

        for index in sorted(list(return_dic)):
            if count >= no_suggestions:
                break
            for w in return_dic[index]:
                suggestions.append(w)
                count += 1
                if count >= no_suggestions:
                    break
        return suggestions


def generate_word_list(file):
    with open(file) as f:
        word_list = f.read().splitlines()
    word_list = [w.lower() for w in word_list]
    return word_list

# Create WordDistance object
# wd = WordDistance(ins_cost=2, del_cost=2, sub_cost=1)
#
#
# word_list = generate_word_list('5k-words.txt')
# print(len(word_list))
#
# word_dict = {}
# for i in range(1, 15):
#     word_dict[i] = [word for word in word_list if len(word) == i]
#
# k = 2
# bk_tree_dict = {}
# for i in range(1, 15):
#     bk_tree = BKNode(word_dict[i][0])
#     for j in range(max(i - k, 1), min(i + k, 15)):
#         bk_tree.generate_from_list(word_dict[j], wd)
#     bk_tree_dict[i] = bk_tree
#
#
# import time
#
# check_w = 'a'
# while check_w:
#     check_w = input("Enter a word: ").lower()
#     N = len(check_w) + k
#
#     pTime = time.time()
#     l = min(len(check_w), 14)
#     suggestions_list = bk_tree_dict[l].get_suggestions(check_w, N, wd, no_suggestions=10)
#     for num in range(len(suggestions_list)):
#         print(f'{num + 1} -- {suggestions_list[num]}')
#     cTime = time.time()
#     print(f'Time for calculations: {int(1000*(cTime - pTime))} ms')
#
#     print()
#     print()

