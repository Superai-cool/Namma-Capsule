import streamlit as st
import openai
import random
from datetime import datetime
import os

# Page config
st.set_page_config(page_title="Mana Capsule - Hyderabad News Bot", page_icon="🗞️", layout="wide")

# Tailwind-style-inspired HTML for UI rendering
st.markdown("""
    <style>
        .stApp {
            background: black;
            font-family: 'Segoe UI', sans-serif;
        }
        .main-container {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }
        .box {
            text-align: center;
            padding: 2rem;
        }
        .news-button {
            margin-top: 1.5rem;
            background-color: #dc2626;
            color: white;
            font-weight: 600;
            font-size: 1.1rem;
            padding: 0.75rem 2rem;
            border-radius: 9999px;
            border: none;
            box-shadow: 0 4px 10px rgba(0,0,0,0.4);
            cursor: pointer;
            transition: 0.3s ease;
        }
        .news-button:hover {
            background-color: #b91c1c;
        }
        .news-box {
            background-color: rgba(0, 0, 0, 0.85);
            padding: 2rem;
            margin: 2rem auto;
            max-width: 800px;
            border-radius: 20px;
            color: white;
        }
        .source-line {
            color: #90caf9;
            margin-top: 0.5rem;
        }
        .sponsor-line {
            color: #a5d6a7;
            margin-top: 0.25rem;
        }
        hr {
            border-top: 1px solid #ffffff33;
            margin: 1.5rem 0;
        }
    </style>

    <div class='main-container'>
      <div class='box'>
        <div style='font-size: 2.5rem;'>📰</div>
        <h1 style='font-size: 2rem; font-weight: bold;'>Mana Capsule</h1>
        <p style='color: #ccc; font-size: 1.1rem; margin-top: 1rem;'>
          Your daily dose of Hyderabad news, condensed<br>
          into 10 essential updates.
        </p>
      </div>
    </div>
""", unsafe_allow_html=True)

# API Key
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

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

# Button Logic
if st.button("Tell me Today’s Top 10 News", key="today_btn"):
    query_date = datetime.today()
    formatted_date = query_date.strftime('%B %d, %Y')
    shuffled_sponsors = random.sample(sponsors, len(sponsors))

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
