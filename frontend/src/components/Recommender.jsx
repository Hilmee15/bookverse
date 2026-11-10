import { useState } from "react";
import BookCover from "./BookCover";
import Stars from "./Stars";
import { predict } from "../api";

const EXAMPLES = [
  "a magic school adventure with friendship",
  "detective solving a murder on an island",
  "space survival and problem solving",
  "colonial era indonesia and forbidden love",
];

export default function Recommender({ books, onPredicted }) {
  const [mode, setMode] = useState("title");
  const [query, setQuery] = useState("");
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const inputValue = mode === "title" ? query : text;
  const disabled = loading || inputValue.trim().length < 2;

  async function handleSubmit(e) {
    e.preventDefault();
    if (disabled) return;
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const data = await predict({ query: inputValue.trim(), mode });
      setResult(data);
      onPredicted?.();
    } catch (err) {
      setError(
        err.status === 404
          ? `Book not found: "${inputValue.trim()}". Pick one from the list or switch to description mode.`
          : err.message || "Something went wrong. Is the backend running?"
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    /* dark leather section with the stone-wall texture */
    <section id="recommender" className="stone-wall-dark">
      <div className="mx-auto max-w-6xl px-4 py-16 md:py-20">
        <div className="mb-10 flex items-baseline justify-between border-b border-paper/15 pb-4">
          <div className="flex items-baseline gap-4">
            <span className="text-xs font-medium tabular-nums text-paper/40">02</span>
            <h2 className="font-display text-2xl font-semibold tracking-tight text-paper md:text-3xl">
              Recommendations
            </h2>
          </div>
          <span className="hidden text-[11px] uppercase tracking-[0.18em] text-paper/40 sm:block">
            TF-IDF · cosine similarity
          </span>
        </div>

        <div className="grid gap-12 lg:grid-cols-[400px_1fr]">
          {/* ---------- form ---------- */}
          <div>
            {/* mode switch — plain text tabs */}
            <div className="mb-6 flex gap-6 border-b border-paper/15">
              {[
                ["title", "By a book I liked"],
                ["text", "By description"],
              ].map(([value, label]) => (
                <button
                  key={value}
                  onClick={() => { setMode(value); setResult(null); setError(""); }}
                  className={`-mb-px border-b-2 pb-2.5 text-sm transition ${
                    mode === value
                      ? "border-brass-light font-medium text-paper"
                      : "border-transparent text-paper/50 hover:text-paper/80"
                  }`}
                >
                  {label}
                </button>
              ))}
            </div>

            <form onSubmit={handleSubmit}>
              {mode === "title" ? (
                <div>
                  <label className="mb-2 block text-[13px] text-paper/60">
                    A book or novel you enjoyed
                  </label>
                  <input
                    list="book-titles"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="e.g. The Hobbit, Laskar Pelangi"
                    className="w-full rounded-none border border-paper/25 bg-leather/40 px-3.5 py-2.5 text-[15px] text-paper outline-none transition placeholder:text-paper/30 focus:border-brass-light"
                  />
                  <datalist id="book-titles">
                    {books.map((b) => <option key={b.id} value={b.title} />)}
                  </datalist>
                </div>
              ) : (
                <div>
                  <label className="mb-2 block text-[13px] text-paper/60">
                    What do you feel like reading?
                  </label>
                  <textarea
                    rows={3}
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    placeholder="e.g. an epic war story with dragons and political intrigue"
                    className="w-full resize-none rounded-none border border-paper/25 bg-leather/40 px-3.5 py-2.5 text-[15px] text-paper outline-none transition placeholder:text-paper/30 focus:border-brass-light"
                  />
                  <div className="mt-3 space-y-1.5">
                    {EXAMPLES.map((ex) => (
                      <button
                        key={ex}
                        type="button"
                        onClick={() => setText(ex)}
                        className="block text-left text-[13px] text-paper/45 underline-offset-4 transition hover:text-brass-light hover:underline"
                      >
                        {ex}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              <button
                type="submit"
                disabled={disabled}
                className="mt-8 w-full rounded-none bg-paper py-3 text-sm font-semibold text-ink transition enabled:hover:bg-brass-light disabled:cursor-not-allowed disabled:opacity-40"
              >
                {loading ? "Working…" : "Recommend books"}
              </button>
            </form>

            {error && (
              <p className="mt-4 border-l-2 border-red-400 bg-red-950/40 px-4 py-3 text-[13px] text-red-200">
                {error}
              </p>
            )}
          </div>

          {/* ---------- results ---------- */}
          <div>
            {result ? (
              <>
                <p className="mb-6 flex flex-wrap items-center gap-x-3 gap-y-1 text-[13px] text-paper/60">
                  {result.source?.title
                    ? <>Because you liked <span className="font-medium text-paper">{result.source.title}</span></>
                    : <>Based on <span className="font-medium text-paper">“{result.source.query}”</span></>}
                  {result.cached && (
                    <span className="border border-paper/25 px-1.5 py-0.5 text-[10px] uppercase tracking-[0.14em] text-brass-light">
                      from cache
                    </span>
                  )}
                </p>

                <ol className="divide-y divide-paper/10">
                  {result.recommendations.map((b, i) => (
                    <li key={b.id} className="flex items-center gap-5 py-4">
                      <span className="w-7 shrink-0 text-right font-display text-lg font-semibold tabular-nums text-paper/30">
                        {String(i + 1).padStart(2, "0")}
                      </span>
                      <BookCover book={b} className="h-20 w-14 shrink-0 rounded-sm" />
                      <div className="min-w-0 flex-1">
                        <h3 className="truncate text-[15px] font-semibold text-paper">
                          {b.title}
                        </h3>
                        <p className="mt-0.5 truncate text-[13px] text-paper/50">
                          {b.author} · {b.genre}
                        </p>
                        <div className="mt-1.5 flex items-center gap-2">
                          <Stars value={b.rating} tone="light" />
                          <span className="text-[12px] tabular-nums text-paper/50">
                            {b.rating.toFixed(1)}
                          </span>
                        </div>
                      </div>
                      <div className="w-28 shrink-0">
                        <p className="mb-1 text-right font-display text-lg font-semibold tabular-nums text-brass-light">
                          {Math.round(b.similarity * 100)}%
                        </p>
                        <div className="h-px bg-paper/15">
                          <div
                            className="h-px bg-brass-light transition-all duration-700"
                            style={{ width: `${Math.max(4, Math.round(b.similarity * 100))}%` }}
                          />
                        </div>
                      </div>
                    </li>
                  ))}
                </ol>
              </>
            ) : (
              <div className="flex h-full min-h-[280px] items-center justify-center border border-dashed border-paper/20 p-8">
                <p className="max-w-xs text-center text-[13px] leading-relaxed text-paper/40">
                  Pick a title you enjoyed or describe what you feel like
                  reading — the six closest matches from the catalog will
                  appear here, scored by similarity.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
