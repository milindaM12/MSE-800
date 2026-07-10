from prompt_builder import TripPreferences, build_user_prompt


def test_prompt_contains_core_preferences():
    preferences = TripPreferences(
        start_city="Auckland",
        end_city="Queenstown",
        days=10,
        month_or_season="January",
        travellers=2,
        budget_level="Mid-range",
        transport="Rental car and domestic flights",
        pace="Balanced",
        interests=["Nature", "Māori culture"],
        accommodation="Hotels",
    )

    prompt = build_user_prompt(preferences)

    assert "Starting city: Auckland" in prompt
    assert "Ending city: Queenstown" in prompt
    assert "Number of days: 10" in prompt
    assert "Nature, Māori culture" in prompt
    assert "Create exactly 10 numbered days" in prompt
