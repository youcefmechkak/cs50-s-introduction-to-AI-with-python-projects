from cProfile import label
import csv
from re import A
import sys

import numpy


from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    months = {'Jan' : 0, 'Feb' :1 , 'Mar' : 2, 
              'Apr' : 3, 'May' : 4, 'June' : 5 , 
              'Jul' : 6 , 'Aug' : 7 , 'Sep' : 8 , 
              'Oct' : 9 , 'Nov' : 10, 'Dec' : 11}

    evidence = list ()
    labels = list()

    i = 0

    with open(filename, 'r') as csvfile:
        rows = csv.reader(csvfile)

        
        for row in rows: # if row is not none
            
            # excluding the header row
            if i == 0 :
                i += 1
                continue
            

            # the evidence part
            tmp = [0 ,0 , 0 , 0 , 0 ,0 , 0 , 0,0 ,0 , 0 , 0,0 ,0 , 0 , 0,0]

            # convert into int
            tmp[0] = int(row[0])
            tmp[2] = int (row[2])
            tmp[4] = int (row[4])
            tmp[10] = months[row[10]]
            tmp[11] = int (row[11])
            tmp[12] = int (row[12])
            tmp[13] = int (row[13])
            tmp[14] = int (row[14])

            if row[15] == 'Returning_Visitor' :
                tmp[15] = 1
            else :
                tmp[15] = 0

            if row[16] == 'TRUE' :
                tmp[16] = 1
            else :
                tmp[16] = 0


            # convert into float
            tmp[1] = float(row[1])
            tmp[3] = float(row[3])
            tmp[5] = float(row[5])
            tmp[6] = float(row[6])
            tmp[7] = float(row[7])
            tmp[8] = float(row[8])
            tmp[9] = float(row[9])


            evidence.append(tmp)


            # the label part

            if row[17] == 'TRUE' :
                labels.append(1)
            else :
                labels.append(0)

            i+=1

    return (evidence, labels)




            
            


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """

    model = KNeighborsClassifier (n_neighbors= 1)

    model.fit(evidence, labels)

    return model

    

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    
    true_true = 0
    total_true = 0

    false_false = 0
    total_false = 0

    for i in range (len(labels)) :
        
        

        if labels[i] == 1 :
            if predictions[i] == labels[i] :
                true_true += 1
            total_true += 1

        else :
            if predictions[i] == labels[i] :
                false_false += 1
            total_false += 1
            
    return (true_true/total_true , false_false/total_false)


if __name__ == "__main__":
    main()
