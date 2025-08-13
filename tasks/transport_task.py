# tasks/transport_task.py
from crewai import Task
from tools.fallback_search import FallbackSearchTool

def create_transport_task(agent, destination, days, preferences, budget):
    return Task(
        description=(
            f"You are a local transport planning expert. Suggest the best transportation options in and around {destination} "
            f"for a {days}-day trip with a {budget} budget, considering these preferences: {preferences}.\n\n"
            "You MUST return the final answer strictly in valid JSON format with this schema:\n"
            "{\n"
            '  "destination": "string",\n'
            '  "transport_options": [\n'
            '    {\n'
            '      "mode": "string",  # e.g. metro, taxi, bus, bike rental\n'
            '      "description": "string",\n'
            '      "cost_range": "string",\n'
            '      "duration_range": "string",\n'
            '      "availability": "string",\n'
            '      "pros": ["string", ...],\n'
            '      "cons": ["string", ...],\n'
            '      "start_point": "string",\n'
            '      "end_point": "string",\n'
            '      "coordinates": {\n'
            '        "start_lat": "string",\n'
            '        "start_lon": "string",\n'
            '        "end_lat": "string",\n'
            '        "end_lon": "string"\n'
            '      },\n'
            '      "link": "string"  # optional booking/info page\n'
            '    }\n'
            '  ]\n'
            "}\n\n"
            "Important:\n"
            "- Include local, affordable, and premium options.\n"
            "- Provide time & cost estimates.\n"
            "- Suggest sustainable transport if available (e.g., cycling, EV taxis).\n"
            "- If information is missing, use FallbackSearchTool(query) to retrieve it.\n"
            "- Validate JSON before returning — no text outside JSON.\n"
        ),
        agent=agent,
        # tools=[FallbackSearchTool()],
        tools=[],
        expected_output=f"Strict JSON list of transportation options in and around {destination}."
    )
