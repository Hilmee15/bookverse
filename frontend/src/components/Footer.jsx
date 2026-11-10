export default function Footer() {
  return (
    <footer className="stone-wall-dark">
      <div className="mx-auto flex max-w-6xl flex-col gap-2 px-4 py-10 text-center md:flex-row md:items-baseline md:justify-between md:text-left">
        <p className="font-display text-lg font-semibold text-paper">BookVerse</p>
        <p className="text-[13px] text-paper/50">
          React · FastAPI · scikit-learn · PostgreSQL · Redis · Docker Compose
        </p>
        <p className="text-[12px] text-paper/35">
          UTS COMP6991031 — Cloud Computing · runs on localhost
        </p>
      </div>
    </footer>
  );
}
