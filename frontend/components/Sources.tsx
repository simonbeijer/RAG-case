export type Source = { url: string; title: string };

// "https://www.compileit.com/om-oss" → "compileit.com/om-oss"
function displayUrl(url: string) {
  const { host, pathname } = new URL(url);
  return host.replace(/^www\./, "") + pathname;
}

export default function Sources({ sources }: { sources: Source[] }) {
  const [first, ...rest] = sources;

  return (
    <div className="flex flex-col gap-2.5 rounded-[18px] bg-canvas p-3.5">
      <span className="text-xs font-semibold tracking-[0.06em] text-muted uppercase">
        Källor
      </span>

      <a
        href={first.url}
        target="_blank"
        rel="noopener noreferrer"
        className="flex min-h-[52px] items-center gap-3 rounded-xl bg-white px-3 py-2.5"
      >
        <span className="flex size-6 flex-none items-center justify-center rounded-lg bg-accent text-xs font-semibold text-white">
          1
        </span>
        <span className="flex min-w-0 flex-1 flex-col">
          <span className="font-semibold">Kolla den här källan</span>
          <span className="text-[13px] break-words text-muted">
            {first.title} · {displayUrl(first.url)}
          </span>
        </span>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.25" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <path d="M7 17L17 7M8 7h9v9" />
        </svg>
      </a>

      {rest.map((source, index) => (
        <a
          key={index}
          href={source.url}
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-3 px-3 text-[13px] text-muted underline"
        >
          <span className="w-6 flex-none text-center font-semibold no-underline">
            {index + 2}
          </span>
          <span className="min-w-0 break-words">{displayUrl(source.url)}</span>
        </a>
      ))}
    </div>
  );
}
