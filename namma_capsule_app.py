import streamlit as st
import openai
import re
import random

# ------------------
# Streamlit App
# ------------------
def main():
    st.title("Namma Capsule News")

    # Store or retrieve your OpenAI API key as appropriate.
    # For best practice, store it in Streamlit secrets:
    # e.g., in .streamlit/secrets.toml -> OPENAI_API_KEY="YOUR_KEY"
    openai.api_key = st.secrets["OPENAI_API_KEY"]  # Make sure to set this in your secrets.

    # FINAL HTML CODE (corrected)
    html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Namma Capsule News</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <style>
    /* Basic reset */
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: Arial, sans-serif;
    }

    /* White background for body, black text */
    body {
      background-color: #fff;
      color: #000;
    }

    .container {
      max-width: 800px;
      margin: 0 auto;
      padding: 20px;
    }

    header {
      text-align: center;
      margin-bottom: 30px;
    }

    header h1 {
      font-size: 2em;
      margin-bottom: 10px;
    }

    header p {
      font-weight: 300;
      color: #666;
    }

    .search-bar {
      text-align: center;
      margin-bottom: 40px;
    }

    /* Button styling */
    .search-bar button {
      padding: 12px 24px;
      border: none;
      border-radius: 8px;
      background: linear-gradient(to right, #ff8c00, #ffa500);
      color: #fff;
      cursor: pointer;
      font-size: 1.1em;
      font-weight: bold;
      box-shadow: 0 4px 10px rgba(255,140,0,0.3);
      transition: transform 0.2s, box-shadow 0.2s;
    }

    .search-bar button:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 15px rgba(255,140,0,0.4);
    }

    .news-list {
      display: flex;
      flex-direction: column;
      gap: 20px;
    }

    .news-item {
      background-color: #fff;
      border: 1px solid #000;
      border-radius: 6px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      padding: 20px;
      transition: transform 0.2s, box-shadow 0.2s;
    }

    .news-item:hover {
      transform: translateY(-5px);
      box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }

    .news-date {
      font-size: 0.9em;
      color: #003366; /* Dark blue */
      font-weight: bold;
      margin-bottom: 10px;
    }

    .news-content p {
      margin: 10px 0;
      line-height: 1.5;
    }

    .news-content a {
      text-decoration: none;
      color: #FFA500;
      font-weight: bold;
    }

    .news-content a:hover {
      text-decoration: underline;
    }

    footer {
      text-align: center;
      font-size: 0.8em;
      color: #999;
      margin-top: 40px;
    }
  </style>
</head>
<body>

  <div class="container">
    <header>
      <h1>Namma Capsule News</h1>
      <p>Your quick daily digest of local and national headlines</p>
    </header>

    <!-- Hardcoded button for "Top 10 News Today" -->
    <div class="search-bar">
      <button>Top 10 News Today</button>
    </div>

    <div class="news-list">

      <!-- News Item 1 -->
      <div class="news-item">
        <div class="news-date">Bengaluru Local News | March 27, 2025</div>
        <div class="news-content">
          <p>An aerial image of Bengaluru's Bellandur area has gone viral,
             drawing comparisons to the video game "Clash of Clans" due to
             its stark contrast between densely packed, irregular layouts
             and neatly arranged red-roofed houses.</p>
          <p>
            📰 Source: NDTV –
            <a href="#">Read More</a>
          </p>
          <p>
            📣 Powered by <strong>Flatreads</strong> – Your Apartment, Your City, Your Community.
          </p>
        </div>
      </div>

      <!-- News Item 2 -->
      <div class="news-item">
        <div class="news-date">Bengaluru Local News | March 27, 2025</div>
        <div class="news-content">
          <p>[Add second news story here...]</p>
          <p>📰 Source: [Publication Name] –
            <a href="#">Read More</a>
          </p>
          <p>📣 Powered by <strong>Flatreads</strong> – Your Apartment, Your City, Your Community.</p>
        </div>
      </div>

      <!-- Continue similarly for news items 3 to 10 -->

    </div>

    <footer>
      &copy; 2025 Namma Capsule News
    </footer>
  </div>

</body>
</html>
    """

    # Display the HTML code in Streamlit (for demonstration)
    st.markdown(html_code, unsafe_allow_html=True)

    # User input field
    user_query = st.text_input("Enter your query:")

    # Button to submit
    if st.button("Get News"):
        # Validate query format
        pattern_today = r"^Top 10 Bangalore news today$"
        pattern_date  = r"^Top 10 Bangalore news [A-Za-z]+\s+\d{1,2},\s+\d{4}$"

        if re.match(pattern_today, user_query) or re.match(pattern_date, user_query):
            with st.spinner("Generating the top 10 Bangalore news..."):
                news_output = generate_bangalore_news(user_query)
                st.markdown(news_output, unsafe_allow_html=True)
        else:
            st.write(
                "Please type your question in the correct format: "
                "Top 10 Bangalore news today or Top 10 Bangalore news [DATE]."
            )


def generate_bangalore_news(query_text):
    # Shuffle the 10 sponsor lines each time so their order changes
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
        "📣 Snap Prints | Print-on-Demand Services | WhatsApp : 8830720742"
    ]
    random.shuffle(sponsor_lines)

    # Truncated for brevity – supply your full system instructions here
    system_instructions = (
        "You are 'Namma Capsule', a hyper-local news summarizer exclusively focused on delivering..."
        # etc. (maintain the full rules from your earlier prompt)
    )

    user_prompt = f"{query_text}\n\nRemember all mandatory instructions above."

    # Call the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=1500
    )

    raw_output = response["choices"][0]["message"]["content"].strip()

    # Insert sponsor lines
    lines = raw_output.split("\n")
    sponsor_index = 0
    final_lines = []

    for line in lines:
        if line.strip().startswith("📣"):
            if sponsor_index < 10:
                final_lines.append(sponsor_lines[sponsor_index])
                sponsor_index += 1
            else:
                final_lines.append(line)
        else:
            final_lines.append(line)

    final_text = "\n".join(final_lines)
    return final_text


if __name__ == "__main__":
    main()
