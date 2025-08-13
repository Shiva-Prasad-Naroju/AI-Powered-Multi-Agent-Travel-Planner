# from crewai_tools import tool
# import requests

# @tool
# def FallbackSearchTool(query: str) -> str:
#     """
#     Performs a fallback web search using DuckDuckGo API or similar
#     when primary tools fail.
#     """
#     url = f"https://api.duckduckgo.com/?q={query}&format=json"
#     response = requests.get(url)
#     data = response.json()
    
#     # Extract the abstract or related topics
#     if "AbstractText" in data and data["AbstractText"]:
#         return data["AbstractText"]
#     elif "RelatedTopics" in data and data["RelatedTopics"]:
#         return data["RelatedTopics"][0].get("Text", "No results found.")
#     return "No results found."






# -----------------------------------------------------------------------------------
# 2nd worked but error getting:
import requests
class FallbackSearchTool:
    """
    Fallback search tool for CrewAI v0.60.0.
    Accepts a query string and returns structured JSON with:
    name, description, link, coordinates.
    """

    name = "FallbackSearchTool"
    description = "Searches for attractions using DuckDuckGo and OpenStreetMap"

    def __call__(self, query: str) -> dict:
        results = []

        # 1️⃣ DuckDuckGo Instant Answer API
        ddg_url = f"https://api.duckduckgo.com/?q={query}&format=json&no_redirect=1&no_html=1"
        ddg_response = requests.get(ddg_url, timeout=10)
        ddg_data = ddg_response.json()

        if ddg_data.get("AbstractText"):
            results.append({
                "name": query.title(),
                "description": ddg_data.get("AbstractText"),
                "link": ddg_data.get("AbstractURL", ""),
                "coordinates": None
            })
        elif "RelatedTopics" in ddg_data:
            for topic in ddg_data["RelatedTopics"][:5]:
                if "Text" in topic:
                    results.append({
                        "name": topic["Text"].split(" - ")[0],
                        "description": topic["Text"],
                        "link": topic.get("FirstURL", ""),
                        "coordinates": None
                    })

        # 2️⃣ OpenStreetMap coordinates
        for item in results:
            try:
                osm_url = f"https://nominatim.openstreetmap.org/search?format=json&q={item['name']}"
                osm_resp = requests.get(osm_url, headers={"User-Agent": "FallbackSearchTool"}, timeout=10)
                osm_data = osm_resp.json()
                if osm_data:
                    item["coordinates"] = {
                        "lat": osm_data[0]["lat"],
                        "lon": osm_data[0]["lon"]
                    }
            except Exception:
                item["coordinates"] = None

        return {
            "query": query,
            "results": results
        }


# -----------------------------------------------------------------------------
