# from crewai import Agent
# from tools.serper_search import serper_search

# def create_itinerary_agent(llm):
#     return Agent(
#         role="Itinerary Planner",
#         goal="Create a well-organized travel plan that maximizes experience.",
#         backstory="A master of travel logistics who balances activities, rest, and travel times.",
#         verbose=True,
#         llm=llm,
#         tools=[serper_search],
#         memory=True
#     )

from crewai import Agent
from tools.fallback_search import FallbackSearchTool

def create_itinerary_agent(llm):
    return Agent(
        role="Itinerary Planner",
        goal=(
            "Create a well-organized travel plan that maximizes experience while "
            "optimizing time, budget, and energy."
        ),
        backstory=(
            "An award-winning travel logistics planner who has designed hundreds of "
            "itineraries for solo travelers, families, and luxury tours. Skilled at "
            "balancing attractions, rest, transit, and flexibility for unexpected adventures."
        ),
        verbose=True,
        llm=llm,
        # tools=[FallbackSearchTool()],  # ✅ Pass the class, do not instantiate
        tools=[], 
        memory=True,
        output_format=(
            "Return the itinerary in **valid JSON** with keys: "
            "`day`, `morning_activity`, `afternoon_activity`, `evening_activity`, "
            "`notes`, `estimated_cost`, `travel_time_between`."
        )
    )
