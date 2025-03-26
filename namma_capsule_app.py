import streamlit as st
import openai
import random
from datetime import datetime
import os

# Page config
st.set_page_config(page_title="Mana Capsule - Hyderabad News Bot", page_icon="🗞️", layout="centered")

# Enhanced CSS for mobile-friendly styling
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(to right, #e3f2fd, #fce4ec);
            font-family: 'Segoe UI', sans-serif;
        }
        .chat-container {
            background-color: white;
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            max-width: 95%;
            width: 700px;
            margin: 2rem auto;
            border: 1px solid #e0e0e0;
        }
        .chat-header {
            font-size: 1.8rem;
            font-weight: 700;
            text-align: center;
            margin-bottom: 1.5rem;
            color: #0d47a1;
        }
        .stTextInput>div>div>input {
            padding: 1rem;
            border-radius: 10px;
            border: 1px solid #bdbdbd;
            background-color: #f9f9f9;
        }
        .stMarkdown p {
            font-size: 1rem;
            line-height: 1.6;
        }
        .source-line, .sponsor-line {
            display: block;
            margin-top: 0.5rem;
            font-size: 0.92rem;
        }
        .source-line {
            color: #0d47a1;
        }
        .sponsor-line {
            color: #2e7d32;
        }
        hr {
            margin-top: 1.5rem;
            margin-bottom: 1.5rem;
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

# Chat UI container
with st.container():
    st.markdown("""<div class='chat-container'>""", unsafe_allow_html=True)
    st.markdown("<div class='chat-header'>🤖 Mana Capsule - Your Hyderabad News Bot</div>", unsafe_allow_html=True)
    user_input = st.text_input("", placeholder="Top 10 Hyderabad news today", label_visibility="collapsed")

    if user_input:
        valid_today = user_input.strip().lower() == "top 10 hyderabad news today"
        valid_date_format = False
        query_date = None

        try:
            if valid_today:
                query_date = datetime.today()
                valid_date_format = True
            elif "top 10 hyderabad news" in user_input.lower():
                date_part = user_input.lower().replace("top 10 hyderabad news", "").strip()
                query_date = datetime.strptime(date_part, "%B %d, %Y")
                valid_date_format = True
        except Exception as e:
            st.error("⚠️ Date parsing failed. Use format: Top 10 Hyderabad news [Month DD, YYYY]")

        if valid_today or valid_date_format:
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
                st.markdown(news_summaries, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ Failed to fetch news: {e}")

        else:
            st.warning("⚠️ Use correct format: Top 10 Hyderabad news today or Top 10 Hyderabad news [DATE].")
    st.markdown("""</div>""", unsafe_allow_html=True)
