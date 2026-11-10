import BookCover from "./BookCover";
import Stars from "./Stars";

// "The Shortlist" — ranked editorial list (01–10) with hairline dividers.
export default function Shortlist({ books }) {
  const ranked = [...books].sort((a, b) => b.rating - a.rating).slice(0, 10);

  return (
    <section id="shortlist" className="bg-paper">
      <div className="mx-auto max-w-6xl px-4 py-16 md:py-20">
        <div className="mb-8 flex items-baseline justify-between border-b border-line pb-4">
          <div className="flex items-baseline gap-4">
            <span className="text-xs font-medium tabular-nums text-fade/70">01</span>
            <h2 className="font-display text-2xl font-semibold tracking-tight text-ink md:text-3xl">
              The Shortlist
            </h2>
          </div>
          <a
            href="#browse"
            className="text-sm text-fade underline-offset-4 transition hover:text-ink hover:underline"
          >
            View the catalog
          </a>
        </div>

        <ol className="divide-y divide-line">
          {ranked.map((b, i) => (
            <li
              key={b.id}
              className="group flex items-center gap-5 py-4 transition-colors hover:bg-vellum/60"
            >
              <span className="w-8 shrink-0 text-right font-display text-xl font-semibold tabular-nums text-line transition-colors group-hover:text-brass">
                {String(i + 1).padStart(2, "0")}
              </span>

              <BookCover book={b} className="h-20 w-14 shrink-0 rounded-sm" />

              <div className="min-w-0 flex-1">
                <h3 className="truncate text-[15px] font-semibold text-ink">
                  {b.title}
                </h3>
                <p className="mt-0.5 truncate text-[13px] text-fade">
                  {b.author} · {b.year}
                </p>
              </div>

              <div className="hidden shrink-0 sm:block">
                <span className="text-[11px] font-medium uppercase tracking-[0.16em] text-fade/70">
                  {b.genre}
                </span>
              </div>

              <div className="flex shrink-0 items-center gap-2">
                <Stars value={b.rating} />
                <span className="text-[13px] font-medium tabular-nums text-fade">
                  {b.rating.toFixed(1)}
                </span>
              </div>
            </li>
          ))}
        </ol>
      </div>
    </section>
  );
}
