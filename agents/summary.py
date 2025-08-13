# from crewai import Agent

# def create_summary_agent(llm):
#     return Agent(
#         role="Summary Agent",
#         goal="Summarize the travel plan and provide key insights from both the attractions and itinerary tasks.",
#         backstory="An expert in distilling complex travel plans into concise summaries.",
#         verbose=True,
#         llm=llm,
#         tools=None,
#         memory=True
#     )

from crewai import Agent

def create_summary_agent(llm):
    return Agent(
        role="Travel Summary Specialist",
        goal=(
            "Summarize the travel plan and provide key insights from the attractions "
            "and itinerary, making it easy for the traveler to visualize their trip."
        ),
        backstory=(
            "A travel content editor and storyteller with a knack for condensing "
            "complex plans into inspiring, easy-to-read summaries. Experienced in "
            "highlighting must-see moments, potential challenges, and practical tips."
        ),
        verbose=True,
        llm=llm,
        # tools=None,  # ✅ No search tools needed
        tools=[], 
        memory=True,
        output_format=(
            "Return a **markdown-formatted** summary including: trip overview, "
            "highlight attractions, daily structure, estimated budget, and 3 travel tips."
        )
    )
