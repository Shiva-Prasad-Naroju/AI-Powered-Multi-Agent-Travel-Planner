# from crewai import Task

# def create_summary_task(agent, destination):
#     return Task(
#         description=(
#             f"Summarize the travel plan for {destination} based on the attractions and itinerary tasks.\n"
#             "Include key highlights, must-see attractions, and overall trip recommendations.\n"
#             "Focus on providing a concise overview that captures the essence of the trip."
#         ),
#         agent=agent,
#         expected_output=f"A concise summary of the travel plan for {destination}"
#     )

# tasks/summary_task.py
from crewai import Task
from tools.fallback_search import FallbackSearchTool

def create_summary_task(agent, destination):
    return Task(
        description=(
            f"Summarize the travel plan for {destination} based on attractions, hotels, restaurants, and itinerary.\n"
            "Return the result in **valid JSON** with this schema:\n"
            "{\n"
            '  "overview": "string",\n'
            '  "highlight_attractions": ["string", ...],\n'
            '  "daily_summary": [\n'
            '    {\n'
            '      "day": number,\n'
            '      "summary": "string",\n'
            '      "meals": {\n'
            '          "breakfast": "string",\n'
            '          "lunch": "string",\n'
            '          "dinner": "string"\n'
            '      }\n'
            '    }\n'
            '  ],\n'
            '  "estimated_budget": "string",\n'
            '  "tips": ["string", ...]\n'
            "}\n\n"
            "Important:\n"
            "- Provide concise, actionable travel insights.\n"
            "- Use FallbackSearchTool(query) if extra clarification is needed.\n"
            "- Do NOT include any text outside JSON.\n"
            "- Validate JSON before returning."
        ),
        agent=agent,
        # tools=[FallbackSearchTool()],
        tools=[],
        expected_output=f"Structured summary of the travel plan for {destination}."
    )
