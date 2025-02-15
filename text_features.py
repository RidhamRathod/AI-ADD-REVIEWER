import pytesseract
import cv2
import spacy
import pandas as pd
from textblob import TextBlob
from langid import classify
from PIL import Image
import textstat
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
import language_tool_python

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load spaCy model for NER
nlp = spacy.load("en_core_web_sm")

# Initialize NLTK Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# Initialize LanguageTool for grammar checking
tool = language_tool_python.LanguageTool('en-US')

# Load your CSV
csv_file = "C:\\Users\\Ridham\\Desktop\\demo2 project\\posters.csv"
df = pd.read_csv(csv_file)

# Ensure required columns exist in the dataframe
columns_to_add = [
    "keyword_relevance_score", "explanation_keyword",
    "grammar_accuracy_score", "explanation_grammar",
    "readability_quality", "explanation_readability",
    "sentiment_quality", "explanation_sentiment",
    "call_to_action_quality", "explanation_cta"
]

for col in columns_to_add:
    if col not in df.columns:
        df[col] = None  # Initialize missing columns

# Function to perform OCR
def extract_text_from_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text.strip()

# Readability score (Flesch-Kincaid)
def get_readability_score(text):
    return round(textstat.flesch_reading_ease(text), 1)

# Sentiment intensity (VADER)
def get_sentiment_intensity(text):
    sentiment = analyzer.polarity_scores(text)
    return round(sentiment['compound'], 1)  # Compound score (-1 to 1)

# Keyword relevance score (TF-IDF)
def get_keyword_relevance_score(texts, text):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    tfidf_scores = vectorizer.transform([text])
    feature_names = vectorizer.get_feature_names_out()
    score = tfidf_scores.sum(axis=0)
    scores = {feature_names[i]: score[0, i] for i in range(len(feature_names))}
    return round(max(scores.values()), 1) if scores else 0.0  # Handle empty text case

# Grammar accuracy score (LanguageTool)
def get_grammar_accuracy_score(text):
    if not text.strip():
        return 0.0
    matches = tool.check(text)
    return round(1 - len(matches) / len(text.split()), 2)

# Call-to-action phrases detection
def get_call_to_action_score(text):
    call_to_action_keywords = ["buy", "now", "order", "get started", "shop", "click here"]
    return sum(keyword in text.lower() for keyword in call_to_action_keywords)

# Function to classify and explain quality
def classify_quality(score, score_type):
    if score is None or pd.isna(score):
        return 'low', 'Data not available.'

    explanations = {
        'readability': [
            ("high", "Your text is easy to read and understand for most audiences."),
            ("medium", "Your text is moderately readable but might require some simplification."),
            ("low", "Your text is difficult to read. Consider simplifying sentence structure.")
        ],
        'sentiment': [
            ("positive", "Your text conveys a positive message, which can attract a more engaged audience."),
            ("neutral", "Your text has a balanced tone, neither too positive nor negative."),
            ("negative", "Your text has a negative tone, which may not appeal to all audiences.")
        ],
        'grammar': [
            ("high", "Your text has very few errors, making it grammatically strong."),
            ("medium", "Your text has some grammar issues, which may affect clarity."),
            ("low", "Your text has many grammar issues, which may impact readability.")
        ],
        'call_to_action': [
            ("high", "Your text includes strong call-to-action phrases, increasing engagement."),
            ("medium", "Your text has some call-to-action elements but could be improved."),
            ("low", "Your text lacks effective call-to-action words.")
        ],
        'keyword': [
            ("high", "Your poster has highly relevant keywords, making it more impactful."),
            ("medium", "Your poster has some relevant keywords, but could be improved."),
            ("low", "Your poster lacks strong keywords, which may reduce its effectiveness.")
        ]
    }

    # Assign categories
    if score_type in ['readability', 'sentiment', 'grammar', 'call_to_action', 'keyword']:
        if score > 0.8:
            return explanations[score_type][0]
        elif 0.5 < score <= 0.8:
            return explanations[score_type][1]
        else:
            return explanations[score_type][2]

    return 'low', 'No explanation available.'

# Process images and extract features
for index, row in df.iterrows():
    image_path = f"C:\\Users\\Ridham\\Desktop\\demo2 project\\images\\{row['poster_id']}.png"
    text = extract_text_from_image(image_path)

    # Extract features
    keyword_relevance_score = get_keyword_relevance_score(
        df['poster_id'].apply(lambda x: extract_text_from_image(
            f"C:\\Users\\Ridham\\Desktop\\demo2 project\\images\\{x}.png")).tolist(), 
        text
    )
    grammar_accuracy_score = get_grammar_accuracy_score(text)
    readability_score = get_readability_score(text)
    sentiment_score = get_sentiment_intensity(text)
    call_to_action_score = get_call_to_action_score(text)

    # Classify and explain
    readability_quality, explanation_readability = classify_quality(readability_score, 'readability')
    sentiment_quality, explanation_sentiment = classify_quality(sentiment_score, 'sentiment')
    grammar_quality, explanation_grammar = classify_quality(grammar_accuracy_score, 'grammar')
    call_to_action_quality, explanation_cta = classify_quality(call_to_action_score, 'call_to_action')
    keyword_quality, explanation_keyword = classify_quality(keyword_relevance_score, 'keyword')

    # Assign values to DataFrame
    df.at[index, 'keyword_relevance_score'] = keyword_relevance_score
    df.at[index, 'explanation_keyword'] = explanation_keyword
    df.at[index, 'grammar_accuracy_score'] = grammar_accuracy_score
    df.at[index, 'explanation_grammar'] = explanation_grammar
    df.at[index, 'readability_quality'] = readability_quality
    df.at[index, 'explanation_readability'] = explanation_readability
    df.at[index, 'sentiment_quality'] = sentiment_quality
    df.at[index, 'explanation_sentiment'] = explanation_sentiment
    df.at[index, 'call_to_action_quality'] = call_to_action_quality
    df.at[index, 'explanation_cta'] = explanation_cta

# Print to check if updates are applied
print(df.head())

# Save the updated CSV
df.to_csv("updated_posters.csv", index=False)

print("Feature extraction complete. CSV updated with explanations.")
