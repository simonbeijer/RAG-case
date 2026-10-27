"use client";

import { useEffect, useRef, useState, type FormEvent } from "react";
import { useSearchParams } from "next/navigation";
import Message, { type ChatMessage } from "@/components/Message";
import { sendQuestion } from "@/lib/api";

const suggestions = [
  "Vilka branscher jobbar ni med?",
  "Hur kontaktar man er?",
  "Sammanfatta ”Om oss”",
];

export default function Chat() {
  const searchParams = useSearchParams();
  const [threadId] = useState(() => crypto.randomUUID());
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const sentQuery = useRef(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  const canSend = input.trim() !== "" && !isStreaming;

  // Copy the last message (the answer) and change it, so React sees a new object.
  function updateAnswer(change: (answer: ChatMessage) => ChatMessage) {
    setMessages((prev) => [...prev.slice(0, -1), change(prev[prev.length - 1])]);
  }

  async function send(question: string) {
    question = question.trim();
    if (!question || isStreaming) return;

    setMessages((prev) => [
      ...prev,
      { role: "user", text: question, sources: [] },
      { role: "assistant", text: "", sources: [] },
    ]);
    setIsStreaming(true);

    await sendQuestion(question, threadId, {
      onToken: (text) => updateAnswer((a) => ({ ...a, text: a.text + text })),
      onSource: (source) => updateAnswer((a) => ({ ...a, sources: [...a.sources, source] })),
      onError: (message) => updateAnswer((a) => ({ ...a, error: message })),
    });

    setIsStreaming(false);
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!canSend) return;
    send(input);
    setInput("");
  }

  // StrictMode runs effects twice in dev. The ref makes sure ?q= is sent once.
  useEffect(() => {
    const query = searchParams.get("q");
    if (query && !sentQuery.current) {
      sentQuery.current = true;
      send(query);
    }
  }, [searchParams]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ block: "end" });
  }, [messages]);

  return (
    <section className="flex flex-1 flex-col overflow-clip rounded-[28px] bg-white shadow-[0_12px_32px_rgba(11,13,23,0.06)]">
      <main className="flex flex-1 flex-col gap-6 px-[clamp(16px,4vw,48px)] py-8">
        {messages.map((message, index) => (
          <Message key={index} message={message} />
        ))}
      </main>

      <footer className="sticky bottom-0 flex flex-col gap-2.5 border-t border-line bg-white px-[clamp(16px,4vw,48px)] pt-4 pb-5">
        <div className="flex flex-wrap gap-2">
          {suggestions.map((suggestion) => (
            <button
              key={suggestion}
              type="button"
              onClick={() => setInput(suggestion)}
              className="min-h-9 cursor-pointer rounded-full bg-canvas px-3.5 py-1.5 text-[13px] font-medium"
            >
              {suggestion}
            </button>
          ))}
        </div>

        <form
          onSubmit={handleSubmit}
          className="flex items-center gap-2 rounded-t-[18px] rounded-b-[5px] border-b-2 border-accent bg-canvas py-2 pr-2 pl-5"
        >
          <label htmlFor="chat-input" className="sr-only">
            Din fråga
          </label>
          <input
            id="chat-input"
            type="text"
            value={input}
            onChange={(event) => setInput(event.target.value)}
            placeholder="Fråga något mer…"
            className="h-12 min-w-0 flex-1 bg-transparent text-[17px] outline-none"
          />
          <button
            type="submit"
            disabled={!canSend}
            className="flex h-12 cursor-pointer items-center gap-2 rounded-xl bg-ink px-5 font-semibold text-white disabled:cursor-not-allowed disabled:opacity-40"
          >
            Fråga
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.25" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
              <path d="M5 12h14M13 6l6 6-6 6" />
            </svg>
          </button>
        </form>
      </footer>
      <div ref={bottomRef} />
    </section>
  );
}
