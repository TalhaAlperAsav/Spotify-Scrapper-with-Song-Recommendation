import csv
'''

Burak TÜZEL - 191805057

Talha Alper ASAV - 201805072

'''

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Read transactions from the playlist data
file_path = "scrapedSongs.csv"
transactions = []
with open(file_path, "r", newline="", encoding="utf-8") as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        transactions.append(row)

# Preprocess data
playlist_songs = [" ".join(playlist) for playlist in transactions]
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(playlist_songs)

# Function to recommend songs
def recommend_songs(input_song, tfidf_matrix, tfidf_vectorizer, n=10):
    input_song_tfidf = tfidf_vectorizer.transform([input_song])
    
    # Calculate cosine similarity
    cosine_similarities = linear_kernel(input_song_tfidf, tfidf_matrix).flatten()

    # Get indices and scores of top n similar playlists
    top_indices_with_scores = [(i, score) for i, score in enumerate(cosine_similarities)]
    top_indices_with_scores.sort(key=lambda x: x[1], reverse=True)
    top_indices_with_scores = top_indices_with_scores[:n]

    # Get songs from the recommended playlists
    recommended_songs = []
    for i, _ in top_indices_with_scores:
        playlist_songs = transactions[i]
        recommended_songs.extend(playlist_songs)

    # Remove duplicates from recommended songs
    recommended_songs = list(set(recommended_songs))

    # Get TF-IDF scores of recommended songs
    tfidf_scores = []
    for song in recommended_songs:
        song_tfidf = tfidf_vectorizer.transform([song])
        tfidf_score = song_tfidf.max()  # Get the maximum TF-IDF score for the song
        tfidf_scores.append((song, tfidf_score))

    # Sort TF-IDF scores in descending order
    tfidf_scores.sort(key=lambda x: x[1], reverse=True)

    return recommended_songs[:n], top_indices_with_scores, tfidf_scores[:n]

# Example usage
input_song = "Poşet"
recommendations, top_indices_with_scores, tfidf_scores = recommend_songs(input_song, tfidf_matrix, tfidf_vectorizer)
print("Top 10 recommended songs for:", input_song)
for song in recommendations:
    print(song)

# Printing top indices with scores
print("\nTop indices with scores:")
for index, score in top_indices_with_scores:
    print("Playlist Index:", index, "Score:", score)

# Printing top 10 TF-IDF scores of recommended songs
print("\nTop 10 TF-IDF scores of recommended songs:")
for song, tfidf_score in tfidf_scores:
    print("Song:", song, "TF-IDF Score:", tfidf_score)
