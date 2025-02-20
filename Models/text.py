import pytesseract
import cv2
import spacy
import textstat
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import language_tool_python

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize NLTK Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# Initialize LanguageTool for grammar checking
tool = language_tool_python.LanguageTool('en-US')

# Function to extract text from an image
'''def extract_text(image_path):
    #image_path = r"D:\PYTHON\Sem6Project\Test_imgs\p8.png"  # Directly using the image path
    img = cv2.imread(image_path)

    if img is None:
        return None, "Error: Could not load the image. Please check the file path."

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text.strip(), None'''

# Readability score (Flesch-Kincaid)
def evaluate_readability(image_path):
    img = cv2.imread(image_path)

    if img is None:
        return None, "Error: Could not load the image. Please check the file path."

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    text.strip()
    #return text.strip(), None

    score = textstat.flesch_reading_ease(text)
    if score > 80:
        return f"{score:.1f} - ✅ Easy to read."
    elif score > 50:
        return f"{score:.1f} - ⚠️ Moderate readability."
    elif score > 20:
        return f"{score:.1f} - 🔎 Some areas aren't readable."
    else:
        return f"{score:.1f} - ❌Difficult to read"

# Sentiment intensity (VADER)
def evaluate_sentiment(image_path):
    img = cv2.imread(image_path)

    if img is None:
        return None, "Error: Could not load the image. Please check the file path."

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    text.strip()
    sentiment = analyzer.polarity_scores(text)
    if sentiment['compound'] > 0.5:
        return f"{sentiment['compound']:.1f} - ✅ Positive sentiment."
    elif sentiment['compound'] > -0.5:
        return f"{sentiment['compound']:.1f} - ⚠️ Neutral sentiment."
    else:
        return f"{sentiment['compound']:.1f} - ❌ Negative sentiment."

# Grammar accuracy
def evaluate_grammar(image_path):
    img = cv2.imread(image_path)

    if img is None:
        return None, "Error: Could not load the image. Please check the file path."

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    text.strip()
    if not text.strip():
        return "0.0 - ❌ No text detected."
    
    matches = tool.check(text)
    error_rate = len(matches) / max(len(text.split()), 1)  # Avoid division by zero
    accuracy_score = max(1 - error_rate, 0)

    if accuracy_score > 0.8:
        return f"{accuracy_score:.1f} - ✅ Strong grammar."
    elif accuracy_score > 0.5:
        return f"{accuracy_score:.1f} - ⚠️ Moderate grammar accuracy."
    else:
        return f"{accuracy_score:.1f} - ❌ Poor grammar."

# Call-to-action phrase detection
def evaluate_call_to_action(image_path):
    img = cv2.imread(image_path)

    if img is None:
        return None, "Error: Could not load the image. Please check the file path."

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    text.strip()
    call_to_action_keywords = [
    # Direct Action Verbs
    "Buy Now", "Subscribe", "Sign Up", "Download", "Shop Now", "Get Started",
    "Learn More", "Order Now", "Try It Free", "Register", "Join Us", "Watch Now",
    "Explore", "Get Access", "Claim Offer", "Add to Cart", "Discover",

    # Urgency and Scarcity Words
    "Limited Time Offer", "Hurry", "Act Now", "Don't Miss Out", "Only X Left",
    "Exclusive Offer", "Last Chance",

    # Value-Oriented Phrases
    "See Why", "Find Out How", "Start Your Free Trial", "Unlock Benefits",
    "Discover More", "Get Your Discount", "Experience More", "Claim Your Prize",

    # Social Proof and Trust-Oriented CTAs
    "Join Thousands of Happy Customers", "See What Others Are Saying",
    "Start Your Journey", "Trust the Experts", "Get the App", "Join Our Community",

    # Interactive or Engaging CTAs
    "Take the Quiz", "Get Your Free Estimate", "Start the Test",
    "Check Availability", "Join the Waitlist", "Take Action", "Get Your Personalized Plan"
]

    count = sum(1 for word in call_to_action_keywords if word in text.lower())

    if count >= 2:
        return f"{count} - ✅ Strong call to action.[Call to action suggests how encouraging/appealing the message is.]"
    elif count == 1:
        return f"{count} - ⚠️ Moderate call to action.[Call to action suggests how encouraging/appealing the message is.]"
    else:
        return f"{count} - ❌ Weak call to action.[Call to action suggests how encouraging/appealing the message is.]"

# Extract text
# text, error = extract_text()

'''if error:
    print(error)
else:
    print("\n--- Poster Evaluation Results ---")
    print(evaluate_readability(text))
    print(evaluate_sentiment(text))
    print(evaluate_grammar(text))
    print(evaluate_call_to_action(text))'''