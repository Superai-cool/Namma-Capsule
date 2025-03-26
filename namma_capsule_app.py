import streamlit as st
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

query = st.text_input("Ask Mana Capsule", placeholder="Top 10 Hyderabad news today")

valid_today = "top 10 hyderabad news today"
valid_date_format = "top 10 hyderabad news "

if query:
    q_lower = query.lower().strip()
    if q_lower == valid_today or (q_lower.startswith(valid_date_format) and len(q_lower.split()) >= 5):
        try:
            # Parse date if provided
            if q_lower == valid_today:
                query_date = datetime.today()
            else:
                try:
                    date_str = query[len(valid_date_format):].strip()
                    query_date = datetime.strptime(date_str, "%B %d, %Y")
                except ValueError:
                    st.error("Please enter the date in the format: Top 10 Hyderabad news March 25, 2025")
                    st.stop()

            formatted_date = query_date.strftime('%B %d, %Y')
            shuffled_sponsors = random.sample(sponsors, len(sponsors))

            prompt = f"""
You are 'Mana Capsule', a hyper-local news summarizer exclusively focused on delivering the Top 10 daily news summaries relevant to Hyderabad, across 10 fixed categories. You include national or global developments only when directly connected to one of these categories with a clear Hyderabad angle.

Generate exactly 10 concise news summaries, each belonging to one of the following 10 fixed categories:
{', '.join(categories)}

Each summary must:
- Begin with a number 1–10, followed by the category and full date in this format:
  1. **Category | {formatted_date}**
- Be concise, factual, and no longer than 60 words
- Always include this source line:
  📰 Source: Name – [Read More](https://example.com)
- End with a sponsor line (randomized from below)
- Separated by a horizontal divider (---)

Sponsor lines:
{shuffled_sponsors}

Mandatory rules:
- No missing categories. If no fresh news is available, include a throwback, explainer, past feature, or upcoming event related to Hyderabad for that category.
- Never exceed 60 words per summary.
- All links must be in markdown and open in a new tab.
- Never summarize or include news from outside Hyderabad unless clearly relevant.
- Do not perform any other tasks—only return news in required format.
- Final format strictly as:
  Number. **Category | Full Date**
  Summary (max 60 words)
  📰 Source: Name – [Read More](https://example.com)
  📣 Sponsor line
  ---
Ensure all summaries are cleanly rendered.
"""

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=1500
            )

            summaries = response.choices[0].message.content
            st.markdown(f"<div class='news-card'><div class='news-date'>{formatted_date}</div>{summaries}</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Failed to fetch news: {e}")
    else:
        st.warning("Please type your question in the correct format: Top 10 Hyderabad news today or Top 10 Hyderabad news [DATE].")
