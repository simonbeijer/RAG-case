import Sources, { type Source } from "@/components/Sources";
import Feedback from "@/components/Feedback";

export type ChatMessage = {
  role: "user" | "assistant";
  text: string;
  sources: Source[];
  error?: string;
};

export default function Message({ message }: { message: ChatMessage }) {
  if (message.role === "user") {
    return (
      <div className="max-w-[75%] self-end rounded-[18px_18px_4px_18px] bg-accent px-4 py-3 font-medium text-white">
        {message.text}
      </div>
    );
  }

  const paragraphs = message.text ? message.text.split("\n\n") : [];
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
          {paragraphs.map((paragraph, index) => (
            <p key={index}>{paragraph}</p>
          ))}
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
