# import os
# from dotenv import load_dotenv
# from crewai import Crew, Process, LLM
# import google.generativeai as genai

# from agents.attractions import create_attractions_agent
# from agents.itinerary import create_itinerary_agent
# from agents.summary import create_summary_agent
# from tasks.attractions_task import create_attractions_task
# from tasks.itinerary_task import create_itinerary_task
# from tasks.summary_task import create_summary_task

# load_dotenv(override=True)

# # Load API keys
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# if not GEMINI_API_KEY:
#     raise ValueError("GEMINI_API_KEY missing in environment (.env) file.")

# # Configure Gemini
# genai.configure(api_key=GEMINI_API_KEY)
# llm = LLM(model="gemini/gemini-2.0-flash", api_key=GEMINI_API_KEY, temperature=0.7)

# def run_travel_planner(destination, travel_dates, days, preferences, budget):
#     # Create agents
#     attractions_agent = create_attractions_agent(llm)
#     itinerary_agent = create_itinerary_agent(llm)
#     summary_agent = create_summary_agent(llm)

#     # Create tasks
#     attractions_task = create_attractions_task(attractions_agent, destination, days, preferences, budget)
#     itinerary_task = create_itinerary_task(itinerary_agent, destination, travel_dates, days, preferences, budget)
#     summary_task = create_summary_task(summary_agent, destination)

#     # Assemble crew
#     crew = Crew(
#         agents=[attractions_agent, itinerary_agent, summary_agent],
#         tasks=[attractions_task, itinerary_task, summary_task],
#         verbose=True,
#         process=Process.sequential
#     )

#     return crew.kickoff(inputs={
#         "destination": destination,
#         "travel_dates": travel_dates,
#         "duration_days": days,
#         "preferences": preferences,
#         "budget": budget
#     })


# crew/assemble.py
import os
from dotenv import load_dotenv
from crewai import Crew, Process, LLM

from agents.attractions import create_attractions_agent
from agents.itinerary import create_itinerary_agent
from agents.summary import create_summary_agent

from tasks.attractions_task import create_attractions_task
from tasks.itinerary_task import create_itinerary_task
from tasks.summary_task import create_summary_task
from tasks.hotels_task import create_hotels_task
from tasks.restaurants_task import create_restaurants_task
from tasks.transport_task import create_transport_task

load_dotenv(override=True)

# Load Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY missing in environment (.env) file.")

# Configure Gemini LLM
llm = LLM(
    model="gemini/gemini-2.0-flash",
    api_key=GEMINI_API_KEY,
    temperature=0.7
)


def run_travel_planner(destination, travel_dates, days, preferences, budget):
    """
    Orchestrates all agents and tasks to generate a full travel plan.
    Returns structured JSON with results from all agents.
    """
    # --- Create Agents ---
    attractions_agent = create_attractions_agent(llm)
    itinerary_agent = create_itinerary_agent(llm)
    summary_agent = create_summary_agent(llm)

    # --- Create Tasks ---
    attractions_task = create_attractions_task(attractions_agent, destination, days, preferences, budget)
    itinerary_task = create_itinerary_task(itinerary_agent, destination, travel_dates, days, preferences, budget)
    summary_task = create_summary_task(summary_agent, destination)

    # Optional tasks for hotels, restaurants, transport
    hotels_task = create_hotels_task(itinerary_agent, destination, days, budget, preferences)
    restaurants_task = create_restaurants_task(itinerary_agent, destination, days, preferences, budget)
    transport_task = create_transport_task(itinerary_agent, destination, days, preferences, budget)

    # --- Assemble Crew ---
    crew = Crew(
        agents=[attractions_agent, itinerary_agent, summary_agent],
        tasks=[
            attractions_task,
            hotels_task,
            restaurants_task,
            transport_task,
            itinerary_task,
            summary_task
        ],
        verbose=True,
        process=Process.sequential  # switch to parallel if desired
    )

    # --- Kickoff Crew with Error Handling ---
    try:
        result = crew.kickoff(inputs={
            "destination": destination,
            "travel_dates": travel_dates,
            "duration_days": days,
            "preferences": preferences,
            "budget": budget
        })
    except Exception as e:
        result = {"error": str(e)}

    return {
        "destination": destination,
        "travel_dates": travel_dates,
        "duration_days": days,
        "preferences": preferences,
        "budget": budget,
        "results": result
    }
