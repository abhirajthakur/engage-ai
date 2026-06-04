import { IngestResponse, ChatResponse, SourceCitation } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

/**
 * Ingest YouTube Short and Instagram Reel URLs
 * Creates a comparison session and returns video data
 */
export async function ingestVideos(
  youtubeUrl: string,
  instagramUrl: string,
): Promise<IngestResponse> {
  const response = await fetch(`${API_BASE_URL}/api/ingest`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      youtube_url: youtubeUrl,
      instagram_url: instagramUrl,
    }),
  });

  const res = await response.json();

  console.log("Ingest response:", res);

  if (!response.ok) {
    throw new Error(res.detail || "Failed to ingest videos");
  }

  return res;
}

/**
 * Send a chat message to the backend
 * Returns AI response with sources
 */
export async function chat(sessionId: string, message: string): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE_URL}/api/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      session_id: sessionId,
      message: message,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to send message");
  }

  return response.json();
}

type ChatStreamEvent =
  | { type: "token"; content: string }
  | { type: "sources"; sources: SourceCitation[] }
  | { type: "done" }
  | { type: "error"; message: string };

/**
 * Stream chat response from backend using Server-Sent Events (SSE)
 * Handles token, sources, done, and error events
 */
export async function streamChat(
  sessionId: string,
  message: string,
  handlers: {
    onToken: (token: string) => void;
    onSources: (sources: SourceCitation[]) => void;
    onError: (error: string) => void;
  },
): Promise<void> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/chat/stream`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        session_id: sessionId,
        message: message,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Failed to stream chat");
    }

    const reader = response.body?.getReader();
    if (!reader) {
      throw new Error("No response body");
    }

    const decoder = new TextDecoder();
    let buffer = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop() || ""; // Keep the last incomplete line in buffer

      for (const line of lines) {
        if (!line.startsWith("data: ")) continue;

        const dataStr = line.slice(6); // Remove 'data: ' prefix
        try {
          const event: ChatStreamEvent = JSON.parse(dataStr);

          switch (event.type) {
            case "token":
              handlers.onToken(event.content);
              break;
            case "sources":
              handlers.onSources(event.sources);
              break;
            case "done":
              // Generation complete
              break;
            case "error":
              handlers.onError(event.message);
              break;
          }
        } catch (e) {
          console.warn("Failed to parse SSE event:", dataStr, e);
        }
      }
    }

    // Flush remaining buffer if it exists
    if (buffer.startsWith("data: ")) {
      const dataStr = buffer.slice(6);
      try {
        const event: ChatStreamEvent = JSON.parse(dataStr);
        if (event.type === "sources") {
          handlers.onSources(event.sources);
        } else if (event.type === "error") {
          handlers.onError(event.message);
        }
      } catch (e) {
        console.warn("Failed to parse final SSE event:", dataStr, e);
      }
    }
  } catch (error) {
    // Fallback to regular chat if streaming fails
    console.warn("Streaming failed, falling back to regular chat:", error);
    const chatResponse = await chat(sessionId, message);
    handlers.onToken(chatResponse.answer);
    handlers.onSources(chatResponse.sources);
  }
}
