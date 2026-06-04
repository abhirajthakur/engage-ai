# EngageAI

AI powered creator intelligence platform that compares a YouTube Short and an Instagram Reel, retrieves the most relevant content from both videos, and generates actionable insights using Retrieval Augmented Generation and LangGraph.

## Features

- Compare a YouTube Short against an Instagram Reel
- Extract video metadata and transcripts
- Cache expensive operations
- Chunk and index content into a vector database
- Retrieve relevant evidence for every question
- Maintain conversational memory across turns
- Stream responses using Server Sent Events
- Session persistence using Redis
- Swappable vector store architecture with Chroma and Qdrant support
- Swappable cache architecture with in memory and Redis support

## Architecture

```text
Frontend
    │
    ▼
FastAPI
    │
    ▼
LangGraph
    │
    ├── Session Loading
    ├── Memory Loading
    ├── Retrieval
    └── Prompt Building
    │
    ▼
   LLM
    │
    ▼
Streaming Response
```

### Data Flow

```text
  YouTube Short
  Instagram Reel
       │
       ▼
   Ingestion
       │
       ▼
   Transcript 
       + 
    Metadata
       │
       ▼
    Chunking
       │
       ▼
   Embeddings
       │
       ▼
  Vector Store
       │
       ▼
   Retrieval
       │
       ▼
   LangGraph
       │
       ▼
      LLM
       │
       ▼
 Answer + Sources
```

## Tech Stack

### Backend

- FastAPI
- LangChain + LangGraph
- Sentence Transformers (BGE Small Embeddings)
- Redis
- ChromaDB
- Qdrant
- Pydantic
- uv

### Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS

### AI Models

- Gemini
- Groq
- BGE Small Embeddings
- Faster Whisper

## Project Structure

```text
app
├── api
├── cache
├── core
├── graph
├── ingestion
│   ├── instagram
│   └── youtube
├── llm
├── models
├── retrieval
│   ├── embeddings
│   ├── vectorstores
│   └── chunking
├── schemas
├── services
└── session
```

## Setup

### Clone Repository

```bash
git clone github.com/abhirajthakur/engage-ai.git
cd engage-ai
```

### Backend

```bash
cd backend

uv sync
```

### Environment Variables

Create `.env`

```env
GEMINI_API_KEY=
GROQ_API_KEY=

APIFY_API_TOKEN=

VECTOR_DB=qdrant

CACHE_PROVIDER=redis

REDIS_HOST=localhost
REDIS_PORT=6379

QDRANT_HOST=localhost
QDRANT_PORT=6333
```

## Running Locally

### Redis

```bash
docker run -p 6379:6379 redis:7-alpine
```

### Qdrant

```bash
docker run \
  -p 6333:6333 \
  qdrant/qdrant
```

### Backend

```bash
uvicorn app.main:app --host localhost --port 8000
```

### Frontend

```bash
npm install

npm run dev
```

## API

### Ingest Videos

**POST**

```text
/api/ingest
```

Request:

```json
{
  "youtube_url": "https://www.youtube.com/shorts/abc123",
  "instagram_url": "https://www.instagram.com/reel/xyz123/"
}
```

Response:

```json
{
  "session_id": "uuid",
  "video_a": {
    "external_id": "youtube-id",
    "platform": "youtube",
    "title": "Title",
    "creator": "Creator"
  },
  "video_b": {
    "external_id": "instagram-id",
    "platform": "instagram",
    "title": "Title",
    "creator": "Creator"
  }
}
```

### Chat

**POST**

```text
/api/chat
```

Request:

```json
{
  "session_id": "uuid",
  "message": "Why did video A perform better?"
}
```

Response:

```json
{
  "answer": "Response",
  "sources": [
    {
      "external_id": "video-id",
      "chunk_id": "chunk-id",
      "text": "retrieved text"
    }
  ]
}
```

### Streaming Chat

**POST**

```text
/api/chat/stream
```

Response Type:

```text
text/event-stream
```

Event Types:

```json
{
  "type": "token",
  "content": "Video"
}
```

```json
{
  "type": "sources",
  "sources": []
}
```

```json
{
  "type": "done"
}
```

```json
{
  "type": "error",
  "message": "Something went wrong"
}
```

## Caching Strategy

The cache layer is provider based.

Current providers:

- In Memory Cache
- Redis Cache

Cached operations:

- YouTube metadata
- YouTube transcripts
- Instagram metadata
- Instagram transcripts
- Embeddings
- Sessions
- Conversation memory

Switching providers only requires changing:

```env
CACHE_PROVIDER=redis
```

## Vector Database Strategy

The vector layer is provider based.

Supported providers:

- ChromaDB
- Qdrant

Switching providers only requires changing:

```env
VECTOR_DB=qdrant
```

## LangGraph Workflow

```text
Load Session
      │
      ▼
Load Memory
      │
      ▼
Retrieve Evidence
      │
      ▼
Build Prompt
```

The graph is responsible only for preparing context.

LLM execution happens outside the graph which allows:

- Standard responses
- Streaming responses
- Future model switching

without modifying the graph.

## Source Grounding

Every answer is grounded using retrieved chunks.

Each response returns:

- Video identifier
- Chunk identifier
- Retrieved chunk text

This enables explainability and traceability of generated answers.

## Memory

Conversation history is stored per session.

Each new question includes:

- Previous user messages
- Previous assistant messages

This allows follow up questions and multi turn analysis.

## Scalability

Current architecture supports:

- Redis backed session persistence
- Redis backed conversation memory
- Swappable vector databases
- Streaming responses
- Async ingestion
- Concurrent external API calls

For larger workloads:

- Run multiple FastAPI containers
- Place Redis behind all application instances
- Use managed Qdrant or a dedicated Qdrant cluster
- Add background workers for transcription

