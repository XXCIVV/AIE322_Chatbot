import pandas as pd
import numpy as np
import faiss
import requests
import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

# Step 1: Download Datasets
match_url = "https://raw.githubusercontent.com/martj42/international_results/master/results.csv"
player_stats_url = "https://raw.githubusercontent.com/RonGO4/Football-Player-Dataset-2022-2023-/refs/heads/main/Football%20player_stats%20.csv"

match_path = "soccer_matches.csv"
player_stats_path = "player_stats.csv"

def download_dataset(url, path):
    """Download dataset if it doesn't already exist."""
    if not os.path.exists(path):
        response = requests.get(url)
        if response.status_code == 200:
            with open(path, 'wb') as file:
                file.write(response.content)
            print(f"Dataset {path} downloaded successfully.")
        else:
            print(f"Failed to download {path}. HTTP Status: {response.status_code}")
    else:
        print(f"Dataset {path} already exists.")

# Download available datasets
download_dataset(match_url, match_path)
download_dataset(player_stats_url, player_stats_path)

# Step 2: Load Data
try:
    df_matches = pd.read_csv(match_path)
    print("Match dataset loaded successfully.")
except Exception as e:
    print(f"Error loading match dataset: {e}")
    df_matches = pd.DataFrame()

try:
    df_players = pd.read_csv(player_stats_path, encoding='utf-8', on_bad_lines='skip')
    df_players.columns = df_players.columns.str.strip()  # Trim column names
    print("Player statistics dataset loaded successfully.")
except Exception as e:
    print(f"Error loading player dataset: {e}")
    df_players = pd.DataFrame()

# Step 3: Preprocess Data for FAISS Indexing
if not df_matches.empty and {'date', 'home_team', 'away_team', 'home_score', 'away_score'}.issubset(df_matches.columns):
    df_matches['match_info'] = df_matches.apply(lambda row: f"{row['date']} - {row['home_team']} vs {row['away_team']} (Score: {row['home_score']} - {row['away_score']})", axis=1)
else:
    df_matches['match_info'] = ""

required_columns = {'Player name', 'Squad', 'Goal', 'Assist'}
if not df_players.empty and required_columns.issubset(df_players.columns):
    df_players['player_info'] = df_players.apply(lambda row: f"{row['Player name']} - {row['Squad']}: {row['Goal']} goals, {row['Assist']} assists", axis=1)
else:
    print("Warning: Player dataset is missing required columns or is empty.")
    df_players['player_info'] = []

# Combine all text data
all_texts = df_matches['match_info'].tolist() + df_players['player_info'].tolist()

# Convert text to embeddings (TF-IDF for FAISS indexing)
if all_texts:
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(all_texts).toarray().astype('float32')

    if X.shape[0] > 0:  # Ensure data exists before indexing
        d = X.shape[1]  # Dimension of embeddings
        index = faiss.IndexFlatL2(d)  # L2 Distance-based Index
        index.add(X)

        # Step 4: Save FAISS Index, Vectorizer, and Text Data
        faiss.write_index(index, "faiss_soccer_index.idx")
        with open("vectorizer.pkl", "wb") as f:
            pickle.dump(vectorizer, f)

        # ✅ **Save text data to CSV (fix missing file issue!)**
        pd.DataFrame({"text": all_texts}).to_csv("soccer_text_data.csv", index=False)

        print("✅ FAISS Index Created and Saved Successfully.")
    else:
        print("⚠ Warning: No valid data for FAISS indexing.")
else:
    print("⚠ Warning: No data available for FAISS indexing.")

print("✅ Data processing complete. Run the Flask server separately.")
