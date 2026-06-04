"use client";

import ChatPanel from "@/components/chat-panel";
import Header from "@/components/header";
import PerformanceMetrics from "@/components/performance-metrics";
import VideoCard from "@/components/video-card";
import VideoIngestionForm from "@/components/video-ingestion-form";
import { ingestVideos, streamChat } from "@/lib/api";
import { ChatMessage, SourceCitation, Video } from "@/lib/types";
import { useState } from "react";

export default function Dashboard() {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [videoA, setVideoA] = useState<Video | null>(null);
  const [videoB, setVideoB] = useState<Video | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "1",
      role: "assistant",
      content: "Hi! I'm EngageAI. Paste two video URLs and I'll help you compare them.",
    },
  ]);

  const handleCompare = async (youtubeUrl: string, instagramUrl: string) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await ingestVideos(youtubeUrl, instagramUrl);
      setSessionId(response.session_id);
      setVideoA(response.video_a);
      setVideoB(response.video_b);

      // Reset messages for new comparison
      setMessages([
        {
          id: "1",
          role: "assistant",
          content: "Great! I've analyzed both videos. What would you like to know about them?",
        },
      ]);
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : "Failed to analyze videos";
      setError(errorMessage);
      console.error("Error comparing videos:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = async (content: string) => {
    if (!sessionId) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: "user",
      content,
    };

    setMessages((prev) => [...prev, userMessage]);

    // Create placeholder for assistant message
    const assistantId = (Date.now() + 1).toString();
    const assistantMessage: ChatMessage = {
      id: assistantId,
      role: "assistant",
      content: "",
      sources: [],
    };

    setMessages((prev) => [...prev, assistantMessage]);

    try {
      // Stream response with SSE events
      await streamChat(sessionId, content, {
        onToken: (token: string) => {
          setMessages((prev) =>
            prev.map((msg) =>
              msg.id === assistantId ? { ...msg, content: msg.content + token } : msg,
            ),
          );
        },
        onSources: (sources: SourceCitation[]) => {
          if (sources && sources.length > 0) {
            setMessages((prev) =>
              prev.map((msg) => (msg.id === assistantId ? { ...msg, sources } : msg)),
            );
          }
        },
        onError: (errorMsg: string) => {
          setMessages((prev) =>
            prev.map((msg) =>
              msg.id === assistantId ? { ...msg, content: `Error: ${errorMsg}` } : msg,
            ),
          );
        },
      });
    } catch (error) {
      console.error("Error sending message:", error);
      const errorMsg = error instanceof Error ? error.message : "Failed to get response";
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === assistantId ? { ...msg, content: `Error: ${errorMsg}` } : msg,
        ),
      );
    }
  };

  return (
    <main className="min-h-screen bg-background">
      <Header />
      <div className="grid gap-8 px-6 py-8 lg:grid-cols-3">
        {/* Main Content */}
        <div className="space-y-8 lg:col-span-2">
          {/* Video Ingestion */}
          <VideoIngestionForm onCompare={handleCompare} isLoading={isLoading} />

          {/* Error Display */}
          {error && (
            <div className="rounded-lg border border-destructive/50 bg-destructive/10 p-4">
              <p className="text-sm text-destructive">{error}</p>
            </div>
          )}

          {/* Video Comparison - Only show after successful ingestion */}
          {videoA && videoB && (
            <>
              <div className="space-y-4">
                <h2 className="text-lg font-semibold text-foreground">Video Comparison</h2>
                <div className="grid gap-6 md:grid-cols-2">
                  <VideoCard video={videoA} label="Video A" />
                  <VideoCard video={videoB} label="Video B" />
                </div>
              </div>

              {/* Performance Metrics - Only show after successful ingestion */}
              <PerformanceMetrics videoA={videoA} videoB={videoB} />
            </>
          )}
        </div>

       {/* Chat Panel */}
       <div className="h-fit">
         <ChatPanel messages={messages} onSendMessage={handleSendMessage} disabled={!sessionId} videoA={videoA} videoB={videoB} />
       </div>
      </div>
    </main>
  );
}
