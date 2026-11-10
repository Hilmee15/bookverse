import { useState } from "react";
import BookCover from "./BookCover";

export default function Hero({ books, onSearch }) {
  const [q, setQ] = useState("");
  const showcase = [...books].sort((a, b) => b.rating - a.rating).slice(0, 6);

  function submit(e) {
    e.preventDefault();
    onSearch?.(q);
    document.getElementById("browse")?.scrollIntoView({ behavior: "smooth" });
  }

  return (
    <section id="top" className="stone-wall border-b border-line">
      <div className="mx-auto grid max-w-6xl gap-14 px-4 py-16 md:grid-cols-2 md:py-24">
        {/* ---------- Left: headline, search, note ---------- */}
        <div>
          <p className="mb-5 text-[11px] font-medium uppercase tracking-[0.22em] text-fade">
            AI book &amp; novel recommender
          </p>
          <h1 className="font-display text-4xl font-semibold leading-[1.08] tracking-tight text-ink md:text-5xl">
            A library that&apos;s always open for every reader.
          </h1>
          <p className="mt-5 max-w-md text-[15px] leading-relaxed text-fade">
            {books.length || 55} curated books across 11 genres. Search the
            catalog, or let the engine match your taste with TF-IDF similarity.
          </p>

          {/* underline search */}
          <form onSubmit={submit} className="mt-10 flex max-w-md items-end gap-3">
            <input
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder="Search books, authors or topics"
              className="w-full rounded-none border border-line bg-paper px-3.5 py-2.5 text-[15px] text-ink outline-none transition placeholder:text-fade/70 focus:border-ink"
            />
            <button
              type="submit"
              className="shrink-0 rounded-none bg-ink px-5 py-2.5 text-sm font-medium text-paper transition hover:bg-leather"
            >
              Search
            </button>
          </form>

          <p className="mt-8 text-[13px] text-fade/80">
            Read by 500+ readers · covers from Google Books &amp; Open Library
          </p>
        </div>

        {/* ---------- Right: aligned cover grid on the stone wall ---------- */}
        <div className="hidden md:block">
          <div className="grid grid-cols-3 gap-3">
            {showcase.map((b) => (
              <BookCover key={b.id} book={b} className="aspect-[2/3] w-full rounded-sm" />
            ))}
          </div>
          <p className="mt-4 text-right text-[11px] uppercase tracking-[0.18em] text-fade/70">
            Highest rated — from the catalog
          </p>
        </div>
      </div>
    </section>
  );
}
