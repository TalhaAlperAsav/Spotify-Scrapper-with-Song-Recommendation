'''

Burak TÜZEL - 191805057

Talha Alper ASAV - 201805072

'''

import pandas as pd

# Read frequent itemsets from the CSV file
frequent_itemsets_file = "frequent_itemsets.csv"
frequent_itemsets_df = pd.read_csv(frequent_itemsets_file)

# Extract frequent itemsets as a list of sets
frequent_itemsets = [set(eval(itemset)) for itemset in frequent_itemsets_df['itemsets']]

target_item = 'Poşet'

# Generate recommendations for the target item
all_recommendations = []
for itemset in frequent_itemsets:
    if target_item in itemset:
        recommendations = itemset - {target_item}
        all_recommendations.extend(recommendations)

# Count occurrences of each recommendation
recommendation_counts = {recommendation: all_recommendations.count(recommendation) for recommendation in set(all_recommendations)}

# Sort recommendations by their frequency in descending order
sorted_recommendations = sorted(recommendation_counts.items(), key=lambda x: x[1], reverse=True)

# Extract top 10 unique recommendations from the sorted list
top_recommendations = [recommendation[0] for recommendation in sorted_recommendations[:10]]

# Print top 10 recommendations
print("Top {} Unique Recommendations Ordered by Frequency:".format(len(top_recommendations)))
for recommendation in top_recommendations:
    print(recommendation)