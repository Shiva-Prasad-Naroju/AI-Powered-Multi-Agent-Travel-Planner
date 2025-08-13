# tasks/hotels_task.py
from crewai import Task
from tools.fallback_search import FallbackSearchTool

def create_hotels_task(agent, destination, days, budget, preferences):
    return Task(
        description=(
            f"You are a travel accommodation expert. Find the best hotels in {destination} "
            f"for a {budget}-budget, {days}-day stay matching these preferences: {preferences}.\n\n"
            "You MUST return the final answer strictly in valid JSON format with this schema:\n"
            "{\n"
            '  "destination": "string",\n'
            '  "hotels": [\n'
            '    {\n'
            '      "name": "string",\n'
            '      "description": "string",\n'
            '      "location": "string",\n'
            '      "price_per_night": "string",\n'
            '      "total_estimated_cost": "string",\n'
            '      "amenities": ["string", ...],\n'
            '      "pros": ["string", ...],\n'
            '      "cons": ["string", ...],\n'
            '      "coordinates": {"lat": "string", "lon": "string"},\n'
            '      "link": "string"\n'
            '    }\n'
            '  ]\n'
            "}\n\n"
            "Important:\n"
            "- Only include hotels that fit the budget range.\n"
            "- Prefer well-reviewed hotels (4.0+ rating if available).\n"
            "- Include variety: budget, mid-range, luxury if possible.\n"
            "- Use `null` for unknown fields.\n"
            "- If data is missing, use FallbackSearchTool(query) to retrieve it.\n"
            "- Validate JSON before returning — no text outside JSON.\n"
        ),
        agent=agent,
        # tools=[FallbackSearchTool()],
        tools=[],
        expected_output=f"Strict JSON list of hotels in {destination} matching budget {budget}."
    )
