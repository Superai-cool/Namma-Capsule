import streamlit as st
import openai
import random
from datetime import datetime
import os

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

# App Title
st.title("🗞️ Mana Capsule - Hyderabad Top 10 News")

# User Input
user_input = st.text_input("Ask Mana Capsule", placeholder="Top 10 Hyderabad news today")

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
        st.error("Date parsing failed. Please use the correct format: Top 10 Hyderabad news [Month DD, YYYY]")

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
📰 Source: Name – [Read More](https://example.com)
Sponsor line
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
            st.error(f"Failed to fetch news from OpenAI: {e}")

    else:
        st.error("Please type your question in the correct format: Top 10 Hyderabad news today or Top 10 Hyderabad news [DATE].")
