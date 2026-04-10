"""cleans raw data & make clean dataset"""

"""cleans raw data & make clean dataset"""

import json
import spacy
import re
import nltk
from nltk.corpus import stopwords
from unidecode import unidecode
import emoji
from pathlib import Path

# Initialize spacy lemmatizer and nltk stopwords
nlp = spacy.load('en_core_web_sm')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))


def clean_text(text):
    """Clean text by removing punctuation, emojis, and extra whitespaces."""
    text = emoji.replace_emoji(text, replace='')
    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    text = unidecode(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def remove_stopwords(text):
    """Remove stopwords from text."""
    return ' '.join([word for word in text.split() if word not in stop_words])


def lemmatize_text(text):
    """Lemmatize the text."""
    doc = nlp(text)
    return ' '.join([token.lemma_ for token in doc if not token.is_stop])


def process_review(review, review_id):
    """Clean and process the review data."""

    # Clean the review content
    cleaned_content = clean_text(review['content'])

    # Remove stopwords and lemmatize the text
    cleaned_content = remove_stopwords(cleaned_content)
    cleaned_content = lemmatize_text(cleaned_content)

    # Filter out extremely short reviews
    if len(cleaned_content) < 15:
        return None

    cleaned_review = {
        'reviewId': review_id,
        'userName': review['userName'],
        'content': cleaned_content,
        'score': review['score'],
        'at': review['at'],
        'replyContent': review.get('replyContent', ''),
        'appVersion': review.get('appVersion', '')
    }

    return cleaned_review


def load_reviews(input_path):
    """Load reviews from the JSONL file."""
    reviews = []
    with open(input_path, 'r', encoding='utf-8') as file:
        for line in file:
            reviews.append(json.loads(line.strip()))
    return reviews


def save_reviews(reviews, output_path):
    """Save reviews to a JSONL file."""
    with open(output_path, 'w', encoding='utf-8') as file:
        for review in reviews:
            file.write(json.dumps(review, ensure_ascii=False) + '\n')


def main():
    project_root = Path(__file__).resolve().parents[1]
    input_file = project_root / "data" / "reviews_raw.jsonl"
    output_file_clean = project_root / "data" / "reviews_clean.jsonl"
    output_file_human = project_root / "data" / "reviews_human_readable.jsonl"

    print("Loading raw reviews...")
    reviews = load_reviews(input_file)
    print(f"Loaded {len(reviews)} raw reviews.")

    print("Cleaning and processing reviews...")

    cleaned_reviews = []
    human_readable_reviews = []

    seen_review_ids = set()
    review_counter = 1

    for review in reviews:

        # Remove duplicates based on original reviewId
        if review['reviewId'] in seen_review_ids:
            continue

        seen_review_ids.add(review['reviewId'])

        review_id = f"rev_{str(review_counter).zfill(4)}"

        # --- Clean content FIRST (for filtering decision) ---
        cleaned_content = clean_text(review['content'])
        cleaned_content = remove_stopwords(cleaned_content)
        cleaned_content = lemmatize_text(cleaned_content)

        # Filter BEFORE saving anything
        if len(cleaned_content) < 15:
            continue

        # --- Human-readable version (RAW content) ---
        human_readable_review = {
            'reviewId': review_id,
            'userName': review['userName'],
            'content': review['content'],
            'score': review['score'],
            'at': review['at'],
            'replyContent': review.get('replyContent', ''),
            'appVersion': review.get('appVersion', '')
        }

        # --- Cleaned version ---
        cleaned_review = {
            'reviewId': review_id,
            'userName': review['userName'],
            'content': cleaned_content,
            'score': review['score'],
            'at': review['at'],
            'replyContent': review.get('replyContent', ''),
            'appVersion': review.get('appVersion', '')
        }

        human_readable_reviews.append(human_readable_review)
        cleaned_reviews.append(cleaned_review)

        review_counter += 1

    print(f"Saving {len(cleaned_reviews)} cleaned reviews to {output_file_clean}...")
    save_reviews(cleaned_reviews, output_file_clean)

    print(f"Saving {len(human_readable_reviews)} human-readable reviews to {output_file_human}...")
    save_reviews(human_readable_reviews, output_file_human)

    print("Cleaning process completed!")


if __name__ == "__main__":
    main()