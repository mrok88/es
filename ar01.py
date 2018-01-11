
# dataset = [['Milk', 'Onion', 'Nutmeg', 'Kidney Beans', 'Eggs', 'Yogurt'],
#            ['Dill', 'Onion', 'Nutmeg', 'Kidney Beans', 'Eggs', 'Yogurt'],
#            ['Milk', 'Apple', 'Kidney Beans', 'Eggs'],
#            ['Milk', 'Unicorn', 'Corn', 'Kidney Beans', 'Yogurt'],
#            ['Corn', 'Onion', 'Onion', 'Kidney Beans', 'Ice cream', 'Eggs']]
from datetime import timedelta, date
from es02 import es02 
dataset = []
if __name__ == "__main__":
    global dataset
    es = es02()
    es.set_service("display")
    es.load_datas2(date(2017,12,1),date(2018,1,8))
    dataset2 = es.dset

dataset = [ item for item in dataset2  if len(item) > 1 ]
for item in dataset:
    print(item)

import pandas as pd
from mlxtend.preprocessing import OnehotTransactions

oht = OnehotTransactions()
oht_ary = oht.fit(dataset).transform(dataset)
df = pd.DataFrame(oht_ary, columns=oht.columns_)
from mlxtend.frequent_patterns import apriori
frequent_itemsets = apriori(df, min_support=0.3,use_colnames=True)
print(frequent_itemsets)

from mlxtend.frequent_patterns import association_rules
arule = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)
print(arule)