// Video data types
export interface Video {
  external_id: string;
  platform: string;
  title: string;
  creator: string;
  description: string;
  transcript: string;
  views?: number;
  likes?: number;
  comments?: number;
  thumbnail_url?: string;
}

export interface VideoData {
  external_id: string;
  platform: string;
  title: string | null;
  creator: string | null;
  creator_id: string | null;
  follower_count: number | null;
  views: number | null;
  likes: number | null;
  comments: number | null;
  engagement_rate: number | null;
  duration: number | null;
  upload_date: string | null;
  hashtags: string[];
  description: string | null;
  thumbnail_url: string | null;
  transcript: string;
}

// API request/response types
export interface CompareRequest {
  video_a_url: string;
  video_b_url: string;
}

export interface IngestResponse {
  session_id: string;
  video_a: Video;
  video_b: Video;
}

export interface CompareResponse {
  session_id: string;
  video_a: VideoData;
  video_b: VideoData;
  hook_analysis: HookAnalysis;
}

export interface ChatRequest {
  session_id: string;
  message: string;
}

export interface ChatResponse {
  answer: string;
  sources: SourceCitation[];
}

// Chat and analysis types
export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: SourceCitation[];
}

export interface SourceCitation {
  external_id: string;
  chunk_id: string;
  text: string;
  platform: string;
  title: string;
  creator: string;
}

export interface HookAnalysis {
  video_a_hook: string;
  video_b_hook: string;
  summary: string;
}

// Comparison progress types
export type ComparisonStage =
  | "fetching_metadata"
  | "extracting_transcripts"
  | "generating_embeddings"
  | "indexing_content"
  | "building_comparison";

export interface ProgressState {
  stage: ComparisonStage;
  status: "pending" | "running" | "completed";
}
