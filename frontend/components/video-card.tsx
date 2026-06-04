"use client";

import { Badge } from "@/components/ui/badge";
import { Video } from "@/lib/types";
import { formatMetricCount } from "@/lib/utils";
import { Eye, MessageCircle, ThumbsUp } from "lucide-react";
import Image from "next/image";
import { useState } from "react";

interface VideoCardProps {
  video: Video | null;
  label: string;
}

export default function VideoCard({ video, label }: VideoCardProps) {
  const platformLabel = video?.platform === "youtube" ? "YouTube Short" : "Instagram Reel";
  const platformColor =
    video?.platform === "youtube" ? "bg-red-500/10 text-red-600" : "bg-pink-500/10 text-pink-600";
  const [isTranscriptExpanded, setIsTranscriptExpanded] = useState(false);

  if (!video) {
    return (
      <div className="rounded-lg border border-border bg-card/50 p-6">
        <div className="flex h-40 items-center justify-center rounded-lg bg-muted/20">
          <p className="text-sm text-muted-foreground">No video data</p>
        </div>
      </div>
    );
  }

  return (
    <div
      id={`video-${video.external_id}`}
      className="rounded-lg border border-border bg-card overflow-hidden"
    >
      {/* Header with Platform Badge */}
      <div className="relative h-40">
        {video.thumbnail_url ? (
          <Image
            src={video.thumbnail_url}
            alt={`${video.title} thumbnail`}
            className="absolute inset-0 h-full w-full object-cover"
            crossOrigin="anonymous"
            referrerPolicy="no-referrer"
            style={{ 
              objectPosition: video.platform === 'instagram' ? 'bottom center' : 'center' 
            }}
            onError={(e) => {
              console.error("Failed to load thumbnail:", e);
            }}
          />
        ) : (
          <div className="absolute inset-0 bg-linear-to-br from-muted to-muted/50" />
        )}
        <div className="absolute top-3 left-3">
          <Badge className={`${platformColor} border-0`}>{platformLabel}</Badge>
        </div>
      </div>

      {/* Content */}
      <div className="p-4 space-y-4">
        {/* Title and Creator */}
        <div>
          <p className="text-xs text-muted-foreground mb-1">{label}</p>
          <h3 className="font-semibold text-foreground line-clamp-2">{video.title}</h3>
          <p className="text-sm text-muted-foreground mt-1">{video.creator}</p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-3">
          <div className="rounded bg-muted/50 p-2">
            <div className="flex items-center gap-1 text-xs text-muted-foreground mb-1">
              <Eye className="h-3 w-3" />
              Views
            </div>
            <p className="font-semibold text-sm text-foreground">
              {formatMetricCount(video.views)}
            </p>
          </div>

          <div className="rounded bg-muted/50 p-2">
            <div className="flex items-center gap-1 text-xs text-muted-foreground mb-1">
              <ThumbsUp className="h-3 w-3" />
              Likes
            </div>
            <p className="font-semibold text-sm text-foreground">
              {formatMetricCount(video.likes)}
            </p>
          </div>

          <div className="rounded bg-muted/50 p-2">
            <div className="flex items-center gap-1 text-xs text-muted-foreground mb-1">
              <MessageCircle className="h-3 w-3" />
              Comments
            </div>
            <p className="font-semibold text-sm text-foreground">
              {formatMetricCount(video.comments)}
            </p>
          </div>
        </div>

        {/* Description */}
        {video.description && (
          <p className="text-xs text-muted-foreground line-clamp-2">{video.description}</p>
        )}

        {/* Transcript */}
        {video.transcript && (
          <div className="rounded bg-muted/30 p-3">
            <p className="text-xs font-medium text-muted-foreground mb-2">Transcript</p>
            <p className={`text-xs text-foreground ${!isTranscriptExpanded ? "line-clamp-3" : ""}`}>
              {video.transcript}
            </p>
            <button
              onClick={() => setIsTranscriptExpanded(!isTranscriptExpanded)}
              className="mt-2 text-xs font-medium text-muted-foreground hover:text-foreground"
            >
              {isTranscriptExpanded ? "Show less" : "Show full transcript"}
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
