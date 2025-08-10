from curses.ascii import isalpha
import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""
# 

NONTERMINALS = """
S -> NP VP
AdjP -> Adj | Adj AdjP
NP -> N | AdjP NP | N PP | N ConjP | N Adv | Det N NP | Det Adj NP | Det N | Det Adj | PP | ConjP | Adv
PP -> P NP
VP -> V | V NP | V NP P | V ConjP | V PP | V Adv ConjP
ConjP -> Conj NP | Conj VP | Conj NP VP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    words = list ()

    lst = nltk.tokenize.word_tokenize(sentence)

    for word in lst :
        alpha = False

        for letter in word :
            if letter.isalpha() :
                alpha = True
                break
        

        if alpha :
            words.append (word.lower())

    return words
        


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    NP_s = list ()

    for t in tree.subtrees() :
        if t.label() == "NP" :
            check = True


            i = 0
            for sub_t in t.subtrees() :
                if i == 0 :
                    i+=1
                    continue
                if sub_t.label () == "NP" :
                    check = False

            if check :
                NP_s.append (t)


    return NP_s



if __name__ == "__main__":
    main()
