import os
import requests
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
import google.generativeai as genai 

load_dotenv(override=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY missing in environment (.env) file.")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY missing in environment (.env) file.")
if not SERPER_API_KEY:
    raise ValueError("SERPER_API_KEY missing in environment (.env) file.")

genai.configure(api_key=GEMINI_API_KEY)
llm = LLM(
    model="gemini/gemini-2.0-flash",
    api_key=GEMINI_API_KEY,
    temperature=0.7,
)


@tool
def serper_search(query: str) -> str:
    """Search Google using Serper.dev and return summarized top result links."""
    headers  = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "q": query,
        "num": 3
    }
    response = requests.post("https://google.serper.dev/search", headers=headers, json=data)
    if response.status_code == 200:
        results = response.json()
        output = []
        for item in results.get("organic", []):
            output.append(f"{item.get('title')} - {item.get('link')}")
        return "\n".join(output)
    else:
        return f"Error from Serper API: {response.status_code} - {response.text}"


destination = input("Enter your travel destination: ")
travel_dates = input("Enter your travel dates (default: November 5th, 2025): ") or "Nov 5, 2025"
duration_days = int(input("How many days is your trip? (default: 3): ") or "3")
preferences = input("Enter your travel preferences (default: Cultural & Museums, Food & Culinary): ") or "Cultural & Museums, Food & Culinary"
budget = input("Enter your budget (budget, moderate, luxury) (default: moderate): ") or "moderate"

print(f"\nGenerating travel plan for {destination}…\n")

attractions_specialist = Agent(
    role="Attractions Specialist",
    goal="Discover the best attractions, activities, and hidden gems at the destination.",
    backstory="An expert who finds the most interesting attractions and activities that match travelers' preferences.",
    verbose=True,
    llm=llm,
    tools=[serper_search]
)

itinerary_planner = Agent(
    role="Itinerary Planner",
    goal="Create a well-organized travel plan that maximizes experience.",
    backstory="A master of travel logistics who balances activities, rest, and travel times.",
    verbose=True,
    llm=llm,
    tools=[serper_search]
)

summary_agent = Agent(
    role="Summary Agent",
    goal="Summarize the travel plan and provide key insights from both the attractions and itinerary tasks.",
    backstory="An expert in distilling complex travel plans into concise summaries.",
    verbose=True,
    llm=llm,
    tools=None
)


attractions_task = Task(
    description=(
        f"Find the best attractions in {destination} for a {budget}-budget, "
        f"{duration_days}-day trip matching these preferences: {preferences}.\n"
        "For each attraction include:\n"
        "• Name & brief description\n"
        "• Why it's worth visiting\n"
        "• Recommended time to spend\n"
        "• Entrance fees (if any)\n"
        "• Best time of day/week\n"
        "• Insider tips\n\n"
        "Group by type (museums, outdoor, dining, hidden gems, etc.)."
    ),
    agent=attractions_specialist,
    expected_output=f"A categorized list of attractions in {destination}"
)

itinerary_task = Task(
    description=(
        f"Create a detailed {duration_days}-day itinerary for {destination} starting on {travel_dates}.\n"
        f"Traveler preferences: {preferences}. Budget: {budget}.\n\n"
        "Each day must include:\n"
        "• Morning, afternoon, evening activities with times\n"
        "• Suggested restaurants with cuisine & price\n"
        "• Transport between attractions with duration\n"
        "• Rest periods and flexibility\n\n"
        "Optimize for minimal backtracking, opening hours, and variety."
    ),
    agent=itinerary_planner,
    expected_output=f"A day-by-day itinerary for {destination}"
)

summary_task = Task(
    description=(
        f"Summarize the travel plan for {destination} based on the attractions and itinerary tasks.\n"
        "Include key highlights, must-see attractions, and overall trip recommendations.\n"
        "Focus on providing a concise overview that captures the essence of the trip."
    ),
    agent=summary_agent,
    expected_output=f"A concise summary of the travel plan for {destination}"
)

agents = [attractions_specialist, itinerary_planner, summary_agent]
tasks = [attractions_task, itinerary_task, summary_task]

inputs = {
    "destination": destination,
    "travel_dates": travel_dates,
    "duration_days": duration_days,
    "preferences": preferences,
    "budget": budget
}

crew = Crew(
    agents=agents,
    tasks=tasks,
    verbose=True,
    process=Process.sequential
)

result = crew.kickoff(inputs=inputs)

print("\n\n########################")
print(result)
