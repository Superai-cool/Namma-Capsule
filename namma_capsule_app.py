
import streamlit as st
import openai
import random
from datetime import datetime

# Set your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Sponsor ads
sponsors = [
    "📣 *Powered by* [**Flatreads**](https://www.flatreads.com/) – *Your Apartment, Your City, Your Community.*",
    "📣 *Sponsored by* [**BengaluruBytes**](https://www.bengalurubytes.com/) – *All about Bengaluru.*",
    "📣 *Presented by* [**NammaMetro News**](https://www.nammametronews.com/) – *Stay connected.*",
    "📣 *Supported by* [**Green Bengaluru**](https://www.greenbengaluru.org/) – *For a cleaner city.*",
    "📣 *Brought to you by* [**TechCity Bangalore**](https://www.techcitybangalore.com/) – *Innovation at its best.*",
    "📣 *In association with* [**HealthCity**](https://www.healthcitybangalore.com/) – *Your health, our priority.*",
    "📣 *Powered by* [**EduBengaluru**](https://www.edubengaluru.com/) – *Empowering education.*",
    "📣 *Sponsored by* [**BizBuzz Bangalore**](https://www.bizbuzzbangalore.com/) – *Business simplified.*",
    "📣 *Presented by* [**CultureVibe**](https://www.culturevibe.in/) – *Celebrate Bengaluru’s culture.*",
    "📣 *Supported by* [**InfraBengaluru**](https://www.infrabengaluru.com/) – *Building the future.*",
]

# Fixed categories
categories = [
    "Bengaluru Local News",
    "Politics",
    "Startup",
    "Education",
    "Technology",
    "Health",
    "Environment",
    "Sports",
    "Entertainment",
    "Real Estate"
]

def generate_news_summaries(query_date):
    prompt = f"""
    Generate exactly 10 Bengaluru-specific hyper-local news summaries strictly limited to 60 words each for the following categories on {query_date}:
    {', '.join(categories)}.
    Follow this format strictly for each summary:

    Category | Date

    Summary (≤ 60 words)

    📰 Source: Name – [Read More](link)
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=1000
    )

    return response['choices'][0]['message']['content'].strip().split('\n\n')

# Streamlit App
st.title("🗞️ Namma Capsule – Bengaluru's Hyper-local News")

query = st.text_input("Ask for top 10 Bengaluru news:")

if query:
    query = query.strip()
    if query.lower() == "top 10 bangalore news today":
        query_date = datetime.now().strftime('%d %B %Y')
    elif query.lower().startswith("top 10 bangalore news"):
        try:
            query_date = query.split("news", 1)[1].strip()
            datetime.strptime(query_date, '%d %B %Y')
        except ValueError:
            st.error("Please provide date in correct format: DD Month YYYY (e.g., 27 March 2025)")
            st.stop()
    else:
        st.error("Please type your question in the correct format: **Top 10 Bangalore news today** or **Top 10 Bangalore news [DATE]**.")
        st.stop()

    with st.spinner('Fetching news summaries...'):
        summaries = generate_news_summaries(query_date)

        if len(summaries) != 10:
            st.error("Validation failed, regenerating summaries...")
            st.stop()

        random.shuffle(sponsors)

        for i, summary in enumerate(summaries):
            st.markdown(f"**{i+1}. {summary}**")
            st.markdown(sponsors[i])
            st.markdown('---')
