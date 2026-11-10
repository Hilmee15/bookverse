import { useMemo, useState } from "react";
import BookCover from "./BookCover";
import Stars from "./Stars";

export default function BookGrid({ books, genres, search, onSearch }) {
  const [genre, setGenre] = useState("");

  const filtered = useMemo(() => {
    const q = (search || "").trim().toLowerCase();
    return books.filter(
      (b) =>
        (!genre || b.genre === genre) &&
        (!q || b.title.toLowerCase().includes(q) || b.author.toLowerCase().includes(q))
    );
  }, [books, search, genre]);

  return (
    <section id="browse" className="bg-paper">
      <div className="mx-auto max-w-6xl px-4 py-16 md:py-20">
        <div className="mb-8 flex items-baseline justify-between border-b border-line pb-4">
          <div className="flex items-baseline gap-4">
            <span className="text-xs font-medium tabular-nums text-fade/70">03</span>
            <h2 className="font-display text-2xl font-semibold tracking-tight text-ink md:text-3xl">
              Catalog
            </h2>
          </div>
          <p className="text-sm tabular-nums text-fade">
            {filtered.length} / {books.length} books
          </p>
        </div>

        {/* filters: search + genre chips, square and flat */}
        <div className="mb-10 flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
          <input
            value={search}
            onChange={(e) => onSearch(e.target.value)}
            placeholder="Search title or author"
            className="w-full rounded-none border border-line bg-paper px-3.5 py-2 text-sm text-ink outline-none transition placeholder:text-fade/70 focus:border-ink lg:w-72"
          />
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => setGenre("")}
              className={`rounded-none px-3.5 py-1.5 text-[13px] transition ${
                genre === ""
                  ? "bg-ink font-medium text-paper"
                  : "border border-line text-fade hover:border-ink hover:text-ink"
              }`}
            >
              All
            </button>
            {genres.map((g) => (
              <button
                key={g}
                onClick={() => setGenre(g)}
                className={`rounded-none px-3.5 py-1.5 text-[13px] transition ${
                  genre === g
                    ? "bg-ink font-medium text-paper"
                    : "border border-line text-fade hover:border-ink hover:text-ink"
                }`}
              >
                {g}
              </button>
            ))}
          </div>
        </div>

        <div className="grid gap-x-6 gap-y-10 sm:grid-cols-2 lg:grid-cols-4">
          {filtered.map((b) => (
            <article key={b.id} className="group">
              <BookCover
                book={b}
                className="aspect-[2/3] w-full rounded-sm ring-1 ring-inset ring-line transition group-hover:ring-brass"
              />
              <div className="mt-3">
                <h3 className="text-[15px] font-semibold leading-snug text-ink">
                  {b.title}
                </h3>
                <p className="mt-0.5 text-[13px] text-fade">
                  {b.author} · {b.year}
                </p>
                <div className="mt-1.5 flex items-center gap-2">
                  <Stars value={b.rating} />
                  <span className="text-[12px] font-medium tabular-nums text-fade">
                    {b.rating.toFixed(1)}
                  </span>
                  <span className="ml-auto text-[10px] font-medium uppercase tracking-[0.16em] text-fade/70">
                    {b.genre}
                  </span>
                </div>
                <p className="mt-2 line-clamp-2 text-[13px] leading-relaxed text-fade/90">
                  {b.description}
                </p>
              </div>
            </article>
          ))}
        </div>

        {filtered.length === 0 && (
          <div className="border border-dashed border-line py-16 text-center">
            <p className="text-sm text-fade">
              No books match “{search}”{genre && ` in ${genre}`} — try another keyword.
            </p>
          </div>
        )}
      </div>
    </section>
  );
}
