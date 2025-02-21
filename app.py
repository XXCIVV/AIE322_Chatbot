from flask import Flask, request, jsonify, render_template
import faiss
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import os

# File Paths
INDEX_PATH = "faiss_soccer_index.idx"
VECTORIZER_PATH = "vectorizer.pkl"
TEXT_DATA_PATH = "soccer_text_data.csv"  # Ensure this matches the FAISS indexing script

app = Flask(__name__)

# Check if required files exist
if not os.path.exists(INDEX_PATH):
    raise FileNotFoundError(f"FAISS index file '{INDEX_PATH}' not found. Please run the indexing script first.")

if not os.path.exists(VECTORIZER_PATH):
    raise FileNotFoundError(f"Vectorizer file '{VECTORIZER_PATH}' not found. Please run the indexing script first.")

if not os.path.exists(TEXT_DATA_PATH):
    raise FileNotFoundError(f"Text data file '{TEXT_DATA_PATH}' not found. Ensure it's created properly.")

# Load FAISS Index
try:
    index = faiss.read_index(INDEX_PATH)
except Exception as e:
    raise RuntimeError(f"Error loading FAISS index: {e}")

# Load Vectorizer
try:
    with open(VECTORIZER_PATH, "rb") as f:
        vectorizer = pickle.load(f)
except Exception as e:
    raise RuntimeError(f"Error loading vectorizer: {e}")

# Load Text Data
try:
    text_data = pd.read_csv(TEXT_DATA_PATH)
    all_texts = text_data["text"].tolist()
except Exception as e:
    raise RuntimeError(f"Error loading text data: {e}")

def query_faiss(query_text, top_k=5):
    """Search FAISS index and return relevant text results."""
    try:
        query_vector = vectorizer.transform([query_text]).toarray().astype('float32')
        distances, indices = index.search(query_vector, top_k)

        results = [all_texts[i] for i in indices[0] if 0 <= i < len(all_texts)]
        return results if results else ["No relevant results found."]
    
    except Exception as e:
        return [f"Error processing query: {str(e)}"]

@app.route('/')
def home():
    """Render homepage with example guidelines."""
    guidelines = [
        "Ask about past match results (e.g., 'What was the score of the last World Cup final?').",
        "Inquire about teams (e.g., 'How did Barcelona perform in their last match?').",
        "Ask for player statistics (e.g., 'How many goals did Messi score last season?')."
    ]
    return render_template('index.html', guidelines=guidelines)

@app.route('/query', methods=['POST'])
def query():
    """Handle FAISS query requests."""
    data = request.json
    query_text = data.get('query', '').strip()

    if not query_text:
        return jsonify({"results": ["Please enter a valid question."]})

    results = query_faiss(query_text)
    return jsonify({"results": results})

if __name__ == '__main__':
    app.run(debug=True)
