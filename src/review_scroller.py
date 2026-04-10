"""Allows it to be much nicer to scroll through a whole bunch of reviews"""

import json
from pathlib import Path
import tkinter as tk


def load_reviews(path):
    reviews = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            reviews.append(json.loads(line.strip()))
    return reviews


class ReviewViewer:
    def __init__(self, root, reviews):
        self.root = root
        self.reviews = reviews
        self.index = 0

        root.title("Review Viewer")

        # Review ID label
        self.id_label = tk.Label(root, text="", font=("Arial", 10))
        self.id_label.pack(pady=2)

        # Author label
        self.author_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
        self.author_label.pack(pady=5)

        # Review text box
        self.text = tk.Text(root, wrap="word", height=15, width=70)
        self.text.pack(padx=10, pady=10)

        # Navigation buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        self.prev_button = tk.Button(button_frame, text="⬅ Previous", command=self.prev_review)
        self.prev_button.pack(side="left", padx=10)

        self.next_button = tk.Button(button_frame, text="Next ➡", command=self.next_review)
        self.next_button.pack(side="left", padx=10)

        self.display_review()

    def display_review(self):
        review = self.reviews[self.index]

        # ID
        self.id_label.config(text=f"ID: {review.get('reviewId', 'Unknown')}")

        # Author
        self.author_label.config(text=f"User: {review.get('userName', 'Unknown')}")

        # Content
        content = review.get("content", "")

        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, content)

        self.root.title(f"Review {self.index + 1} / {len(self.reviews)}")

    def next_review(self):
        if self.index < len(self.reviews) - 1:
            self.index += 1
            self.display_review()

    def prev_review(self):
        if self.index > 0:
            self.index -= 1
            self.display_review()


def main():
    project_root = Path(__file__).resolve().parents[1]
    file_path = project_root / "data" / "reviews_human_readable.jsonl"

    reviews = load_reviews(file_path)

    root = tk.Tk()
    app = ReviewViewer(root, reviews)
    root.mainloop()


if __name__ == "__main__":
    main()