import { useEffect, useState } from "react";
import Navbar from "./components/Navbar.jsx";
import Hero from "./components/Hero.jsx";
import Shortlist from "./components/Shortlist.jsx";
import Recommender from "./components/Recommender.jsx";
import BookGrid from "./components/BookGrid.jsx";
import History from "./components/History.jsx";
import Footer from "./components/Footer.jsx";
import { fetchBooks } from "./api";

export default function App() {
  const [books, setBooks] = useState([]);
  const [genres, setGenres] = useState([]);
  const [error, setError] = useState("");
  const [historyKey, setHistoryKey] = useState(0);
  const [search, setSearch] = useState("");

  useEffect(() => {
    fetchBooks()
      .then((data) => {
        setBooks(data.books);
        setGenres(data.genres);
      })
      .catch((err) => setError(err.message || "Failed to load catalog"));
  }, []);

  return (
    <div className="min-h-screen bg-paper font-sans text-ink antialiased">
      <Navbar />
      <main>
        {error ? (
          <div className="mx-auto max-w-xl px-4 py-32 text-center">
            <h1 className="font-display text-2xl font-semibold text-ink">
              Backend not reachable
            </h1>
            <p className="mt-2 text-sm text-neutral-500">
              {error} — start the stack with{" "}
              <code className="bg-neutral-100 px-1.5 py-0.5 text-[13px]">
                docker compose up -d --build
              </code>{" "}
              and reload.
            </p>
          </div>
        ) : (
          <>
            <Hero books={books} onSearch={setSearch} />
            <Shortlist books={books} />
            <Recommender books={books} onPredicted={() => setHistoryKey((k) => k + 1)} />
            <BookGrid books={books} genres={genres} search={search} onSearch={setSearch} />
            <History refreshKey={historyKey} />
          </>
        )}
      </main>
      <Footer />
    </div>
  );
}
