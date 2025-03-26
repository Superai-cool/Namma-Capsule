""import streamlit as st
import openai
import random
from datetime import datetime
import os

# Page config
st.set_page_config(page_title="Mana Capsule - Hyderabad News Bot", page_icon="🗞️", layout="wide")

# Custom styles for clean news card format
st.markdown("""
    <style>
        .stApp {
            font-family: 'Segoe UI', sans-serif;
            background: #ffffff;
            color: #111827;
        }
        .news-card {
            background-color: #f9fafb;
            padding: 1.5rem;
            margin: 1.5rem auto;
            border-radius: 1rem;
            max-width: 800px;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.05);
        }
        .news-card h3 {
            margin: 0.5rem 0;
            font-size: 1.25rem;
        }
        .news-card p {
            font-size: 1rem;
            line-height: 1.5;
            margin-bottom: 0.5rem;
        }
        .category-label {
            background-color: #e5e7eb;
            padding: 0.25rem 0.75rem;
            border-radius: 999px;
            font-size: 0.85rem;
            display: inline-block;
            margin-bottom: 0.25rem;
        }
        .news-date {
            font-size: 0.875rem;
            color: #6b7280;
            text-align: right;
        }
        .source-line, .sponsor-line {
            display: block;
            font-size: 0.875rem;
            margin-top: 0.25rem;
        }
        .source-line {
            color: #1d4ed8;
        }
        .sponsor-line {
            color: #16a34a;
        }
        hr {
            border-top: 1px solid #e5e7eb;
            margin: 1rem 0;
        }
    </style>
""", unsafe_allow_html=True)

# API Key
openai.api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")

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

# Header
st.markdown("""
    <div style='text-align: center; padding-top: 3rem;'>
        <h1 style='font-size: 2.5rem; font-weight: 700;'>📰 Mana Capsule</h1>
        <p style='color: #374151;'>Top 10 Hyderabad News</p>
    </div>
""", unsafe_allow_html=True)

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
📰 Source: Name – [Read More](https://example.com)
📣 SPONSOR
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

        summaries = response.choices[0].message.content

        # Render cleanly
        st.markdown(f"""
        <div class='news-card'>
            <div class='category-label'>Hyderabad</div>
            <div class='news-date'>{formatted_date}</div>
            {summaries}
        </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Failed to fetch news: {e}")
