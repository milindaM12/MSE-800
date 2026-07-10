# LLM-Powered New Zealand Travel Itinerary Generator

A Streamlit application that uses an OpenAI large language model to generate
personalised New Zealand travel itineraries.

## Activity requirement

This repository contains:

- An LLM-powered itinerary generator
- An optimised prompt in `OPTIMIZED_PROMPT.md`
- A sample AI-generated itinerary in `SAMPLE_ITINERARY.md`
- A GitHub-ready README and safe API-key configuration
- A basic automated test for the prompt builder

## Features

- Collects trip duration, season, budget, transport, pace, interests,
  accommodation, accessibility, and dietary requirements
- Produces a structured day-by-day itinerary
- Estimates costs in New Zealand dollars
- Warns about long driving days and weather-sensitive outdoor activities
- Optionally uses OpenAI web search for recent information
- Allows the generated itinerary to be downloaded as Markdown
- Keeps the API key outside the source code

## Project structure

```text
nz-itinerary-generator/
├── app.py
├── prompt_builder.py
├── OPTIMIZED_PROMPT.md
├── SAMPLE_ITINERARY.md
├── requirements.txt
├── .env.example
├── .gitignore
├── tests/
│   └── test_prompt_builder.py
└── README.md
```

## Technologies

- Python
- Streamlit
- OpenAI Responses API
- python-dotenv
- Pytest

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/nz-itinerary-generator.git
cd nz-itinerary-generator
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add the API key

Copy `.env.example` to `.env`:

```bash
copy .env.example .env
```

For macOS or Linux:

```bash
cp .env.example .env
```

Then edit `.env`:

```env
OPENAI_API_KEY=your_real_api_key
OPENAI_MODEL=gpt-5.4-mini
```

Never commit the `.env` file or an API key to GitHub.

### 5. Run the application

```bash
streamlit run app.py
```

Open the local address displayed in the terminal, normally:

```text
http://localhost:8501
```

## Run the test

```bash
pytest
```

## Prompt-engineering approach

The application uses two prompt layers:

1. A stable **system prompt** that defines the planner's role, output format,
   anti-hallucination rules, safety requirements, and New Zealand conventions.
2. A dynamic **user prompt** containing the traveller's preferences and trip
   constraints.

This design improves consistency, maintainability, and testing. See
`OPTIMIZED_PROMPT.md` for the complete prompt.

## Suggested GitHub submission text

**Project title:** LLM-Powered New Zealand Travel Itinerary Generator

**Description:**  
This Python and Streamlit project uses the OpenAI Responses API to create
personalised New Zealand travel itineraries based on trip duration, budget,
transport, pace, interests, accommodation, and traveller requirements. The prompt
includes route-planning constraints, safety checks, cost estimates, and
anti-hallucination instructions.

**Repository link:**  
`https://github.com/YOUR_USERNAME/nz-itinerary-generator`

## Push the project to GitHub

Create an empty GitHub repository named `nz-itinerary-generator`, and then run:

```bash
git init
git add .
git commit -m "Add LLM-powered New Zealand itinerary generator"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/nz-itinerary-generator.git
git push -u origin main
```

## Optional Streamlit Community Cloud deployment

1. Push the project to GitHub.
2. Open Streamlit Community Cloud.
3. Select this repository and choose `app.py`.
4. Add the following secret in the deployment settings:

```toml
OPENAI_API_KEY = "your_real_api_key"
OPENAI_MODEL = "gpt-5.4-mini"
```

For deployment, you may replace the `os.getenv` calls with Streamlit secrets or
provide the values as environment variables.

## Limitations

- The LLM can still make mistakes.
- Travel times, prices, schedules, weather, track status, road conditions, and
  availability change.
- The application does not make bookings.
- Generated advice must be checked against official and current sources before travel.
