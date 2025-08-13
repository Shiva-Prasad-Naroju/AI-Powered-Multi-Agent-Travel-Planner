# # from crewai import Task

# # def create_attractions_task(agent, destination, days, preferences, budget):
# #     return Task(
# #         description=(
# #             f"Find the best attractions in {destination} for a {budget}-budget, "
# #             f"{days}-day trip matching these preferences: {preferences}.\n"
# #             "For each attraction include:\n"
# #             "• Name & brief description\n"
# #             "• Why it's worth visiting\n"
# #             "• Recommended time to spend\n"
# #             "• Entrance fees (if any)\n"
# #             "• Best time of day/week\n"
# #             "• Insider tips\n\n"
# #             "Group by type (museums, outdoor, dining, hidden gems, etc.)."
# #         ),
# #         agent=agent,
# #         expected_output=f"A categorized list of attractions in {destination}"
# #     )


# from crewai import Task
# from tools.fallback_search import FallbackSearchTool

# def create_attractions_task(agent, destination, days, preferences, budget):
#     return Task(
#         description=(
#             f"Find the best attractions in {destination} for a {budget}-budget, "
#             f"{days}-day trip matching these preferences: {preferences}.\n"
#             "For each attraction include:\n"
#             "• Name & brief description\n"
#             "• Why it's worth visiting\n"
#             "• Recommended time to spend\n"
#             "• Entrance fees (if any)\n"
#             "• Best time of day/week\n"
#             "• Insider tips\n"
#             "• Weather suitability (Good, Moderate, Avoid based on travel date)\n"
#             "• Accessibility & safety notes\n\n"
#             "Group by type (museums, outdoor, dining, hidden gems, etc.)."
#         ),
#         agent=agent,
#         expected_output=(
#             f"A JSON array of categorized attractions in {destination}, "
#             "each containing: name, description, why_visit, time_to_spend, "
#             "entrance_fees, best_time, insider_tips, weather_suitability, accessibility"
#         ),
#         tools=["WeatherTool", "FallbackSearchTool"]
#     )


# tasks/attractions_task.py
from crewai import Task
from tools.fallback_search import FallbackSearchTool

def create_attractions_task(agent, destination, days, preferences, budget):
    return Task(
        description=(
            f"You are a travel research expert. Find the best attractions in {destination} "
            f"for a {budget}-budget, {days}-day trip matching these preferences: {preferences}.\n\n"
            "You MUST return the final answer strictly in valid JSON format with this schema:\n"
            "{\n"
            '  "destination": "string",\n'
            '  "categories": [\n'
            '    {\n'
            '      "category_name": "string",\n'
            '      "places": [\n'
            '        {\n'
            '          "name": "string",\n'
            '          "description": "string",\n'
            '          "why_visit": "string",\n'
            '          "recommended_time": "string",\n'
            '          "entrance_fee": "string",\n'
            '          "best_time": "string",\n'
            '          "insider_tips": "string",\n'
            '          "coordinates": {"lat": "string", "lon": "string"},\n'
            '          "link": "string"\n'
            '        }\n'
            '      ]\n'
            '    }\n'
            '  ]\n'
            "}\n\n"
            "Important:\n"
            "- Do NOT include any text outside the JSON.\n"
            "- Use `null` if any field is unknown.\n"
            "- If you lack enough info, use the FallbackSearchTool(query) to get structured details.\n"
            "- Validate the JSON before sending.\n"
        ),
        agent=agent,
        # tools=[FallbackSearchTool()],
        tools=[],
        expected_output=f"Strict JSON response containing categorized attractions in {destination}."
    )
