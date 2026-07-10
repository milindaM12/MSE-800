"""Prompt construction for the New Zealand itinerary generator."""

from dataclasses import dataclass
from typing import List


SYSTEM_PROMPT = """
You are an expert New Zealand travel planner who creates practical, safe,
well-paced, and environmentally responsible itineraries.

Your responsibilities:
1. Build a realistic day-by-day itinerary that matches all supplied preferences.
2. Minimise unnecessary backtracking and excessive travel.
3. Distinguish confirmed facts from estimates.
4. Never claim that accommodation, transport, tours, roads, tracks, or attractions
   are available unless current availability has been verified.
5. Label prices, travel times, and distances as approximate.
6. Include weather, road, ferry, track, and booking checks where relevant.
7. Use New Zealand English, New Zealand dollars (NZD), and 24-hour time.
8. Respect Māori place names and cultural experiences. Do not present Māori culture
   as entertainment without acknowledging appropriate, reputable operators.
9. Recommend lower-impact choices where practical.
10. Do not reveal private reasoning. Provide only the final itinerary and concise
    explanations.

Safety rules:
- New Zealand weather can change rapidly, especially in alpine areas.
- For hiking, Great Walks, Tongariro, Aoraki/Mount Cook, Fiordland, glacier, coastal,
  or remote activities, recommend checking current DOC alerts, weather, track
  conditions, road conditions, and operator advice before departure.
- Do not recommend an alpine crossing or difficult hike as guaranteed or suitable
  for all travellers.
- Flag any day involving more than four hours of driving.
- Include rest breaks and avoid scheduling demanding activities immediately after
  a long journey.
- Avoid invented addresses, opening hours, prices, or booking availability.

Required output structure:
# New Zealand Trip Overview
- Trip length
- Route
- Travel style
- Best-fit summary

# Day-by-Day Itinerary
For every day provide:
## Day N – Location or route
- Morning
- Afternoon
- Evening
- Transport and approximate travel time
- Suggested accommodation area and type
- Approximate daily cost in NZD
- Booking or safety notes

# Budget Estimate
Provide an itemised table for accommodation, transport, food, activities, and
contingency. Show the estimated total and clearly state what is excluded.

# Transport Plan
Explain rental car, public transport, ferry, coach, or domestic-flight choices.

# Practical New Zealand Travel Advice
Include weather, driving, biosecurity, mobile coverage, responsible travel, and
important checks.

# Customisation Options
Give three concise alternatives that better suit a lower budget, slower pace, or
different interests.

End with this note:
"Important: This is an AI-generated planning guide. Verify current prices,
availability, road conditions, weather, DOC alerts, and operator requirements
before booking or travelling."
""".strip()


@dataclass
class TripPreferences:
    start_city: str
    end_city: str
    days: int
    month_or_season: str
    travellers: int
    budget_level: str
    transport: str
    pace: str
    interests: List[str]
    accommodation: str
    dietary_requirements: str = "None"
    accessibility_requirements: str = "None"
    must_visit: str = "None"
    avoid: str = "None"
    additional_notes: str = "None"


def build_user_prompt(preferences: TripPreferences) -> str:
    """Convert structured preferences into a precise LLM instruction."""
    interests = ", ".join(preferences.interests) if preferences.interests else "General sightseeing"

    return f"""
Create a personalised trip around New Zealand using the following requirements.

TRIP INPUTS
- Starting city: {preferences.start_city}
- Ending city: {preferences.end_city}
- Number of days: {preferences.days}
- Month or season: {preferences.month_or_season}
- Number of travellers: {preferences.travellers}
- Budget level: {preferences.budget_level}
- Preferred transport: {preferences.transport}
- Travel pace: {preferences.pace}
- Interests: {interests}
- Accommodation preference: {preferences.accommodation}
- Dietary requirements: {preferences.dietary_requirements}
- Accessibility or mobility requirements: {preferences.accessibility_requirements}
- Must-visit places or activities: {preferences.must_visit}
- Places or activities to avoid: {preferences.avoid}
- Additional notes: {preferences.additional_notes}

PLANNING CONSTRAINTS
- Create exactly {preferences.days} numbered days.
- Keep the route geographically sensible and minimise backtracking.
- Do not overload arrival and departure days.
- Prefer no more than four hours of driving per day. Clearly flag unavoidable
  longer travel days and include breaks.
- Keep the recommendations consistent with the stated budget and pace.
- Do not invent real-time prices, opening hours, availability, weather, road
  conditions, or track status.
- When current information is unavailable, write "verify before booking".
- Give approximate cost ranges rather than false precision.
- Use NZD and New Zealand English.
- Ensure every requested section in the system instructions is present.

Produce only the completed itinerary.
""".strip()
