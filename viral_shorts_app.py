import os
import streamlit as st
from googleapiclient.discovery import build
import openai

# -------------------------
# Read API keys from Streamlit secrets
# -------------------------
# Make sure these are set in your Secrets/Environment Variables
YOUTUBE_API_KEY = st.secrets["YOUTUBE_API_KEY"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# -------------------------
# Initialize clients
# -------------------------
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
openai.api_key = OPENAI_API_KEY

# -------------------------
# Functions
# -------------------------
def get_trending_videos(limit=5):
    """Fetch trending YouTube video titles safely."""
    try:
        request = youtube.videos().list(
            part="snippet",
            chart="mostPopular",
            maxResults=limit
        )
        response = request.execute()
        return [video['snippet']['title'] for video in response['items']]
    except Exception as e:
        st.error(f"Failed to fetch trending videos: {e}")
        return []

def generate_ai_ideas(prompt):
    """Generate AI content using OpenAI."""
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=100
        )
        return response.choices[0].text.strip()
    except Exception as e:
        st.error(f"Failed to generate AI ideas: {e}")
        return ""

# -------------------------
# Streamlit UI
# -------------------------
st.title("Viral Shorts AI — Fixed Version")

st.header("Trending YouTube Videos")
trending = get_trending_videos()
for idx, title in enumerate(trending, start=1):
    st.write(f"{idx}. {title}")

st.header("AI Video Ideas")
user_prompt = st.text_input(
    "Enter a prompt for AI ideas:", 
    "Give me 3 trending short video ideas for YouTube"
)
if st.button("Generate Ideas"):
    ideas = generate_ai_ideas(user_prompt)
    st.write(ideas)
