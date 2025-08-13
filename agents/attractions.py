# from crewai import Agent
# from tools.serper_search import serper_search

# def create_attractions_agent(llm):
#     return Agent(
#         role="Attractions Specialist",
#         goal="Discover the best attractions, activities, and hidden gems at the destination.",
#         backstory="An expert who finds the most interesting attractions and activities that match travelers' preferences.",
#         verbose=True,
#         llm=llm,
#         tools=[serper_search],
#         memory=True
#     )

from crewai import Agent
from tools.fallback_search import FallbackSearchTool

def create_attractions_agent(llm):
    return Agent(
        role="Attractions Specialist",
        goal=(
            "Discover the most exciting attractions, activities, and hidden gems "
            "that perfectly match the traveler's preferences, budget, and trip length."
        ),
        backstory=(
            "A seasoned world traveler and destination researcher with 15+ years of "
            "experience in curating personalized attraction lists. Known for finding "
            "not only the famous spots but also off-the-beaten-path experiences. "
            "Understands how to balance culture, leisure, and adventure."
        ),
        verbose=True,
        llm=llm,
        # tools=[FallbackSearchTool()], 
        tools=[], 
        memory=True,
        output_format=(
            "Return the results in **valid JSON** with keys: "
            "`name`, `description`, `category`, `why_worth_visiting`, "
            "`recommended_time`, `entrance_fee`, `best_time`, `insider_tips`."
        )
    )

