import os
import streamlit as st
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

st.set_page_config(layout="centered", page_icon='✈️', page_title="Travel Planner")
# Load environment variables
load_dotenv()  

# Get API key
my_api_key = os.getenv("GOOGLE_API_KEY")

# Check if API key is loaded correctly
if not my_api_key:
    st.error("🔑 API key not found. Please check your .env file.")
    st.stop()  

# Create AI model
model = ChatGoogleGenerativeAI(api_key=my_api_key, model="gemini-1.5-flash", temperature=1)

# Creating prompt template
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "Act as a travel planner! you are here to create seamless, personalized travel experiences tailored to your preferences. Whether you’re planning a weekend getaway or an extended adventure, you’ll provide concise 1-2 line itineraries, accurate cost estimates, booking recommendations, weather insights, and local tips—all designed to make your trip planning effortless, efficient, and enjoyable. Let’s craft your perfect journey together!"),
    ("human", "Plan a trip from {source} to {destination} for {days} days. Budget: {budget}. Group: {people}. Interests: {interests}.")
])

# 🌟 Apply custom styles
st.markdown("""
    <style>
        body {
            background-color:rgb(137, 183, 230);
        }
        .subheader {
            text-align: center;
            font-size: 20px;
            color: #2E86C1;
        }
        .info-box {
            padding: 10px;
            border: None;
            font-size: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# Main Title
st.markdown('<h1 style="text-align: center;color:rgb(255, 51, 238);font-weight: bold; ">✈️ AI-Powered Travel Planner 🛬</h1>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Plan your dream vacation in seconds! 🚀</p>', unsafe_allow_html=True)

#Travel Input Section
st.markdown("### 📝 Fill your travel details:")
source = st.text_input("📍 Enter city:")
destination = st.text_input("🎯 Enter destination city:")
days = st.number_input("📅 Enter number of days:", min_value=1)
budget = st.selectbox("💰 What’s your budget?", ["", "Low-Budget", "Mid-Range", "Luxury"])
people = st.selectbox("👨‍👩‍👦 How many people are traveling?", ["Solo 🚶🏻‍♀️‍➡️", "Couple 🧑🏻‍🤝‍👩🏻", "Family 👪"])
interests = st.selectbox("🎭 What are your interests? " , ["","Food 🍕", "Culture 🥻", "Adventure 🏄🏻", " Shopping 🛍️", "Temple 📿"])

#Generate Travel Plan button
if st.button("Make Travel Plan ! 🚀"):
    # Prepare input for the prompt
    raw_input = {
        "source": source,
        "destination": destination,
        "days": days,
        "budget": budget,
        "people": people,
        "interests": interests
    }

    # Initialize the output parser
    parser = StrOutputParser()

    # Chain everything together
    chain = chat_prompt | model | parser

    try:
        # Generate AI response
        response = chain.invoke(raw_input)


        # 🎉 Display response
        st.subheader("📝 Your Personalized Travel Plan ")
        st.write(f'<div class="info-box">{response}</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"⚠️ An error occurred: {str(e)}")