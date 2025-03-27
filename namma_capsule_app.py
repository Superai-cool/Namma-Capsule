import streamlit as st
import openai
import random
from datetime import datetime

# 1. Check if 'openai_api_key' is in st.secrets
if "openai_api_key" not in st.secrets:
    st.error("❌ OpenAI API key is missing. Please add 'openai_api_key' to Streamlit secrets and re-run.")
    st.stop()

# 2. Set OpenAI API key
openai.api_key = st.secrets["openai_api_key"]

# Title
st.title("🗞️ Namma Capsule - Top 10 Bangalore News")

# User input
user_input = st.text_input("Enter your query:")

# Sponsor lines
sponsor_lines = [
    "📣 Fresh Bite | Meal Delivery Service | WhatsApp : 8830720742",
    "📣 HomeFix | On-Demand Repair Services | WhatsApp : 8830720742",
    "📣 Skill Spark | Online Learning Platform | WhatsApp : 8830720742",
    "📣 Fit Nest | Personal Fitness Coaching | WhatsApp : 8830720742",
    "📣 Triptote | Custom Travel Planning | WhatsApp : 8830720742",
    "📣 Code Wave | Software Development Agency | WhatsApp : 8830720742",
    "📣 Zen Space | Interior Design Services | WhatsApp : 8830720742",
    "📣 Green Grow | Organic Grocery Delivery | WhatsApp : 8830720742",
    "📣 Care Crew | Elderly Home Care Services | WhatsApp : 8830720742",
    "📣 Snap Prints | Print-on-Demand Services | WhatsApp : 8830720742",
]

# Define categories
categories = [
    "Bangalore Local News",
    "Politics",
    "Economy/Business",
    "Education",
    "Technology",
    "Health",
    "Environment",
    "Sports",
    "Culture/Entertainment",
    "Infrastructure/Transport",
]

# Function to validate input
def validate_input(input_text):
    if input_text.strip().lower() == "top 10 bangalore news today":
        return datetime.today().strftime("%B %d, %Y")
    try:
        prefix = "top 10 bangalore news "
        if input_text.strip().lower().startswith(prefix):
            date_str = input_text[len(prefix):]
            date_obj = datetime.strptime(date_str, "%B %d, %Y")
            return date_obj.strftime("%B %d, %Y")
    except:
        return None
    return None

# GPT Prompt builder
def build_prompt(valid_date):
    prompt = (
        f"You are 'Namma Capsule', a hyper-local news summarizer exclusively focused on delivering "
        f"the Top 10 daily news summaries relevant to Bangalore, across 10 fixed categories. "
        f"Generate exactly 10 concise news summaries, each belonging to these fixed categories: "
        f"{', '.join(categories)}. "
        f"Each summary must begin with the sequential number (1–10), category, and date ({valid_date}), "
        f"and never exceed 60 words. "
        f"Each summary ends with source line in markdown (📰 Source: Name – [Read More](https://example.com)) "
        f"and a sponsor line provided by the user, randomly shuffled. "
        f"Always separate each summary with a horizontal divider (---). Never miss any categories. "
        f"If fresh news is unavailable for any category, include relevant Bangalore-based throwback, "
        f"policy explainer, or event info."
    )
    return prompt

# Function to get summaries from OpenAI
def get_summaries(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=1500,
    )
    return response.choices[0].message.content

# Main Logic
if user_input:
    valid_date = validate_input(user_input)
    if valid_date:
        prompt = build_prompt(valid_date)
        news_summaries = get_summaries(prompt)
        
        # Shuffle sponsor lines
        random.shuffle(sponsor_lines)
        
        # Split summaries
        summary_list = news_summaries.split("---")
        
        # Display summaries
        if len(summary_list) == 10:
            for idx, summary in enumerate(summary_list):
                summary = summary.strip()
                if summary:
                    st.markdown(f"{summary}\n\n{sponsor_lines[idx]}")
                    st.markdown("---")
        else:
            st.error("❌ Error: Summaries count mismatch. Please regenerate.")
    else:
        st.error("Please type your question in the correct format: Top 10 Bangalore news today or Top 10 Bangalore news [DATE].")
