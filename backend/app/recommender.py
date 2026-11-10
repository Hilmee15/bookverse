"""Content-based book recommender: TF-IDF + cosine similarity (scikit-learn, CPU-only).

Each book is turned into a document built from its genre (repeated to weigh it
higher), author and description. The recommender then compares:

* title mode -> the user picks a book they liked; we compare that book's
  TF-IDF vector against every other book,
* text mode  -> the user types free-text preferences; we vectorize that text
  and match it against the whole catalog.
"""
from __future__ import annotations

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class BookRecommender:
    def __init__(self) -> None:
        self._vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self._matrix = None
        self._books: list[dict] = []

    # ------------------------------------------------------------------ fit
    def fit(self, books: list[dict]) -> None:
        """Build the TF-IDF matrix from the catalog (called at startup)."""
        self._books = books
        # Genre repeated 3x so genre similarity dominates a bit more.
        corpus = [
            f"{b['genre']} {b['genre']} {b['genre']} {b['description']} {b['author']}"
            for b in books
        ]
        self._matrix = self._vectorizer.fit_transform(corpus)

    # -------------------------------------------------------------- helpers
    def _package(self, index: int, score: float) -> dict:
        b = self._books[index]
        return {
            "id": b["id"],
            "title": b["title"],
            "author": b["author"],
            "genre": b["genre"],
            "year": b["year"],
            "rating": b["rating"],
            "cover_url": b.get("cover_url"),
            "similarity": round(float(score), 4),
        }

    def _top_indices(self, sims, top_n: int, exclude: int | None = None) -> list[int]:
        if exclude is not None:
            sims = sims.copy()
            sims[exclude] = -1.0  # never recommend the input book itself
        return sims.argsort()[::-1][:top_n]

    # ----------------------------------------------------------- public API
    def find_book(self, query: str) -> dict | None:
        """Case-insensitive substring match on title."""
        q = query.strip().lower()
        for b in self._books:
            if q in b["title"].lower():
                return b
        return None

    def recommend_from_title(self, title: str, top_n: int = 6) -> dict | None:
        source = self.find_book(title)
        if source is None:
            return None
        idx = next(i for i, b in enumerate(self._books) if b["id"] == source["id"])
        sims = cosine_similarity(self._matrix[idx], self._matrix).flatten()
        return {
            "source": source,
            "recommendations": [self._package(i, sims[i]) for i in self._top_indices(sims, top_n, exclude=idx)],
        }

    def recommend_from_text(self, text: str, top_n: int = 6) -> dict:
        vec = self._vectorizer.transform([text.strip()])
        sims = cosine_similarity(vec, self._matrix).flatten()
        return {
            "source": {"query": text.strip()},
            "recommendations": [self._package(i, sims[i]) for i in self._top_indices(sims, top_n)],
        }


# Singleton used by the FastAPI app
recommender = BookRecommender()
