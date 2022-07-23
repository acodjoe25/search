
import sys
from file_io import *
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
nltk_test = PorterStemmer()
STOP_WORDS = set(stopwords.words('english'))

class Querier:
    def __init__(self, is_pr: bool, titles_path: str, docs_path: str, words_path: str):
        self.is_pr = is_pr 
        
        self.ids_to_titles = {}
        read_title_file(titles_path, self.ids_to_titles)
        self.ids_to_rank = {}
        read_docs_file(docs_path, self.ids_to_rank)
        self.words_to_relevance = {}
        read_words_file(words_path, self.words_to_relevance)
        self.ids_to_relevance = {}

        self.run_repl()
    
    def process_relevance(self, input : str):
        if input in self.words_to_relevance:
            for id in self.ids_to_titles:
                if id not in self.words_to_relevance[input]:
                    continue
                if id in self.ids_to_relevance:
                    self.ids_to_relevance[id] = self.ids_to_relevance[id] + self.words_to_relevance[input][id]
                else:
                    self.ids_to_relevance[id] = self.words_to_relevance[input][id]

    def process_query(self, input: str):
        tokenization_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        input_tokens = re.findall(tokenization_regex, input)

        for word in input_tokens:
            if str(word).lower() not in STOP_WORDS:
                self.process_relevance(nltk_test.stem(word))

        # use page rank:
        if self.is_pr:
            page_rank = {}
            for id in self.ids_to_relevance:
                page_rank[id] = (self.ids_to_rank[id] * 2) * self.ids_to_relevance[id] 
            dict = page_rank
        # use relevance:
        else:
            dict = self.ids_to_relevance
            
        sorted_dict = sorted(dict.items(), key = lambda x:x[1], reverse=True)
        sorted_ids = [self.ids_to_titles[x[0]] for x in sorted_dict[:10]]
        sorted_dict.clear()
        self.ids_to_relevance.clear()

        if len(sorted_ids) == 0:
            print("no results")
        else:
            for i, title in enumerate(sorted_ids, start = 1):
                print(i, title)

    def run_repl(self): 
        while True:
            inpt = input(">search:")
            if inpt == ":quit":
                break
            else:
                print(inpt.upper())
                self.process_query(inpt)
        
if __name__ == "__main__":
    if len(sys.argv) == 4:
        Querier(False, *sys.argv[1:])
    elif (len(sys.argv) == 5) and (sys.argv[1] == "--pagerank"):
        Querier(True, *sys.argv[2:])
    else:
        print("wrong number of arguments!")