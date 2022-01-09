import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from apyori import apriori
from codeV2 import*
from time import time

Data2 = pd.read_csv('businessanalytics_panini_purchasereceipts.csv') #, header = None

records = []
for i in range(4573):
    records.append([str(Data2.values[i,j]) for j in range(19)])
for elt in records:
    while 'nan' in elt:
        elt.remove('nan')

'''

            min_support : fiabilité, fixe un seuil en dessous duquel les règles ne sont pas considérées comme fiables. 
                            
                          Support(X) = Transactions contenant (X)/(Transactions Total)
            
            min_confidence : précision de la règle, plus elle est élevée, meilleure est la règle d'association
            
                             Confidence(X → Y) = (Transactions conteant (X et Y))/(Transactions contenant (X))
            
            
            min_lift : caractérise l’intérêt de la règle, sa force (permet aussi de tenir compte de la popularité de deux éléments)
                       
                       Lift(X → Y) = (Confidence (X → Y))/(Support (Y))
                       
                       lift < 1 :  l'article Y est peu susceptible d'être acheté si l'article X est acheté.
                       lift = 1 : absence d'association entre les articles
                       lift > 1 : l'article Y est susceptible d'être acheté si l'article X est acheté.
            


'''

frequent_items = apriori(records, min_support=0.0015, min_confidence=0.25, min_lift=1)
association_results = list(frequent_items)

print("\n\n=====================================")
for item in association_results:

    pair = item[0]
    items = [i for i in pair]
    count_X_and_Y = 0
    count_X = 0
    count_Y = 0
    for elt in records:
        if items[0] in elt and items[1] in elt:
            count_X_and_Y = count_X_and_Y + 1
    for elt in records:
        if items[0] in elt:
            count_X = count_X + 1
    for elt in records:
        if items[1] in elt:
            count_Y = count_Y + 1
    print("\n Rule: " + items[0] + " -> " + items[1])


    print("Support = ", count_X_and_Y/len(records))


    print("Confidence = ", count_X_and_Y/count_X)
    print("Lift = ", (count_X_and_Y/count_X)/(count_Y/len(records)), "\n")
    print("=====================================")
