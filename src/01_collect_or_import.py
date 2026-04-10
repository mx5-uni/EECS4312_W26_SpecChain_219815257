"""imports or reads your raw dataset; if you scraped, include scraper here"""

import json
from datetime import datetime, date
from pathlib import Path
from google_play_scraper import Sort, reviews


APP_ID = 'meditofoundation.medito'
MAX_REVIEWS = 2000
BATCH_SIZE = 200  # how many to fetch per request, this is also the max google play will allow


def fetch_reviews_limited(app_id, max_reviews, batch_size):
    """Fetch reviews up to a maximum limit using pagination."""
    all_reviews = []
    continuation_token = None

    while len(all_reviews) < max_reviews:
        remaining = max_reviews - len(all_reviews)
        count = min(batch_size, remaining)

        result, continuation_token = reviews(
            app_id,
            lang='en',
            country='us',
            sort=Sort.NEWEST,
            count=count,
            continuation_token=continuation_token
        )

        if not result:
            break

        all_reviews.extend(result)
        print(f"Fetched {len(all_reviews)} reviews so far...")

        if continuation_token is None:
            break

    return all_reviews


def sanitize(obj):
    """Recursively convert non-JSON-serializable objects."""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()

    if isinstance(obj, dict):
        return {key: sanitize(value) for key, value in obj.items()}

    if isinstance(obj, list):
        return [sanitize(item) for item in obj]

    return obj


def save_to_jsonl(reviews, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        for review in reviews:
            clean_review = sanitize(review)
            f.write(json.dumps(clean_review, ensure_ascii=False) + '\n')


def main():
    project_root = Path(__file__).resolve().parents[1]
    data_dir = project_root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    output_file = data_dir / "reviews_raw.jsonl"

    print("Fetching reviews...")
    reviews_data = fetch_reviews_limited(APP_ID, MAX_REVIEWS, BATCH_SIZE)
    print(f"Total fetched: {len(reviews_data)} reviews.")

    print(f"Saving to {output_file}...")
    save_to_jsonl(reviews_data, output_file)

    print("Done!")


if __name__ == "__main__":
    main()