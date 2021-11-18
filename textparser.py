import re

                  
class textparser:
    def __init__(self, text):
        self.word_list = (re.sub("[^\w\s]", "", text)).lower().split()
        mcw_text_file = open("most_common_words.txt")
        self.most_common_word_list = list_of_lists = [(line.strip()) for line in mcw_text_file]

    def print_all_text(self):
        print(self.word_list)

    def word_freq(self, ignore_most_common = False):
        word_freq_map = {}
        for word in self.word_list:
            if ignore_most_common:
                if word not in self.most_common_word_list:
                    if word in word_freq_map:
                        word_freq_map[word] += 1
                    else:
                        word_freq_map[word] = 1
            else:
                if word in word_freq_map:
                    word_freq_map[word] += 1
                else:
                    word_freq_map[word] = 1 
        return word_freq_map

    def most_freq_words(self, num, ignore_most_common = False):
        word_freq_map = self.word_freq(ignore_most_common)
        # sort by frequency
        sorted_tuples = sorted(word_freq_map.items(), key=lambda item: item[1], reverse=True)
        ranked_word_freq_map = {k: v for k, v in sorted_tuples}
        return dict(list(ranked_word_freq_map.items())[0: num]) 
