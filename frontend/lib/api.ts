import type { Source } from "@/components/Sources";

type Callbacks = {
  onToken: (text: string) => void;
  onSource: (source: Source) => void;
  onError: (message: string) => void;
};

// POST, so EventSource (GET only) does not work. We read the SSE stream ourselves.
export async function sendQuestion(
  question: string,
  threadId: string,
  callbacks: Callbacks,
): Promise<void> {
  try {
    const response = await fetch(process.env.NEXT_PUBLIC_API_URL + "/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, thread_id: threadId }),
    });
    if (!response.ok || !response.body) {
      callbacks.onError("Kunde inte skicka frågan. Försök igen.");
      return;
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });

      // An event ends with a blank line. Keep the last, maybe unfinished, part.
      const events = buffer.split("\n\n");
      buffer = events.pop() ?? "";

      for (const event of events) {
        let name = "";
        let data = "";
        for (const line of event.split("\n")) {
          if (line.startsWith("event: ")) name = line.slice(7);
          if (line.startsWith("data: ")) data = line.slice(6);
        }
        if (!data) continue;
        const payload = JSON.parse(data);

        if (name === "token") callbacks.onToken(payload.text);
        if (name === "source") callbacks.onSource(payload);
        if (name === "error") callbacks.onError(payload.message);
      }
    }
  } catch {
    callbacks.onError("Kunde inte nå servern. Försök igen.");
  }
}
