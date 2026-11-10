import { useState } from "react";

// Typographic placeholder used when no public cover exists:
// flat vellum card with hairline border — no gradients, no icons.
function PlaceholderCover({ book }) {
  return (
    <div
      className="absolute inset-0 flex flex-col justify-between border border-line bg-vellum p-3"
      aria-hidden="true"
    >
      <span className="text-[9px] font-medium uppercase tracking-[0.18em] text-fade/70">
        {book.genre}
      </span>
      <span className="font-display text-base font-semibold leading-tight text-ink">
        {book.title}
      </span>
      <span className="text-[9px] font-medium uppercase tracking-[0.14em] text-fade/70">
        {book.author}
      </span>
    </div>
  );
}

// Real cover image (hyperlinked from the Google Books / Open Library CDN);
// falls back to the typographic placeholder if the image cannot load.
export default function BookCover({ book, className = "" }) {
  const [failed, setFailed] = useState(false);
  const showImage = Boolean(book.cover_url) && !failed;

  return (
    <div
      className={`relative overflow-hidden bg-vellum ${className}`}
      aria-label={`Cover of ${book.title}`}
    >
      {showImage ? (
        <img
          src={book.cover_url}
          alt={`Cover of ${book.title}`}
          loading="lazy"
          onError={() => setFailed(true)}
          className="absolute inset-0 h-full w-full object-cover"
        />
      ) : (
        <PlaceholderCover book={book} />
      )}
    </div>
  );
}
