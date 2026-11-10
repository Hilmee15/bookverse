export default function Navbar() {
  return (
    <header className="sticky top-0 z-50 border-b border-line bg-paper">
      <nav className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
        <a href="#top" className="font-display text-xl font-bold tracking-tight text-ink">
          BookVerse
        </a>

        <div className="hidden items-center gap-8 text-sm text-fade md:flex">
          <a href="#shortlist" className="transition hover:text-ink">Shortlist</a>
          <a href="#recommender" className="transition hover:text-ink">Recommend</a>
          <a href="#browse" className="transition hover:text-ink">Catalog</a>
          <a href="#history" className="transition hover:text-ink">History</a>
        </div>

        <a
          href="#recommender"
          className="rounded-none bg-ink px-4 py-2 text-sm font-medium text-paper transition hover:bg-leather"
        >
          Get a recommendation
        </a>
      </nav>
    </header>
  );
}
