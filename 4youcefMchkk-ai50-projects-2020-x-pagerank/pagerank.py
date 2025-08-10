import os
#import random
import re
import sys
from typing import Counter
from numpy import random 

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


# the distribution of the dump part
def dump (corpus) :
    dist = list ()

    for i in range(len(corpus)) :
        dist.append (1/len(corpus))
    
    return dist

# the distibution of the other case
def not_dump (corpus, links) :

    dis = list ()

    pages = list(corpus)

    for page in pages :
        if page in links :
            dis.append (1/len(links))
        else :
            dis.append (0)
    return dis


# create a dictionary given a pages list and a distribution
def create_dict (links, dis) :
    dictn = dict()

    for i in range (len (links)) :
        dictn[links[i]] = dis[i]
    
    return dictn


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    
    # find the links taged by the 'page'

    links = corpus[page]


    dis = dump(corpus)

    # if the page doesn't have links to other pages
    if len(links) == 0 :

        return create_dict (list(corpus), dis)

    else :  # add the distribution of the dump part and the other part
        dis2 = not_dump (corpus, links)

        new_dist = list ()

        for i in range (len(dis)) :
            new_dist.append (( (1 - damping_factor) * dis[i]) + (damping_factor * dis2[i]))
        
        return create_dict (list(corpus), new_dist)



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    samples = list()

    # generate the first sample

    pages = list(corpus)

    start = random.choice (pages)
    samples.append (start)

    d = transition_model (corpus, start ,damping_factor)


    for i in range (n-1) :
        sample = random.choice (list(d.keys()) ,p = list(d.values()))
        samples.append (sample)
        d = transition_model (corpus , sample , damping_factor)
    

    t = Counter (samples)

    keys = list(t.keys())
    values = list(t.values())

    sum = 0
    for value in values :
        sum = sum + value
   


    new = dict()

    for i in range(len(keys)) :
        new[keys[i]] = (values[i])/sum


    for page in list(corpus) :
        if page not in new :
            new[page] = 0.0

    return new


#----------------------------------------------------------------

# the number of links in a page
def num_links (corpus, page) :
    return len(corpus[page])

# find all the pages that links to 'page'
def linked (corpus, page) :
    pages = list()

    for element in list(corpus) :
        if page in corpus[element] :
            pages.append(element)

    return pages


def second_c (probability ,corpus, page) :

    # find all the pages that links to 'page'
    pages = linked (corpus , page)

    sum = 0


    for link_page in pages :
        sum = sum + (probability[link_page]/num_links(corpus, link_page))

    return sum

def PR (probability, corpus, page, d) :
    return ( ((1-d)/len(list(corpus))) + (d * second_c(probability, corpus , page)))


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # edit pages with no links
    new_corpus = dict()


    for page in list(corpus) :
        if num_links(corpus, page) == 0 :
            new_corpus[page] = set(list(corpus))
        else :
            new_corpus[page] = corpus[page]




    # assigning each page a rank of 1 / N, where N is the total number of pages in the corpus.
    probability = dict ()

    for page in list(new_corpus) :
        probability[page] = (1/len(list(new_corpus)))


    # loop for each page in the corpus

    check = False

    while check == False :
        checks = list ()

        for page in list(new_corpus) :
            tmp = probability[page]
            probability[page] = PR(probability , new_corpus, page, damping_factor)

            if abs(tmp-probability[page]) <= 0.001:
                checks.append (True)
            else :
                checks.append (False)
            

        if False not in checks :
            check = True


    

    return probability



if __name__ == "__main__":
    main()
