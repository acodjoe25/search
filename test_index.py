import pytest
from index import *

def test_example():
    assert 1+1==2
       
def test_dict_fill_id_title():
    tfile = Indexer("testwiki.xml", "titles.txt", "docs.txt", "words.txt") 
    assert tfile.id_to_title[3856] == "Type of cats"
    assert tfile.id_to_title[3859] == "Cats are the superior animal"
    assert tfile.id_to_title[3850] == "dog"

    xfile = Indexer("miniwiki.xml", "titles.txt", "docs.txt", "words.txt") 
    assert xfile.id_to_title[3856] == "This cat is meowing"
    assert xfile.id_to_title[3866] == "Type of cats"
    assert xfile.id_to_title[2] == "Cats"
    assert xfile.id_to_title[5000] == "Cats:Lions in the jungle"

def test_dicts_clear():
    tfile = Indexer("testwiki.xml", "titles.txt", "docs.txt", "words.txt") 
    tfile.link_dict = {}
    tfile.word_id_count = {}
    tfile.max_count = {}

def test_stem_stop():
    xfile = Indexer("testwiki.xml", "titles.txt", "docs.txt", "words.txt")
    # checks that words that should be stemmed are not in the corpus,
    # but their stemmed versions are 
    with pytest.raises(KeyError):
        xfile.relevance_dict["consisting"]
    assert xfile.relevance_dict["consist"][3850] == 0.08453846153846153
    with pytest.raises(KeyError):
        xfile.relevance_dict["featured"]
    assert xfile.relevance_dict["featur"][3859] == 0.08453846153846153
    # checks that stop words are not in the corpus
    with pytest.raises(KeyError):
        xfile.relevance_dict["the"]
    with pytest.raises(KeyError):
        xfile.relevance_dict["a"]      

def test_relevance():
    xfile = Indexer("miniwiki.xml", "titles.txt", "docs.txt", "words.txt") 
    with pytest.raises(KeyError):
        assert xfile.relevance_dict["cat"][3856] == 0
    with pytest.raises(KeyError):
        assert xfile.relevance_dict["meow"][3866] == 0.0
    with pytest.raises(KeyError):
        assert xfile.relevance_dict["meow"][2] == 0.0
    assert xfile.relevance_dict["meow"][3856] == 0.3465
    assert xfile.relevance_dict["meow"][5000] == 0.1386

    ninifile = Indexer("songnini.xml", "titles.txt", "docs.txt", "words.txt")
    ninifile.relevance_dict["proud"][209] == 0.693
    ninifile.relevance_dict["interest"][121] == 0.4620

def test_page_rank_one():
    flomilli = Indexer("PageRankExample1.xml", "titles.txt", "docs.txt", "words.txt")
    assert flomilli.pank_rage[1] == 0.4326
    assert flomilli.pank_rage[2] == 0.2340
    assert flomilli.pank_rage[3] == 0.3333

def test_page_rank_two():
    spilled_milk = Indexer("PageRankExample2.xml", "titles.txt", "docs.txt", "words.txt")
    assert spilled_milk.pank_rage[1] == 0.2018
    assert spilled_milk.pank_rage[2] == 0.0375
    assert spilled_milk.pank_rage[3] == 0.3740
    assert spilled_milk.pank_rage[4] == 0.3867

def test_page_rank_three():
    page_rank_three = Indexer("PageRankExample3.xml", "titles.txt", "docs.txt", "words.txt")
    assert page_rank_three.pank_rage[1] == 0.0524
    assert page_rank_three.pank_rage[2] == 0.0524
    assert page_rank_three.pank_rage[3] == 0.4476
    assert page_rank_three.pank_rage[4] == 0.4476

def test_page_rank_four():
    page_rank_four = Indexer("PageRankExample4.xml", "titles.txt", "docs.txt", "words.txt")
    assert page_rank_four.pank_rage[1] == 0.0375
    assert page_rank_four.pank_rage[2] == 0.0375
    assert page_rank_four.pank_rage[3] == 0.4625
    assert page_rank_four.pank_rage[4] == 0.4625

def test_page_rank_special_case():
    # checking pages that link to nothing:
    xfile = Indexer("miniwiki.xml", "titles.txt", "docs.txt", "words.txt") 
    assert xfile.pank_rage[2] == xfile.pank_rage[5000]

    # checking pages that link to links outside the corpus
    ninifile = Indexer("songnini.xml", "titles.txt", "docs.txt", "words.txt")
    assert ninifile.pank_rage[121] == ninifile.pank_rage[320]

    # mutiple links to same thing
    ffile = Indexer("fakeminiwiki.xml", "titles.txt", "docs.txt", "words.txt")
    assert xfile.pank_rage[3856] == ffile.pank_rage[3856]

