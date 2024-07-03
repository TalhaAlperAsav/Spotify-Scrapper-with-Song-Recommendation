'''

Burak TÜZEL - 191805057

Talha Alper ASAV - 201805072

'''

import tkinter as tk
from tkinter import ttk
import pandas as pd
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

class RecommendationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Recommendation App")
        
        self.create_widgets()

    def create_widgets(self):
        # Song name input
        song_label = ttk.Label(self, text="Enter a song name:")
        song_label.pack()
        self.song_entry = ttk.Entry(self)
        self.song_entry.pack()

        # Button to trigger recommendations
        recommend_button = ttk.Button(self, text="Get Recommendations", command=self.get_recommendations)
        recommend_button.pack()

        # Result label
        self.result_label = ttk.Label(self, text="")
        self.result_label.pack()

    def get_recommendations(self):
        input_song = self.song_entry.get()

        fi_recommendations = self.get_frequent_itemset_recommendations(input_song)
        tfidf_recommendations = self.get_tfidf_recommendations(input_song)

        result_text = "Frequent Itemset Recommendations:\n"
        for i, recommendation in enumerate(fi_recommendations, 1):
            result_text += f"{i}. {recommendation}\n"

        result_text += "\nTF-IDF Recommendations:\n"
        for i, recommendation in enumerate(tfidf_recommendations, 1):
            result_text += f"{i}. {recommendation}\n"

        self.result_label.config(text=result_text)

    def get_frequent_itemset_recommendations(self, target_item):
        frequent_itemsets_df = pd.read_csv("frequent_itemsets.csv")
        frequent_itemsets = [set(eval(itemset)) for itemset in frequent_itemsets_df['itemsets']]

        all_recommendations = []
        for itemset in frequent_itemsets:
            if target_item in itemset:
                recommendations = itemset - {target_item}
                all_recommendations.extend(recommendations)

        recommendation_counts = {recommendation: all_recommendations.count(recommendation) for recommendation in set(all_recommendations)}
        sorted_recommendations = sorted(recommendation_counts.items(), key=lambda x: x[1], reverse=True)
        top_recommendations = [recommendation[0] for recommendation in sorted_recommendations[:10]]

        return top_recommendations

    def get_tfidf_recommendations(self, input_song):
        transactions = []
        with open("scrapedSongs.csv", "r", newline="", encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                transactions.append(row)

        playlist_songs = [" ".join(playlist) for playlist in transactions]
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(playlist_songs)

        input_song_tfidf = tfidf_vectorizer.transform([input_song])

        cosine_similarities = linear_kernel(input_song_tfidf, tfidf_matrix).flatten()
        top_indices = cosine_similarities.argsort()[:-10-1:-1]

        recommended_songs = []
        for i in top_indices:
            playlist_songs = transactions[i]
            recommended_songs.extend(playlist_songs)

        recommended_songs = list(set(recommended_songs))

        return recommended_songs[:10]

if __name__ == "__main__":
    app = RecommendationApp()
    app.mainloop()