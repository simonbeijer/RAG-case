import Link from "next/link";

const starters = [
  { label: "Tjänster", question: "Vad erbjuder ni för typer av AI-tjänster?" },
  { label: "Kunder", question: "Vilka branscher jobbar ni med?" },
  { label: "Kontakt", question: "Hur kontaktar man er, och var sitter ni?" },
  {
    label: "Om oss",
    question: "Sammanfatta ”Om oss” i tre punkter och länka källan",
    dark: true,
  },
];

export default function HomePage() {
  return (
    <main className="flex flex-col gap-5">
      <section className="flex flex-col gap-7 rounded-[28px] bg-accent px-6 pt-12 pb-8 text-white sm:px-12 sm:pt-16 sm:pb-12">
        <h1 className="max-w-[14ch] font-display text-[clamp(36px,5vw,64px)] leading-[1.02] font-semibold tracking-[-0.035em]">
          Vad vill du veta om Compileit?
        </h1>
        <p className="max-w-[52ch] text-[17px] text-accent-soft">
          Jag svarar på svenska utifrån det som står på compileit.com och visar
          alltid källan. Står det inte där, säger jag det.
        </p>

        {/* Skickar till /chat?q=... */}
        <form
          action="/chat"
          className="flex max-w-[760px] items-center gap-2 rounded-[18px] bg-white py-2 pr-2 pl-5 shadow-[0_12px_32px_rgba(11,13,23,0.18)]"
        >
          <label htmlFor="question" className="sr-only">
            Din fråga
          </label>
          <input
            id="question"
            name="q"
            type="text"
            placeholder="Skriv en fråga…"
            className="h-12 min-w-0 flex-1 bg-transparent text-[17px] text-ink outline-none"
          />
          <button
            type="submit"
            className="flex h-12 cursor-pointer items-center gap-2 rounded-xl bg-ink px-5 font-semibold text-white"
          >
            Fråga
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.25" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
              <path d="M5 12h14M13 6l6 6-6 6" />
            </svg>
          </button>
        </form>
      </section>

      <section className="flex flex-col gap-3 p-2">
        <h2 className="text-[13px] font-semibold tracking-[0.06em] text-muted uppercase">
          Börja här
        </h2>
        <div className="flex flex-wrap gap-3">
          {starters.map((starter) => (
            <Link
              key={starter.label}
              href={`/chat?q=${encodeURIComponent(starter.question)}`}
              className={`flex min-h-[120px] flex-[1_1_220px] flex-col justify-between gap-4 rounded-[18px] p-[18px] ${
                starter.dark ? "bg-ink text-white" : "bg-white text-ink"
              }`}
            >
              <span
                className={`font-display text-[13px] font-semibold ${
                  starter.dark ? "text-lavender" : "text-accent"
                }`}
              >
                {starter.label}
              </span>
              <span className="font-medium">{starter.question}</span>
            </Link>
          ))}
        </div>
      </section>
    </main>
  );
}
