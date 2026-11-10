import { useEffect, useState } from "react";
import { fetchHistory } from "../api";

function fmtTime(iso) {
  const d = new Date(iso);
  return d.toLocaleString("en-GB", {
    day: "2-digit", month: "short",
    hour: "2-digit", minute: "2-digit", second: "2-digit",
  });
}

export default function History({ refreshKey }) {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let alive = true;
    fetchHistory()
      .then((data) => alive && setItems(data.items))
      .catch(() => alive && setItems([]))
      .finally(() => alive && setLoading(false));
    return () => { alive = false; };
  }, [refreshKey]);

  return (
    <section id="history" className="border-t border-line bg-vellum/60">
      <div className="mx-auto max-w-6xl px-4 py-16 md:py-20">
        <div className="mb-8 flex items-baseline justify-between border-b border-line pb-4">
          <div className="flex items-baseline gap-4">
            <span className="text-xs font-medium tabular-nums text-fade/70">04</span>
            <h2 className="font-display text-2xl font-semibold tracking-tight text-ink md:text-3xl">
              History
            </h2>
          </div>
          <span className="hidden text-[11px] uppercase tracking-[0.18em] text-fade/70 sm:block">
            Stored in PostgreSQL
          </span>
        </div>

        {loading ? (
          <div className="divide-y divide-line">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="h-14 animate-pulse bg-paper/70" />
            ))}
          </div>
        ) : items.length === 0 ? (
          <div className="border border-dashed border-line py-14 text-center">
            <p className="text-sm text-fade">
              Nothing here yet — ask for a recommendation above.
            </p>
          </div>
        ) : (
          <ul className="divide-y divide-line">
            {items.map((h) => (
              <li
                key={h.id}
                className="flex flex-col gap-2 py-4 md:flex-row md:items-center md:justify-between"
              >
                <div className="flex min-w-0 items-baseline gap-3">
                  <span className="shrink-0 text-[10px] font-semibold uppercase tracking-[0.16em] text-fade/70">
                    {h.mode}
                  </span>
                  <p className="truncate text-[14px] text-ink">
                    “{h.query}”
                    <span className="mx-2 text-brass">→</span>
                    <span className="font-medium text-fade">
                      {h.results?.[0]?.title ?? "—"}
                    </span>
                    {h.results?.length > 1 && (
                      <span className="ml-1.5 text-[12px] text-fade/60">
                        +{h.results.length - 1}
                      </span>
                    )}
                  </p>
                </div>
                <time className="shrink-0 font-mono text-[11px] text-fade/60 md:text-right">
                  {fmtTime(h.created_at)}
                </time>
              </li>
            ))}
          </ul>
        )}
      </div>
    </section>
  );
}
