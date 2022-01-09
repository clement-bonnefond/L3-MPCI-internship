import pandas as pd
import numpy as np
from  codeV2 import *
from copy import *

Data = pd.read_csv('datamining_buckets.csv') #, header = None

id = pd.read_csv('id_products.csv')

product = id.values.tolist()

for elt in product:
    elt[0] = str(elt[0])
product_bis = product
id_product = []
for i in range(len(product_bis)):
    id_product.append(product_bis[i][0])

Data['liste_actions'] = Data[['liste_actions']].applymap(lambda x: x.split(', '))

table = Data.pivot(index='customer_id', columns='year_week', values='liste_actions').applymap(lambda x: x if isinstance(x, list) else [])

users = table.values.tolist()




