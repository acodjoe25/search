# search
This is a search engine consisting of two main steps: indexing and querying. We used a combination of the PageRank algorthim and relevance computations to build this code.

Instructions for use:
First, the user needs to index an xml file. To do so, open the terminal and
enter: 
    "python3 index.py <XML filepath> <titles filepath> <docs filepath> <words filepath>".
Next, run the querier. If you would not like to use the pagerank algorithm, enter in the terminal:
    "python3 query.py <XML filepath> <titles filepath> <docs filepath> <words filepath>"
if you would like to use the pagerank algorithm, enter in the terminal:
    "python3 query.py --pagerank <XML filepath> <titles filepath> <docs filepath> <words filepath>"
From here, the terminal will prompt a ">search:". You can now type in anything you want to use 
the program! :D When you are done, type in ":quit" to stop. 

How it all fits together:
There are two major parts to the program -- Indexer and Querier. The Indexer takes
in an XML file and parses it using the parse function. Here, it sorts titles and ids;
and sorts, stops, and stems all the text. Then, based off of the parsed data, the relevance
function calculates the importance of each word in the file to each page in the file. This
calculation depends on term frequency and inverse document frequency. The page rank 
function calculates the importance of links to other links in the XML file. It uses
a weights calculation to check how much "weight" each link gives to every other link 
and repeats all these calculations until the difference between the computations
converge (found using distance equation). The Indexer also reads this information
into the inputted titles doc, docs doc, and words doc. The Querier then writes in these files
and uses a REPL loop to relate the user input to the stored information to output
search results.

Features:
We implemented all the features to the best of our ability (pagerank and all!). 
There are no extra features.

Testing:
We tested the Indexer by using unit tests on the global variables, which includes
filling in ids to titles, relevance, page rank. The correctness of intermediate 
calculations should be reflected in the correctness of these variables. We also
split these calculations into their own methods while we were writing the program
initially, and did unit tests at this stage (which passed). We used some
of our own XML files and calculated some things by hand as well as the provided
page rank example files. For our own page rank tests, we checked when links
don't link to anything and when they link to things outside the corpus. The 
provided page rank tests already check when links link to themselves.

We tested the Querier by performing system tests on MedWiki, which are pasted below.
We tested general cases given to us in the TA results google doc, and tested
for the no results case and the less than 10 results case.

