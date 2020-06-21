#!/usr/bin/env python3

from pandas import read_csv
from pandas.plotting import scatter_matrix
from matplotlib import pyplot
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from optparse import OptionParser

def datapeek(dataset):
    # shape
    print(f"instances: {dataset.shape[0]}, attributes: {dataset.shape[1]}")
    print()

    # head
    print("Note: data is in cm")
    print(dataset.head(20))
    print()

    # descriptions
    print(dataset.describe())
    print()

    # class description
    print(dataset.groupby('class').size())
    print()

def datavis(dataset):
    # box and whisker
    dataset.plot(kind='box', subplots=True, layout=(2,2), sharex=False, sharey=False)
    pyplot.show()

    # histograms
    dataset.hist()
    pyplot.show()
    
    # scatter plot matrix
    scatter_matrix(dataset)
    pyplot.show()

def datamodel(dataset):
    # split-out validation dataset
    array = dataset.values
    X = array[:,0:4]
    y = array[:,4]
    X_train, X_validation, Y_train, Y_validation = train_test_split(X, y, test_size=0.20, random_state=1)

    # test different models
    models = []
    models.append(('LR', LogisticRegression(solver='liblinear', multi_class='ovr')))
    models.append(('LDA', LinearDiscriminantAnalysis()))
    models.append(('KNN', KNeighborsClassifier()))
    models.append(('CART', DecisionTreeClassifier()))
    models.append(('NB', GaussianNB()))
    models.append(('SVM', SVC(gamma='auto')))

    # evaluate each model in turn
    results = []
    names = []
    for name, model in models:
        kfold = StratifiedKFold(n_splits=10, random_state=1, shuffle=True)
        cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring='accuracy')
        results.append(cv_results)
        names.append(name)
        print('%s: %f (%f)' % (name, cv_results.mean(), cv_results.std()))
    
    # compare algorithms
    pyplot.boxplot(results, labels=names)
    pyplot.title('Algorithm Comparison')
    pyplot.show()

    # Make predictions on validation dataset
    model = SVC(gamma='auto')
    model.fit(X_train, Y_train)
    predictions = model.predict(X_validation)

    # evaluate predictions
    print(accuracy_score(Y_validation, predictions))
    print(confusion_matrix(Y_validation, predictions))
    print(classification_report(Y_validation, predictions))

def main():
    parser = OptionParser()
    parser.add_option("-p", "--peek", 
        action="store_true",
        dest="peek",
        default=False,
        help="Print some info about the data")
    parser.add_option("-v", "--visualize",
        action="store_true",
        dest="visualize",
        default=False,
        help="plot data")
    parser.add_option("-m", "--model",
        action="store_true",
        dest="model",
        default=False,
        help="model data")
    (options, args) = parser.parse_args()

    # load data
    url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/iris.csv"
    names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
    dataset = read_csv(url, names=names)

    # run requested operations
    if options.peek:
        datapeek(dataset)
    if options.visualize:
        datavis(dataset)
    if options.model:
        datamodel(dataset)

if __name__ == "__main__":
    main()
