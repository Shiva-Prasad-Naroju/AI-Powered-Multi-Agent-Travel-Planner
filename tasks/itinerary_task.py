# from crewai import Task

# def create_itinerary_task(agent, destination, travel_dates, days, preferences, budget):
#     return Task(
#         description=(
#             f"Create a detailed {days}-day itinerary for {destination} starting on {travel_dates}.\n"
#             f"Traveler preferences: {preferences}. Budget: {budget}.\n\n"
#             "Each day must include:\n"
#             "• Morning, afternoon, evening activities with times\n"
#             "• Suggested restaurants with cuisine & price\n"
#             "• Transport between attractions with duration\n"
#             "• Rest periods and flexibility\n\n"
#             "Optimize for minimal backtracking, opening hours, and variety."
#         ),
#         agent=agent,
#         expected_output=f"A day-by-day itinerary for {destination}"
#     )



# tasks/itinerary_task.py
from crewai import Task
from tools.fallback_search import FallbackSearchTool

def create_itinerary_task(agent, destination, travel_dates, days, preferences, budget):
    return Task(
        description=(
            f"You are an expert travel itinerary planner. Using information provided by the Attractions, Hotels, Restaurants, "
            f"and Transport agents, create a detailed {days}-day itinerary for {destination} within a {budget} budget, matching "
            f"these preferences: {preferences} for {travel_dates}.\n\n"
            "Return your final answer strictly in valid JSON format with this schema:\n"
            "{\n"
            '  "destination": "string",\n'
            '  "total_days": number,\n'
            '  "days": [\n'
            '    {\n'
            '      "day": number,\n'
            '      "date": "string (optional)",\n'
            '      "summary": "string",\n'
            '      "schedule": [\n'
            '        {\n'
            '          "time": "string",\n'
            '          "activity": "string",\n'
            '          "location": "string",\n'
            '          "coordinates": {"lat": "string", "lon": "string"},\n'
            '          "transport_mode": "string",\n'
            '          "cost": "string",\n'
            '          "notes": "string"\n'
            '        }\n'
            '      ]\n'
            '    }\n'
            '  ],\n'
            '  "total_estimated_cost": "string",\n'
            '  "special_tips": ["string", ...],\n'
            '  "weather_preparedness": ["string", ...]\n'
            "}\n\n"
            "Rules:\n"
            "- Include breakfast/lunch/dinner spots for each day.\n"
            "- Use attractions, hotels, restaurants, and transport data.\n"
            "- Ensure activities are logically ordered with minimal travel time.\n"
            "- Spread out popular attractions to avoid crowd fatigue.\n"
            "- Consider weather conditions (use FallbackSearchTool if missing).\n"
            "- Include at least one hidden gem or unique local experience.\n"
            "- JSON must be valid — no text outside the JSON.\n"
        ),
        agent=agent,
        # tools=[FallbackSearchTool()],
        tools=[],
        expected_output=f"A complete {days}-day structured itinerary for {destination}."
    )

