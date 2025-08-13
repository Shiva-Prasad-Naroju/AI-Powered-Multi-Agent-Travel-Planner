# AI-Powered-Multi-Agent-Travel-Planner

**AI-Powered Multi-Agent Travel Planner** is a platform that generates personalized travel itineraries using multiple AI agents. 

It orchestrates agents for attractions, itinerary planning, dining, hotels, transport, and trip summaries to provide structured, optimized, and human-readable travel plans.

---

### 🚀 Features

- **Attractions Research Agent**: Finds the best attractions matching traveler preferences and budget.

- **Itinerary Planner Agent**: Creates day-by-day itineraries optimizing time, energy, and budget.

- **Hotels & Restaurants Agent**: Recommends suitable accommodations and local cuisine.

- **Transport Planner Agent**: Suggests the best modes and routes for travel between attractions.

- **Travel Summary Agent**: Generates human-readable summaries, tips, and highlights.

- **Fallback Search Tool**: Ensures structured responses even when primary sources lack data.

- **Structured JSON Output**: Saves travel plans in JSON format for easy consumption.format.

---

### Add your API keys in a .env file:
GEMINI_API_KEY=your_gemini_api_key

SERPER_API_KEY= your_serper_api_key

GEMINI_API_KEY= your_gemini_api_key

Then run : python app.py

---

### Follow the prompts to enter:

- Destination

- Travel dates

- Number of days

- Preferences (e.g., Food, Museums)

- Budget (budget / moderate / luxury)

---

### The app will:

- Orchestrate multiple AI agents.

- Generate structured travel plans.

- Save JSON output in travel_plans/.

- Display a clean, human-readable itinerary in the console.

---

### Output:
The output would look like:

🏖️ Destination: Delhi

📅 Travel Dates: Nov 5th, 2025

⏰ Duration: 3 days

🎯 Preferences: Cultural & Museums, Food & Culinary

💰 Budget: Moderate

#### 📝 Overview:

Explore Delhi’s rich cultural heritage within a moderate budget.

#### 🏛️ Highlight Attractions:

• Red Fort: Iconic Mughal fort.

• Qutub Minar: UNESCO World Heritage site.

• Chandni Chowk: Local food and markets.

#### 📅 Daily Itinerary:

Day 1:

Summary: Explore Red Fort and nearby markets.

Meals:

  Breakfast: Cafe XYZ
  
  Lunch: Restaurant ABC
  
  Dinner: Street food at Chandni Chowk

Day 2:
...

---

### 📝 Notes & Tips

- Ensure stable internet for API calls.

- The app may fail gracefully if LLM APIs are unreachable.

- JSON outputs can be used to integrate with other travel apps.

- Multi-agent orchestration allows flexible extensions like safety alerts or weather planning.

---

Thank your for exploring this project.
