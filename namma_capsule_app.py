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
            margin-top: 0.5rem;
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
        .center-btn {
            text-align: center;
            margin-top: 1rem;
        }
        .center-btn button {
            background-color: #dc2626;
            color: white;
            font-size: 1.1rem;
            font-weight: bold;
            padding: 0.75rem 2rem;
            border: none;
            border-radius: 999px;
            cursor: pointer;
        }
        .center-btn button:hover {
            background-color: #b91c1c;
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

# Button-based trigger
st.markdown("<div class='center-btn'>", unsafe_allow_html=True)
trigger_today = st.button("Tell me Today's Top 10 News")
st.markdown("</div>", unsafe_allow_html=True)

if trigger_today:
    query_date = datetime.today()
    formatted_date = query_date.strftime('%B %d, %Y')
    shuffled_sponsors = random.sample(sponsors, len(sponsors))

    prompt = f"""
You are 'Mana Capsule', a hyper-local news summarizer exclusively focused on delivering the Top 10 daily news summaries relevant to Hyderabad, across 10 fixed categories. You include national or global developments only when directly connected to one of these categories with a clear Hyderabad angle.

Respond only in this format:
1. **Category | {formatted_date}**\nSummary (within 60 words)\n\n📰 Source: Name – [Read More](https://example.com)\n\n📣 Sponsor line\n\n---

Always include all 10 fixed categories. Ensure all summaries are factual, crisp, markdown compatible, and follow this exact template.
Use one sponsor per item (shuffled):
{shuffled_sponsors}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=1600
        )

        summaries = response.choices[0].message.content
        st.markdown(f"<div class='news-card'><div class='news-date'>{formatted_date}</div>{summaries}</div>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Failed to fetch news: {e}")
