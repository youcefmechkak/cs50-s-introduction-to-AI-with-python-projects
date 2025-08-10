from re import S
from tabnanny import filename_only
from tkinter.messagebox import QUESTION
import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    docs = dict()

    folder_path = sys.argv[1]

    for x in os.walk(directory) :
        documents =  x[2]

    for document in documents :

        with open(str(folder_path) + os.sep + str(document)) as f:
            lines = f.read()

            
            docs[document] = lines

    return docs



def not_in_punc(word) :
    if word in string.punctuation or word == '–':
        return False
    
    for c in word :
        if c not in string.punctuation :
            return True
    
    return False

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """

    words = list()

    lst = nltk.tokenize.word_tokenize(document)

    for word in lst : 
        word = word.lower()
        if word not in nltk.corpus.stopwords.words("english") and not_in_punc(word): 
            words.append(word)

    return words




def all_count (word, documents) :
    
    i = 0
    for title in documents :
        if word in documents[title] :
            i += 1

    return i

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """

    idf = dict ()

    for file_name in documents :
        for word in documents[file_name] :
            if word not in idf :
                incount = all_count (word , documents)

                idf[word] = math.log(len(documents)/incount)


    return idf



def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    top = dict()

    for filename in files :

        sum = 0
        for word in query :
            if word in files[filename] :
                sum += files[filename].count(word) * idfs[word]

        top[filename] = sum

    top = sorted(top.items(),key=lambda item: item[1],reverse=True)[:n]

    top_files = list ()

    for value in top :
        top_files.append(value[0])

    return top_files



def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    rank = dict ()

    # get the rank of each sentence in sentences
    for sentence in sentences :

        sum = 0
        for word in query :
            if word in sentences[sentence] :
                sum += idfs[word]

        rank[sentence] = sum


    # rank the sentences bases on rank
    best_sentences = sorted(rank.items(),key=lambda item: item[1],reverse=True)




    chosen = list()
    values = list()
    chosen_sen = list()

    # get the best n sentences in the best_sentences list
    for i in range(n) :
        chosen.append(best_sentences[i])
        values.append(best_sentences[i][1])
        chosen.append(best_sentences[i][0])

        best_sentences.remove(best_sentences[i])


    # check if other sentences need to be in the chosen list
    for sentence in best_sentences :
        if sentence[1] in values :
            chosen.append (sentence)
            values.append (sentence[1])
            chosen_sen.append (sentence[0])

    # if there is no conflict return the sentences
    if len(chosen) == n :
        return chosen_sen

    

    # rank based on query term density

    # find the value of the n-1 element
    min = chosen[n-1][1]

    # found how many elements in the list (from [:n]) that have the same value as the n-1 element
    before_num = 0
    for i in range (n) :
        if chosen[i][1] == min :
            before_num += 1

   
    new_ranking = list()  # the elements that needs to be sorted
    new_ranking_sen = list()

    # find the elements that have the value equals min
    for i in range(len (chosen)) :

        if chosen[i][1] == min :
            new_ranking.append(chosen[i])
            new_ranking_sen.append (chosen[i][0])



    # rank the new ranking list bases on query term density
    QTD = dict()
    
    for sentence in new_ranking_sen :
        i = 0
        for word in query :
            if word in sentences[sentence] :
                i += 1

        QTD[sentence] = i / len(sentences[sentence])
    

    # sort the qtd list based on the query term density
    QTD = sorted(QTD.items(),key=lambda item: item[1],reverse=True)


    returned_sentences = chosen_sen[:n-before_num] # the sentences that have no conflict


    for i in range (before_num) :
        returned_sentences.append(QTD[i][0]) # just return the (before_num) elements

    return returned_sentences


if __name__ == "__main__":
    main()
