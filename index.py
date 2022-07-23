
import sys
from file_io import *
import xml.etree.ElementTree as et
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import math
STOP_WORDS = set(stopwords.words('english'))
nltk_test = PorterStemmer()

class Indexer:
    def __init__(self, xml_path: str, titles_path: str, docs_path: str, words_path: str):
        self.id_to_title = {}
        self.link_dict = {} #cleared
        self.word_id_count = {} #cleared
        self.max_count = {} #cleared
        self.relevance_dict = {}
        self.pank_rage = {}
        
        self.parse(xml_path)
        self.relevance()
        self.pageRank()

        write_title_file(titles_path, self.id_to_title)
        write_docs_file(docs_path, self.pank_rage)
        write_words_file(words_path, self.relevance_dict)
        
# parsing the xml --------------------------------------------------------------
    def parse(self, xml_path: str):
        '''
        -- fills the id_to_title dictionary that maps page ids to their 
            titles;
        -- fills the link_dict dictionary that maps page ids to their outgoing 
            links;
        -- fills the word_id_count dictionary that maps words to page ids to 
            how many times the word occurs on that page
        -- fills the max_count dictionary that maps page ids to the frequency 
            of the most occurring word

        parameters:
        xml_path: the xml file path to be parsed
        '''
        all_pages = et.parse(xml_path).getroot().findall("page")
        title_to_id = {}
        for page in all_pages: # for corpus purposes
            title: str = page.find('title').text.strip()
            id: int = int(page.find('id').text)
            self.id_to_title[id] = title
            title_to_id[title] = id

        for page in all_pages:
            title: str = page.find('title').text
            text: str = page.find('text').text
            id: int = int(page.find('id').text)
            self.max_count[id] = 0
            outgoing_links = []

            tokenization_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
            page_tokens = re.findall(tokenization_regex, title + " " + text) 

            for word in page_tokens:
                # check if word is a link
                if word[0:2] == "[[":
                    text = word[2:-2] # text inside brackets
                    if "|" in text: # if link is piped
                        split_index = text.index("|")
                        link_to = text[:split_index] # for page rank
                        text = text[split_index:] # for tfidf
                        if link_to in title_to_id: # if link is in corpus
                            outgoing_links.append(link_to)
                    else:
                        if text in title_to_id: # if link is in corpus
                            outgoing_links.append(text)
                    link_tokens = re.findall(tokenization_regex, text)
                    page_tokens.extend(link_tokens)
                    continue
                # stop and stem:
                if word.lower() not in STOP_WORDS:
                    word = nltk_test.stem(word)

                    # filling in the words to ids to counts dict:
                    if word in self.word_id_count:
                        if id in self.word_id_count[word]:
                            self.word_id_count[word][id] = self.word_id_count[word][id] + 1
                        else:
                            self.word_id_count[word][id] = 1
                    else:
                        id_count = {}
                        id_count[id] = 1
                        self.word_id_count[word] = id_count

                    # checking max word occurence for each page:
                    count = self.word_id_count[word][id] 
                    if self.max_count[id] < count:
                        self.max_count[id] = count

            self.link_dict[id] = outgoing_links

# relevance --------------------------------------------------------------------
    def relevance(self):
        '''
        fills the relevance_dict dictionary that maps words to ids to their 
        relevance score
        '''
        idf_dict = {} # inverse document frequency

        n = len(self.id_to_title)

        for word in self.word_id_count:
            relevance_scores = {}
            ni = len(list(self.word_id_count[word].keys()))
            idf_dict[word] = round(math.log(n/ni), 3)

            for id in self.id_to_title:
                aj = self.max_count[id]
                if id in self.word_id_count[word]:
                    # calculate term frequency:
                    self.word_id_count[word][id] = self.word_id_count[word][id]/aj
                    if idf_dict[word] != 0:
                        relevance_scores[id] = self.word_id_count[word][id] * idf_dict[word]
            self.relevance_dict[word] = relevance_scores

        # don't need these anymore
        self.max_count.clear() 
        self.word_id_count.clear()
 
# page rank -------------------------------------------------------------------- 
    def distance(self, r, r_prime):
        '''
        calculates the euclidian distance between 2 dictionaries whose 
        values are floats

        parameters:
        r -- the first dictionary
        r_prime -- a second dictionary

        returns:
        a number (the distance between the iterations)
        '''
        distance = 0
        for id in r:
            distance = distance + ((r_prime[id] - r[id]) ** 2)
        return math.sqrt(distance)

    def pageRank(self):
        '''
        fills the pank_rage dictionary that maps a page id to its rank
        '''  
        # calculate and store weights: 
        weight_calcs = {}      
        n = len(self.id_to_title)

        for j in self.link_dict:
            j_title = self.id_to_title[j]
            k_dict = {}
            for k in self.link_dict:
                k_title = self.id_to_title[k]
                nk = len(set(self.link_dict[k]))
                # if k has no links or k only links to itself,
                # should link to everything except itself
                if nk == 0 or (nk == 1 and k_title in self.link_dict[k]):
                    nk = n - 1
                # j link to itself is ignored:
                elif j_title in self.link_dict[j]:
                    nk = nk - 1

                if k == j:
                    k_dict[k] = (0.15/n)
                # k links to j:
                elif j_title in self.link_dict[k]:
                    nk = len(set(self.link_dict[k]))
                    k_dict[k] = (0.15/n) + (.85/nk)
                # k links to everything except itself:
                elif nk == n - 1:
                    k_dict[k] = (0.15/n) + (.85/nk)
                else:
                    k_dict[k] = (0.15/n) 

            weight_calcs[j] = k_dict

        self.link_dict.clear()

        # PAGE RANK:
        # initalize all ranks in r to be 0
        r = {id : 0 for id in self.id_to_title} 
        # initalize all ranks in r' to be 1/n
        r_prime = {id: 1/len(self.id_to_title) for id in self.id_to_title} 

        while self.distance(r, r_prime) > 0.001:
            r = r_prime.copy()
            for j in r: 
                r_prime[j] = 0
                for k in r: 
                    k_pages = weight_calcs[j]
                    r_prime[j] = r_prime[j] + k_pages[k] * r[k]   

                self.pank_rage[j] = round(r_prime[j], 4)     

if __name__ == "__main__":
    if len(sys.argv) == 5:
        try: 
            Indexer(*sys.argv[1:])
        except:
            print("files don't exist")
    else:
        print("wrong number of arguments")