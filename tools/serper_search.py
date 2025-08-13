import requests
from crewai.tools import tools
import os
from dotenv import load_dotenv

load_dotenv(override=True)
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# @tool
@tools.tool
def serper_search(query: str) -> str:
    """Search Google using Serper.dev and return summarized top result links."""
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    data = {"q": query, "num": 3}
    response = requests.post("https://google.serper.dev/search", headers=headers, json=data)

    if response.status_code == 200:
        results = response.json()
        output = []
        for item in results.get("organic", []):
            output.append(f"{item.get('title')} - {item.get('link')}")
        return "\n".join(output)
    else:
        return f"Error from Serper API: {response.status_code} - {response.text}"
