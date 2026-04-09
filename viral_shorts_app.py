import streamlit as st
from googleapiclient.discovery import build
import openai

import os

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

def get_trending():
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    req = youtube.videos().list(
        part="snippet",
        chart="mostPopular",
        maxResults=5
    )
    res = req.execute()
    return [i["snippet"]["title"] for i in res["items"]]

def generate(titles):
    prompt = f"Trending videos: {titles}. Make 3 viral shorts ideas with hook, script, and hashtags."
    res = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role":"user","content":prompt}]
    )
    return res.choices[0].message.content

st.title("🔥 Viral Shorts AI")

if st.button("Generate Ideas"):
    titles = get_trending()
    ideas = generate(titles)
    st.write(ideas)
