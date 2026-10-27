import Markdown, { type Components } from "react-markdown";
import Sources, { type Source } from "@/components/Sources";
import Feedback from "@/components/Feedback";

export type ChatMessage = {
  role: "user" | "assistant";
  text: string;
  sources: Source[];
  error?: string;
};

// Tailwind styles for the markdown in answers. Raw HTML is not rendered.
const markdownComponents: Components = {
  p: ({ children }) => <p>{children}</p>,
  strong: ({ children }) => <strong className="font-semibold">{children}</strong>,
  ul: ({ children }) => <ul className="flex list-disc flex-col gap-1 pl-5">{children}</ul>,
  ol: ({ children }) => <ol className="flex list-decimal flex-col gap-1 pl-5">{children}</ol>,
  a: ({ href, children }) => (
    <a href={href} target="_blank" rel="noopener noreferrer" className="text-accent underline">
      {children}
    </a>
  ),
};

export default function Message({ message }: { message: ChatMessage }) {
  if (message.role === "user") {
    return (
      <div className="max-w-[75%] self-end rounded-[18px_18px_4px_18px] bg-accent px-4 py-3 font-medium text-white">
        {message.text}
      </div>
    );
  }

  const isThinking = !message.text && !message.error;

  return (
    <article className="flex max-w-[720px] gap-3.5 self-start">
      <span
        aria-hidden="true"
        className="flex size-9 flex-none items-center justify-center rounded-xl bg-ink font-display text-[15px] font-bold text-white"
      >
        c<span className="text-lavender">.</span>
      </span>

      <div className="flex min-w-0 flex-col gap-3.5">
        <div className="flex flex-col gap-2.5">
          {isThinking && <p className="text-muted">Tänker…</p>}
          <Markdown components={markdownComponents}>{message.text}</Markdown>
        </div>
        {message.error && (
          <p role="alert" className="rounded-xl bg-red-50 px-3.5 py-2.5 font-medium text-red-700">
            {message.error}
          </p>
        )}
        {message.sources.length > 0 && <Sources sources={message.sources} />}
        {message.text && <Feedback />}
      </div>
    </article>
  );
}
