'use client';

import { Video } from '@/lib/types';
import { formatMetricCount } from '@/lib/utils';
import { TrendingDown, TrendingUp } from 'lucide-react';

interface PerformanceMetricsProps {
  videoA: Video;
  videoB: Video;
}

export default function PerformanceMetrics({ videoA, videoB }: PerformanceMetricsProps) {
  const calculateEngagementRate = (video: Video) => {
    if (!video.views || !video.likes || !video.comments) return 0;
    return ((video.likes + video.comments) / video.views) * 100;
  };

  const engagementA = calculateEngagementRate(videoA);
  const engagementB = calculateEngagementRate(videoB);
  const engagementDiff = engagementB - engagementA;

  const viewsDiff = videoA.views && videoB.views ? 
    ((videoB.views - videoA.views) / videoA.views) * 100 : 0;
  const likesDiff = videoA.likes && videoB.likes ? 
    ((videoB.likes - videoA.likes) / videoA.likes) * 100 : 0;
  const commentsDiff = videoA.comments && videoB.comments ? 
    ((videoB.comments - videoA.comments) / videoA.comments) * 100 : 0;

  return (
    <div className="space-y-4">
      <h2 className="text-lg font-semibold text-foreground">Performance Analysis</h2>
      <div className="grid gap-4 md:grid-cols-4">
        <MetricCard
          label="Engagement Rate"
          videoAValue={engagementA.toFixed(2) + '%'}
          videoBValue={engagementB.toFixed(2) + '%'}
          difference={engagementDiff}
          winner={engagementB > engagementA ? 'B' : engagementA > engagementB ? 'A' : null}
        />
        <MetricCard
          label="Views"
          videoAValue={formatMetricCount(videoA.views)}
          videoBValue={formatMetricCount(videoB.views)}
          difference={viewsDiff}
          winner={videoB.views && videoA.views && videoB.views > videoA.views ? 'B' : videoA.views && videoB.views && videoA.views > videoB.views ? 'A' : null}
        />
        <MetricCard
          label="Likes"
          videoAValue={formatMetricCount(videoA.likes)}
          videoBValue={formatMetricCount(videoB.likes)}
          difference={likesDiff}
          winner={videoB.likes && videoA.likes && videoB.likes > videoA.likes ? 'B' : videoA.likes && videoB.likes && videoA.likes > videoB.likes ? 'A' : null}
        />
        <MetricCard
          label="Comments"
          videoAValue={formatMetricCount(videoA.comments)}
          videoBValue={formatMetricCount(videoB.comments)}
          difference={commentsDiff}
          winner={videoB.comments && videoA.comments && videoB.comments > videoA.comments ? 'B' : videoA.comments && videoB.comments && videoA.comments > videoB.comments ? 'A' : null}
        />
      </div>
    </div>
  );
}

interface MetricCardProps {
  label: string;
  videoAValue: string;
  videoBValue: string;
  difference: number;
  winner: 'A' | 'B' | null;
}

function MetricCard({ label, videoAValue, videoBValue, difference, winner }: MetricCardProps) {
  const isPositive = difference > 0;

  return (
    <div className="rounded-lg border border-border bg-card p-4">
      <p className="mb-3 text-sm font-medium text-muted-foreground">{label}</p>

      <div className="space-y-3">
        <div className={winner === 'A' ? 'bg-accent/20 rounded px-2 py-1' : ''}>
          <p className="text-xs text-muted-foreground">Video A</p>
          <p className="text-lg font-semibold text-foreground">{videoAValue}</p>
        </div>

        <div className="border-t border-border pt-3">
          <div className={winner === 'B' ? 'bg-accent/20 rounded px-2 py-1' : ''}>
            <p className="text-xs text-muted-foreground">Video B</p>
            <p className="text-lg font-semibold text-foreground">{videoBValue}</p>
          </div>
        </div>

        <div
          className={`flex items-center justify-between rounded px-2 py-1 text-xs ${
            isPositive ? 'bg-accent/20 text-accent' : 'bg-destructive/20 text-destructive'
          }`}
        >
          <div className="flex items-center gap-1">
            {isPositive ? (
              <TrendingUp className="h-3 w-3" />
            ) : (
              <TrendingDown className="h-3 w-3" />
            )}
            <span className="font-medium">
              {isPositive ? '+' : ''}{Math.abs(difference).toFixed(1)}%
            </span>
          </div>
          <span className="font-medium">Winner: {winner || '-'}</span>
        </div>
      </div>
    </div>
  );
}

