import streamlit as st
import openai
import random
from datetime import datetime
import os

# Page config
st.set_page_config(page_title="Mana Capsule - Hyderabad News Bot", page_icon="🗞️", layout="wide")

# Custom full-screen background and sleek UI
st.markdown("""
    <style>
        .stApp {
            background: url("https://images.unsplash.com/photo-1612831455546-74c4643a6e76?auto=format&fit=crop&w=1950&q=80") no-repeat center center fixed;
            background-size: cover;
            font-family: 'Segoe UI', sans-serif;
            color: #ffffff;
        }
        .center-box {
            text-align: center;
            margin-top: 20vh;
        }
        .main-title {
            font-size: 2.5rem;
            font-weight: bold;
            color: white;
            margin-bottom: 0.5rem;
        }
        .subtitle {
            font-size: 1.2rem;
            color: #cccccc;
            margin-bottom: 2rem;
        }
        .news-button {
            background-color: #e53935;
            color: white;
            font-weight: 600;
            font-size: 1.1rem;
            padding: 0.75rem 2rem;
            border-radius: 30px;
            border: none;
            cursor: pointer;
        }
        .news-button:hover {
            background-color: #d32f2f;
        }
        .news-box {
            background-color: rgba(0, 0, 0, 0.7);
            padding: 2rem;
            margin: 2rem auto;
            max-width: 800px;
            border-radius: 20px;
            color: white;
        }
        .source-line, .sponsor-line {
            display: block;
            margin-top: 0.5rem;
            font-size: 0.92rem;
        }
        .source-line {
            color: #90caf9;
        }
        .sponsor-line {
            color: #a5d6a7;
        }
        hr {
            border-top: 1px solid #ffffff33;
            margin: 1.5rem 0;
        }
    </style>
""", unsafe_allow_html=True)

# Secure API key handling
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

# Fixed Categories
categories = [
    "Hyderabad Local News",
    "Politics",
    "Economy/Business",
    "Education",
    "Technology",
    "Health",
    "Environment",
    "Sports",
    "Culture/Entertainment",
    "Infrastructure/Transport"
]

# Sponsor Lines
sponsors = [
    "📣 Fresh Bite | Meal Delivery Service | [WhatsApp : 8830720742](https://wa.link/mwb2hf)",
    "📣 HomeFix | On-Demand Repair Services | [WhatsApp : 8830720742](https://wa.link/mwb2hf)",
    "📣 Skill Spark | Online Learning Platform | [WhatsApp : 8830720742](https://wa.link/mwb2hf)",
    "📣 Fit Nest | Personal Fitness Coaching | [WhatsApp : 8830720742](https://wa.link/mwb2hf)",
    "📣 Triptote | Custom Travel Planning | [WhatsApp : 8830720742](https://wa.link/mwb2hf)",
    "📣 Code Wave | Software Development Agency | [WhatsApp : 8830720742](https://wa.link/mwb2hf)",
    "📣 Zen Space | Interior Design Services | [WhatsApp : 8830720742](https://wa.link/mwb2hf)",
    "📣 Green Grow | Organic Grocery Delivery | [WhatsApp : 8830720742](https://wa.link/mwb2hf)",
    "📣 Care Crew | Elderly Home Care Services | [WhatsApp : 8830720742](https://wa.link/mwb2hf)",
    "📣 Snap Prints | Print-on-Demand Services | [WhatsApp : 8830720742](https://wa.link/mwb2hf)"
]

# UI Header Section
st.markdown("""
    <div class='center-box'>
        <div class='main-title'>📰 Mana Capsule</div>
        <div class='subtitle'>Your daily dose of Hyderabad news, condensed into 10 essential updates.</div>
""", unsafe_allow_html=True)

# Button
get_news = st.button("Tell me Today's Top 10 News", key="today_btn")

st.markdown("</div>", unsafe_allow_html=True)

if get_news:
    query_date = datetime.today()
    shuffled_sponsors = random.sample(sponsors, len(sponsors))
    formatted_date = query_date.strftime('%B %d, %Y')

    prompt = f"""
You are 'Mana Capsule', a hyper-local news summarizer. Provide exactly 10 news summaries for Hyderabad on {formatted_date}.
Categories:
{', '.join(categories)}

Format each summary strictly as follows:
Number. **Category | {formatted_date}**
Summary (within 60 words)
<span class='source-line'>📰 Source: Name – [Read More](https://example.com)</span>
<span class='sponsor-line'>SPONSOR</span>
---
Ensure each category is covered, summaries are concise, factual, strictly under 60 words, and relevant exclusively to Hyderabad.
Sponsor lines (shuffled order):
{shuffled_sponsors}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=1200
        )

        news_summaries = response.choices[0].message.content
        st.markdown(f"<div class='news-box'>{news_summaries}</div>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Failed to fetch news: {e}")
