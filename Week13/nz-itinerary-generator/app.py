"""Streamlit interface for the LLM-powered New Zealand itinerary generator."""

import os
from typing import List

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from prompt_builder import SYSTEM_PROMPT, TripPreferences, build_user_prompt


load_dotenv()

st.set_page_config(
    page_title="NZ Travel Itinerary Generator",
    page_icon="🇳🇿",
    layout="wide",
)

st.title("🇳🇿 LLM-Powered New Zealand Travel Itinerary Generator")
st.write(
    "Enter your preferences to generate a personalised New Zealand itinerary. "
    "All prices, times, availability, and conditions must be verified before travel."
)

with st.sidebar:
    st.header("API configuration")
    model = st.text_input(
        "OpenAI model",
        value=os.getenv("OPENAI_MODEL", "gpt-5.4-mini"),
        help="You can change this using OPENAI_MODEL in the .env file.",
    )
    use_web_search = st.checkbox(
        "Use live web search",
        value=True,
        help="Helps the model identify recent travel information. It may increase API usage.",
    )

with st.form("trip_form"):
    col1, col2 = st.columns(2)

    with col1:
        start_city = st.text_input("Starting city", "Auckland")
        end_city = st.text_input("Ending city", "Queenstown")
        days = st.slider("Number of days", min_value=3, max_value=30, value=10)
        month_or_season = st.text_input("Month or season", "Summer")
        travellers = st.number_input(
            "Number of travellers", min_value=1, max_value=12, value=2
        )
        budget_level = st.selectbox(
            "Budget level", ["Budget", "Mid-range", "Comfort", "Luxury"], index=1
        )
        transport = st.selectbox(
            "Preferred transport",
            [
                "Rental car and domestic flights",
                "Rental car",
                "Campervan",
                "Public transport and coaches",
                "Domestic flights and organised tours",
            ],
        )

    with col2:
        pace = st.selectbox(
            "Travel pace", ["Relaxed", "Balanced", "Fast-paced"], index=1
        )
        interests: List[str] = st.multiselect(
            "Interests",
            [
                "Nature",
                "Hiking",
                "Māori culture",
                "Food",
                "Adventure",
                "Wildlife",
                "Beaches",
                "Cities",
                "Photography",
                "Film locations",
                "Wine",
                "Family activities",
            ],
            default=["Nature", "Māori culture", "Cities"],
        )
        accommodation = st.selectbox(
            "Accommodation",
            ["Hostels", "Motels", "Hotels", "Holiday parks", "Mixed accommodation"],
            index=2,
        )
        dietary_requirements = st.text_input("Dietary requirements", "None")
        accessibility_requirements = st.text_input(
            "Accessibility or mobility requirements", "None"
        )
        must_visit = st.text_area(
            "Must-visit places or activities",
            "Rotorua, Wellington and Milford Sound",
        )
        avoid = st.text_input("Places or activities to avoid", "None")
        additional_notes = st.text_area(
            "Additional notes",
            "Allow time to rest after long travel days.",
        )

    submitted = st.form_submit_button("Generate itinerary", type="primary")

if submitted:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        st.error(
            "OPENAI_API_KEY was not found. Copy .env.example to .env and add your key."
        )
        st.stop()

    preferences = TripPreferences(
        start_city=start_city,
        end_city=end_city,
        days=days,
        month_or_season=month_or_season,
        travellers=int(travellers),
        budget_level=budget_level,
        transport=transport,
        pace=pace,
        interests=interests,
        accommodation=accommodation,
        dietary_requirements=dietary_requirements,
        accessibility_requirements=accessibility_requirements,
        must_visit=must_visit,
        avoid=avoid,
        additional_notes=additional_notes,
    )

    user_prompt = build_user_prompt(preferences)
    client = OpenAI(api_key=api_key)

    request_options = {
        "model": model,
        "instructions": SYSTEM_PROMPT,
        "input": user_prompt,
    }

    if use_web_search:
        request_options["tools"] = [{"type": "web_search"}]

    try:
        with st.spinner("Creating your itinerary..."):
            response = client.responses.create(**request_options)
            itinerary = response.output_text

        st.success("Itinerary generated")
        st.markdown(itinerary)
        st.download_button(
            "Download itinerary as Markdown",
            data=itinerary,
            file_name="new-zealand-itinerary.md",
            mime="text/markdown",
        )

        with st.expander("View the generated prompt"):
            st.code(user_prompt, language="text")

    except Exception as exc:
        st.error(
            "The itinerary could not be generated. Check the API key, model access, "
            f"internet connection, and API account status.\n\nTechnical detail: {exc}"
        )

st.divider()
st.caption(
    "This application is an educational project. It does not make bookings and "
    "must not be treated as an authoritative safety or availability service."
)
