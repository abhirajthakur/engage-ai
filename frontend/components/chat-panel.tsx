"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ChatMessage, Video } from "@/lib/types";
import { Lightbulb, Send } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface ChatPanelProps {
  messages: ChatMessage[];
  onSendMessage: (message: string) => void;
  disabled?: boolean;
  videoA?: Video | null;
  videoB?: Video | null;
}

const suggestedQuestions = [
  "Why did Video A outperform Video B?",
  "What's the engagement rate of each?",
  "Compare the hooks in the first 5 seconds.",
  "Suggest improvements for Video B.",
  "Who is the creator of Video B?",
];

export default function ChatPanel({ messages, onSendMessage, disabled = false }: ChatPanelProps) {
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesContainerRef = useRef<HTMLDivElement>(null);
  const [expandedSources, setExpandedSources] = useState<Map<string, boolean>>(new Map());

  useEffect(() => {
    if (messagesContainerRef.current) {
      const { scrollTop, scrollHeight, clientHeight } = messagesContainerRef.current;
      // If user is within 100px of bottom, scroll to bottom
      if (scrollHeight - scrollTop - clientHeight < 100) {
        messagesContainerRef.current.scrollTo({
          top: scrollHeight,
          behavior: "smooth",
        });
      }
    }
  }, [messages]);

  const handleSend = () => {
    if (input.trim()) {
      setIsLoading(true);
      onSendMessage(input);
      setInput("");
      setTimeout(() => setIsLoading(false), 2000);
    }
  };

  const handleSuggestedQuestion = (question: string) => {
    setIsLoading(true);
    onSendMessage(question);
    setTimeout(() => setIsLoading(false), 2000);
  };

  const handleSourceClick = (externalId: string) => {
    const videoCardEl = document.getElementById(`video-${externalId}`);
    if (videoCardEl) {
      videoCardEl.scrollIntoView({ behavior: "smooth", block: "nearest" });
      videoCardEl.style.boxShadow = "0 0 0 2px rgb(59 130 246)";
      setTimeout(() => {
        videoCardEl.style.boxShadow = "";
      }, 1500);
    }
  };

  const toggleSources = (messageId: string) => {
    setExpandedSources((prev) => {
      const newMap = new Map(prev);
      const isExpanded = newMap.get(messageId) || false;
      newMap.set(messageId, !isExpanded);
      return newMap;
    });
  };

  return (
    <div className="flex h-150 flex-col rounded-lg border border-border bg-card">
      {/* Header */}
      <div className="border-b border-border px-4 py-3">
        <h3 className="text-sm font-semibold text-foreground">EngageAI Assistant</h3>
        <p className="text-xs text-muted-foreground">Powered by advanced analytics</p>
      </div>

      {/* Messages */}
      <div ref={messagesContainerRef} className="flex-1 space-y-3 overflow-y-auto p-4">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full text-center">
            <p className="text-sm text-muted-foreground">Start a conversation</p>
          </div>
        ) : (
          messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
            >
              <div
                className={`max-w-xs rounded-lg px-3 py-2 text-sm ${
                  msg.role === "user"
                    ? "bg-accent text-accent-foreground"
                    : "bg-secondary text-secondary-foreground"
                }`}
              >
                <div className="leading-relaxed">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>{msg.content}</ReactMarkdown>
                  {msg.role === "assistant" && isLoading && (
                    <span className="ml-1 animate-pulse inline-block h-3 w-1 rounded bg-current"></span>
                  )}
                </div>
                {msg.sources && msg.sources.length > 0 && (
                  <div className="mt-3 space-y-3 pt-2 border-t border-current/10">
                    <div className="flex items-center justify-between mb-2">
                      <p className="text-xs font-medium text-muted-foreground">Sources:</p>
                      <button
                        onClick={() => toggleSources(msg.id)}
                        className="text-xs font-medium text-muted-foreground hover:text-foreground"
                      >
                        {expandedSources.get(msg.id) ? "Hide sources" : "Show sources"}
                      </button>
                    </div>
                    {expandedSources.get(msg.id) && (
                      <div className="mt-2">
                        <div className="flex flex-wrap gap-2">
                          {msg.sources.map((source) => (
                            <div
                              key={`${source.external_id}-${source.chunk_id}`}
                              onClick={() => handleSourceClick(source.external_id)}
                              className="cursor-pointer rounded-lg border border-current/20 px-3 py-2 text-xs flex items-center gap-2 hover:border-current/40 transition-colors"
                              title={source.text}
                            >
                              <div className="flex-1">
                                <div className="flex flex-wrap gap-2">
                                  <span className="font-semibold">{source.platform}</span>
                                  <span className="text-current/60">•</span>
                                  <span className="text-xs font-medium">{source.creator}</span>
                                </div>
                                {source.title && (
                                  <div className="mt-1">
                                    <p className="text-xs text-current/60 line-clamp-2">
                                      {source.title}
                                    </p>
                                  </div>
                                )}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          ))
        )}
      </div>

      {/* Suggested Questions */}
      {messages.length <= 1 && !isLoading && !disabled && (
        <div className="border-t border-border px-4 py-3">
          <p className="mb-2 text-xs text-muted-foreground flex items-center gap-1">
            <Lightbulb className="h-3 w-3" />
            Try asking:
          </p>
          <div className="flex flex-wrap gap-2">
            {suggestedQuestions.map((question) => (
              <button
                key={question}
                onClick={() => handleSuggestedQuestion(question)}
                className="rounded-full border border-border bg-secondary/50 px-3 py-1 text-xs text-muted-foreground hover:bg-secondary hover:text-foreground transition-colors"
              >
                {question}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input */}
      <div className="border-t border-border p-3">
        {disabled ? (
          <p className="text-xs text-muted-foreground text-center">
            Submit videos to start chatting
          </p>
        ) : (
          <div className="flex gap-2">
            <Input
              placeholder="Ask a question about Video A and Video B..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
              disabled={isLoading}
              className="bg-input text-foreground placeholder:text-muted-foreground"
            />
            <Button
              size="sm"
              onClick={handleSend}
              disabled={!input.trim() || isLoading}
              className="shrink-0"
            >
              <Send className="h-4 w-4" />
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}

