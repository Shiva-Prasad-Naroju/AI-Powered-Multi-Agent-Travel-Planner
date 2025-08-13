# tasks/restaurants_task.py
from crewai import Task
from tools.fallback_search import FallbackSearchTool

def create_restaurants_task(agent, destination, days, preferences, budget):
    return Task(
        description=(
            f"You are a local food and dining expert. Find the best restaurants in {destination} "
            f"for a {budget}-budget, {days}-day trip matching these preferences: {preferences}.\n\n"
            "You MUST return the final answer strictly in valid JSON format with this schema:\n"
            "{\n"
            '  "destination": "string",\n'
            '  "restaurants": [\n'
            '    {\n'
            '      "name": "string",\n'
            '      "description": "string",\n'
            '      "cuisine_type": "string",\n'
            '      "category": "string",  # e.g. street food, fine dining, cafe, casual eatery\n'
            '      "location": "string",\n'
            '      "average_cost_per_person": "string",\n'
            '      "signature_dishes": ["string", ...],\n'
            '      "vegetarian_options": "boolean",\n'
            '      "rating": "string",\n'
            '      "pros": ["string", ...],\n'
            '      "cons": ["string", ...],\n'
            '      "coordinates": {"lat": "string", "lon": "string"},\n'
            '      "link": "string"\n'
            '    }\n'
            '  ]\n'
            "}\n\n"
            "Important:\n"
            "- Include a mix of cuisines & dining experiences.\n"
            "- Respect dietary preferences mentioned.\n"
            "- Only include restaurants with good ratings (4.0+ if possible).\n"
            "- If data is missing, use FallbackSearchTool(query) to retrieve it.\n"
            "- Validate JSON before returning — no text outside JSON.\n"
        ),
        agent=agent,
        # tools=[FallbackSearchTool()],
        tools=[],
        expected_output=f"Strict JSON list of restaurants in {destination} matching preferences {preferences}."
    )
