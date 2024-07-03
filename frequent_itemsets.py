'''

Burak TÜZEL - 191805057

Talha Alper ASAV - 201805072

'''

import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
import csv

# Read transactions from the playlist data
file_path = "scrapedSongs.csv"
transactions = []
with open(file_path, "r", newline="", encoding="utf-8") as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        transactions.append(row)

# Find frequent itemsets using the Apriori algorithm from mlxtend
te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
df = pd.DataFrame(te_ary, columns=te.columns_)
min_support = 0.01  # Minimum support threshold
frequent_itemsets = apriori(df, min_support=min_support, use_colnames=True)

# Save frequent itemsets to a CSV file
output_file = "frequent_itemsets.csv"
frequent_itemsets.to_csv(output_file, index=False, encoding="utf-8-sig")
