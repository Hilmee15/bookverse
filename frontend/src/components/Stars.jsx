// Minimal five-star rating: small glyphs, warm monochrome.
// tone="dark" for parchment backgrounds, tone="light" for the leather section.
export default function Stars({ value, tone = "dark", className = "" }) {
  const filled = tone === "dark" ? "text-ink" : "text-paper";
  const empty = tone === "dark" ? "text-line" : "text-paper/25";
  return (
    <span
      className={`inline-flex items-center gap-[2px] ${className}`}
      aria-label={`Rated ${value} out of 5`}
      title={`${value} / 5`}
    >
      {[1, 2, 3, 4, 5].map((i) => (
        <span
          key={i}
          className={`text-[11px] leading-none ${i <= Math.round(value) ? filled : empty}`}
        >
          ★
        </span>
      ))}
    </span>
  );
}
