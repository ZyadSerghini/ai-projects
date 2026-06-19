import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4

MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")

INTS = (0, 2, 4, 11, 12, 13, 14) 

def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    field, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        field, labels, test_size=TEST_SIZE
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


def load_data(filename = 'shopping.csv'):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    field lists and a list of labels. Return a tuple (field, labels).

    field should be a list of lists, where each list contains the
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
    
    file = open(filename, 'r')
    r = csv.reader(file)
    file.readline()
    
    evidence = []
    labels = []
    
    for row in r:
        field = []
        
        for i in range(len(row)):
            entry = row[i]
            
            #Month
            if i == 10:
                field.append(MONTHS.index(entry))
            
            #New/Returning visitor
            elif i == 15:
                if entry == "Returning_Visitor":
                    field.append(1)
                else:
                    field.append(0)
            
            #Weekend
            elif i == 16:
                if entry == "TRUE":
                    field.append(1)
                else:
                    field.append(0)
            
            #Purchase        
            elif i == 17:
                if entry == "TRUE":
                    labels.append(1)
                else:
                    labels.append(0)
            
            #INTS
            elif i in INTS:
                field.append(int(entry))
            #FLOATS
            else:
                field.append(float(entry))
        
        assert len(field) == 17, f"Length of field is {len(field)}."
        evidence.append(field)
        
    file.close()   
    return (evidence, labels)
    
    
def train_model(field, labels):
    """
    Given a list of field lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    classifier = KNeighborsClassifier(n_neighbors = 1)
    classifier.fit(field, labels)
    
    return classifier

    # Make a prediction on new data
    #prediction = classifier.predict([[0, 0.0, 0, 0.0, 21, 331.0833333, 0.00952381, 0.042857143, 0.0, 0.0, 11, 2, 2, 1, 2, 1, 0]])
    #print(prediction)

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
    assert len(labels) == len(predictions), "Number of predictions does not match number of actual labels."
    
    nb_true_pos = 0
    nb_true_neg = 0
    
    nb_actual_pos = 0
    nb_actual_neg = 0
    
    n = len(labels)
    
    for i in range(n):
        if labels[i] == 1:
            nb_actual_pos += 1
            if predictions[i] == 1:
                nb_true_pos += 1
        else:
            nb_actual_neg += 1
            if predictions[i] == 0:
                nb_true_neg += 1
    
    return (nb_true_pos/nb_actual_pos, nb_true_neg/nb_actual_neg)
        


if __name__ == "__main__":
    main()
