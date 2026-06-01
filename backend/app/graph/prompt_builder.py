from app.models.video import VideoData


def build_prompt(
    *,
    query: str,
    video_a: VideoData,
    video_b: VideoData,
    transcript_context: str,
    conversation_history: str,
) -> str:
    """
    Build EngageAI prompt.
    """

    return f"""
You are EngageAI. You compare short-form videos.

Video A Details:
Title: {video_a.title}
Creator: {video_a.creator}
Views: {video_a.views}
Likes: {video_a.likes}
Comments: {video_a.comments}
Engagement Rate: {video_a.engagement_rate}

Video B Details:
Title: {video_b.title}
Creator: {video_b.creator}
Views: {video_b.views}
Likes: {video_b.likes}
Comments: {video_b.comments}
Engagement Rate: {video_b.engagement_rate}

---

Transcript Context
{transcript_context}

Conversation History
{conversation_history}

Question
{query}

---

Instructions:
- Use metadata when answering metric questions.
- Use transcript context when answering content questions.
- Use both when answering comparison questions.
- If information is unavailable, say so.
- Be concise and specific.
"""
