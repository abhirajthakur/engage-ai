"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Link2, Loader2 } from "lucide-react";
import { useState } from "react";

interface VideoIngestionFormProps {
  onCompare: (videoAUrl: string, videoBUrl: string) => void;
  isLoading?: boolean;
}

export default function VideoIngestionForm({
  onCompare,
  isLoading = false,
}: VideoIngestionFormProps) {
  const [videoAUrl, setVideoAUrl] = useState("");
  const [videoBUrl, setVideoBUrl] = useState("");

  const handleCompare = () => {
    if (videoAUrl.trim() && videoBUrl.trim()) {
      onCompare(videoAUrl, videoBUrl);
      setVideoAUrl("");
      setVideoBUrl("");
    }
  };

  return (
    <div className="rounded-lg border border-border bg-card p-6">
      <div className="mb-4 flex items-center gap-2">
        <Link2 className="h-5 w-5 text-accent" />
        <h2 className="text-lg font-semibold text-foreground">Compare Videos</h2>
      </div>

       <div className="grid gap-4 md:grid-cols-2">
         {/* Video A */}
         <div className="space-y-3">
           <label className="block text-sm font-medium text-foreground">
             Video A URL (YouTube Short)
           </label>
           <Input
             placeholder="https://youtube.com/watch?v=..."
             value={videoAUrl}
             onChange={(e) => setVideoAUrl(e.target.value)}
             disabled={isLoading}
             className="bg-input text-foreground placeholder:text-muted-foreground"
           />
         </div>

         {/* Video B */}
         <div className="space-y-3">
           <label className="block text-sm font-medium text-foreground">
             Video B URL (Instagram Reel)
           </label>
           <Input
             placeholder="https://instagram.com/p/..."
             value={videoBUrl}
             onChange={(e) => setVideoBUrl(e.target.value)}
             disabled={isLoading}
             className="bg-input text-foreground placeholder:text-muted-foreground"
           />
         </div>
       </div>

      <div className="mt-6">
        <Button
          onClick={handleCompare}
          disabled={!videoAUrl.trim() || !videoBUrl.trim() || isLoading}
          size="lg"
          className="w-full bg-accent text-accent-foreground font-bold text-base hover:bg-accent/90 hover:shadow-lg active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer transition-all shadow-lg border border-accent/50"
        >
          {isLoading ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Analyzing Videos...
            </>
          ) : (
            "Analyze Videos"
          )}
        </Button>
      </div>

      <p className="mt-4 text-xs text-muted-foreground">
        Paste YouTube or Instagram video URLs to compare engagement metrics and get AI-powered
        insights.
      </p>
    </div>
  );
}
