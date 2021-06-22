def generate_word_list(file):

    with open(file) as f:

        word_list = f.read().splitlines()

    word_list = [w.lower() for w in word_list]

    return word_list


def generate_suggest_dict(word, word_split, word_list, length_limit = 5):

    first_letter = 0
    last_letter = -1

    word_length = len(word)

    suggest = list()

    for e in range(len(word_list)):

        if word_list[e][1:] == word[1:]:

            suggest.append(word_list[e])

    for i in range(len(word_split)):
    
        if i == first_letter:

            for e in range(len(word_list)):

                if word_split[first_letter] == word_list[e][first_letter]:

                    suggest.append(word_list[e])


    for i in range(len(suggest)):

        if len(suggest[i]) < word_length:

                suggest[i] = None

        elif len(suggest[i]) - word_length not in range(length_limit):

                suggest[i] = None


    suggest = list(filter(None, suggest))

    suggest_dict = {key : 0 for key in suggest}

    return suggest_dict


def generate_suggest_points(word, word_split, suggest_dict, number_of_suggestions = 10):

    word_length = len(word)

    first_letter = 0
    last_letter = -1

    for i in range(len(word_split)):
 
        if i > first_letter:

            for key in suggest_dict:

                if len(key) == word_length:

                    if key == word:

                        return key

                    if word_split[i] == key[i]: 

                        suggest_dict[key] += len(key) - i

                elif len(key) > word_length:

                    if key[:word_length] == word:

                        suggest_dict[key] += sum(range(len(key[:word_length]))) + len(key[word_length:])

        
    suggestion_result = {key: value for key, value in sorted(suggest_dict.items(), key=lambda item: item[1], reverse=True)}
    
    top_suggestion = list(suggestion_result)[:number_of_suggestions]

    return top_suggestion


def generate_suggestion(word, suggestions):

    if suggestions == word:

        # print("\nThis word is correctly spelled!\n")

        return 0

    elif len(suggestions) > 1:

        # print("\nSuggestions for: {}\n".format(word))

        # for i in range(len(suggestions)):

            # print("- {i}. {suggest_word}".format(i=i + 1, suggest_word=suggestions[i]))

        return suggestions


# word_list = generate_word_list(file="5k-words.txt")
# print(generate_suggestion(word=word, suggestions=generate_suggest_points(word=word, word_split=word_split, suggest_dict=generate_suggest_dict(word=word, word_split=word_split, word_list=word_list))))
