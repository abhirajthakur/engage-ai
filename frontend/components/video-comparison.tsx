"use client";

import VideoCard from "@/components/video-card";
import { Video } from "@/lib/types";

interface VideoComparisonProps {
  videoA: Video | null;
  videoB: Video | null;
}

export default function VideoComparison({ videoA, videoB }: VideoComparisonProps) {
  return (
    <div className="space-y-4">
      <h2 className="text-lg font-semibold text-foreground">Video Comparison</h2>
      <div className="grid gap-6 md:grid-cols-2">
        <VideoCard video={videoA} label="Video A" />
        <VideoCard video={videoB} label="Video B" />
      </div>
    </div>
  );
}
