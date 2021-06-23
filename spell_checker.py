class WordDistance(object):
    def __init__(self, ins_cost, del_cost, sub_cost):
        self.ins_cost = ins_cost
        self.del_cost = del_cost
        self.sub_cost = sub_cost

    def find_distance(self, check_s, s):
        if s == " ":
            return len(check_s) * self.del_cost

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

    def generate_from_file(self, filename, word_distance):
        with open(filename) as f:
            for line in f:
                self.insert(line.strip().lower(), word_distance)

    def generate_from_list(self, list_word, word_distance):
        for word in list_word:
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
# wd = WordDistance(ins_cost=1, del_cost=1, sub_cost=1)
#
# bk_tree = BKNode(" ")
# bk_tree.generate_from_file(filename='5k-words.txt', word_distance=wd)
#
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