# from crew.assemble import run_travel_planner

# if __name__ == "__main__":
#     destination = input("Enter your travel destination: ")
#     travel_dates = input("Enter your travel dates (default: November 5th, 2025): ") or "Nov 5, 2025"
#     days = int(input("How many days is your trip? (default: 3): ") or "3")
#     preferences = input("Enter your travel preferences (default: Cultural & Museums, Food & Culinary): ") or "Cultural & Museums, Food & Culinary"
#     budget = input("Enter your budget (budget, moderate, luxury) (default: moderate): ") or "moderate"

#     print(f"\nGenerating travel plan for {destination}...\n")
#     result = run_travel_planner(destination, travel_dates, days, preferences, budget)
#     print("\n\n########################")
#     print(result)






# ------------------------------------------------------------------------------------------



# app.py
# import json
# from crew.assemble import run_travel_planner

# if __name__ == "__main__":
#     # --- Gather User Inputs ---
#     destination = input("Enter your travel destination: ")
#     travel_dates = input("Enter your travel dates (default: November 5th, 2025): ") or "Nov 5, 2025"
    
#     try:
#         days = int(input("How many days is your trip? (default: 3): ") or "3")
#         if days <= 0:
#             raise ValueError
#     except ValueError:
#         print("Invalid input for days. Using default value 3.")
#         days = 3

#     preferences = input(
#         "Enter your travel preferences (default: Cultural & Museums, Food & Culinary): "
#     ) or "Cultural & Museums, Food & Culinary"

#     budget = input("Enter your budget (budget, moderate, luxury) (default: moderate): ") or "moderate"
#     if budget not in ["budget", "moderate", "luxury"]:
#         print("Invalid budget input. Using default value 'moderate'.")
#         budget = "moderate"

#     # --- Run Travel Planner ---
#     print(f"\nGenerating travel plan for {destination}...\n")
#     result = run_travel_planner(destination, travel_dates, days, preferences, budget)

#     # --- Save JSON to file ---
#     output_filename = f"{destination.replace(' ', '_')}_travel_plan.json"
#     with open(output_filename, "w", encoding="utf-8") as f:
#         json.dump(result, f, indent=4, ensure_ascii=False)

#     # --- Pretty-print result to console ---
#     print("\n\n########################")
#     print(f"Travel plan saved to {output_filename}\n")
#     print(json.dumps(result, indent=4, ensure_ascii=False))





# ------------------------------------------------------------------------------------

import json
import os
from datetime import datetime
from crew.assemble import run_travel_planner

def crewoutput_to_dict(obj):
    """
    Recursively convert CrewOutput or nested objects to plain dicts/lists
    so they can be JSON serialized.
    """
    if isinstance(obj, dict):
        return {k: crewoutput_to_dict(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [crewoutput_to_dict(v) for v in obj]
    elif hasattr(obj, "__dict__"):
        return {k: crewoutput_to_dict(v) for k, v in obj.__dict__.items()}
    else:
        return obj

def get_user_inputs():
    """Collect and validate user inputs for travel planning."""
    print("🌍 Welcome to AI-Powered Multi-Agent Travel Planner!")
    print("=" * 55)

    destination = input("Enter your travel destination: ").strip()
    if not destination:
        destination = "Delhi"

    travel_dates = input("Enter your travel dates (default: November 5th, 2025): ").strip()
    if not travel_dates:
        travel_dates = "November 5th, 2025"

    try:
        days = int(input("How many days is your trip? (default: 3): ").strip() or 3)
        if days <= 0:
            days = 3
    except ValueError:
        days = 3

    preferences = input("Enter your travel preferences (default: Cultural & Museums, Food & Culinary): ").strip()
    if not preferences:
        preferences = "Cultural & Museums, Food & Culinary"

    budget = input("Enter your budget (budget, moderate, luxury) (default: moderate): ").strip().lower()
    if budget not in ["budget", "moderate", "luxury"]:
        budget = "moderate"

    return destination, travel_dates, days, preferences, budget

def display_inputs(destination, travel_dates, days, preferences, budget):
    """Display user inputs for confirmation."""
    print("\n" + "="*55)
    print("📋 TRAVEL PLAN SUMMARY")
    print("="*55)
    print(f"🏖️  Destination: {destination}")
    print(f"📅 Travel Dates: {travel_dates}")
    print(f"⏰ Duration: {days} days")
    print(f"🎯 Preferences: {preferences}")
    print(f"💰 Budget: {budget.title()}")
    print("="*55)

    confirm = input("\nProceed with planning? (y/n): ").lower()
    return confirm == 'y'

def save_travel_plan(result, destination):
    """Save travel plan to JSON file with safe CrewOutput conversion."""
    try:
        safe_destination = "".join(c for c in destination if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_destination = safe_destination.replace(' ', '_')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs("travel_plans", exist_ok=True)
        full_path = os.path.join("travel_plans", f"{safe_destination}_travel_plan_{timestamp}.json")

        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(crewoutput_to_dict(result), f, indent=4, ensure_ascii=False)

        print(f"✅ Travel plan saved to: {full_path}")
        return full_path

    except Exception as e:
        print(f"⚠️ Warning: Could not save to file: {str(e)}")
        return None

def display_travel_plan(result, destination):
    """Display the travel plan in a readable structured format."""
    from pprint import pprint
    
    print("\n" + "🎉" + "="*53 + "🎉")
    print(f"   TRAVEL PLAN FOR {destination.upper()}")
    print("🎉" + "="*53 + "🎉")

    try:
        data = crewoutput_to_dict(result)

        # Show general description if exists
        if 'description' in data:
            print("\n📝 Overview:\n" + "-"*40)
            print(data['description'])

        # Highlight attractions
        if 'highlight_attractions' in data:
            print("\n🏛️ Highlight Attractions:\n" + "-"*40)
            for attr in data['highlight_attractions']:
                print(f"• {attr}")

        # Daily summaries
        if 'daily_summary' in data:
            print("\n📅 Daily Itinerary:\n" + "-"*40)
            for day_info in data['daily_summary']:
                print(f"\nDay {day_info.get('day')}:")
                print(f"Summary: {day_info.get('summary')}")
                meals = day_info.get('meals', {})
                if meals:
                    print("Meals:")
                    for meal, detail in meals.items():
                        print(f"  {meal.title()}: {detail}")

        # Any other sections
        for key, value in data.items():
            if key not in ['description', 'highlight_attractions', 'daily_summary']:
                print(f"\n📝 {key.replace('_', ' ').title()}:\n" + "-"*40)
                pprint(value)

    except Exception as e:
        print(f"Error formatting output: {e}")
        print("Raw output:")
        pprint(result)

    print("\n" + "="*57)
    print("✅ Planning complete! Have an amazing trip! 🧳✈️")
    print("="*57)


def main():
    """Main function to run the travel planner."""
    try:
        destination, travel_dates, days, preferences, budget = get_user_inputs()

        if not display_inputs(destination, travel_dates, days, preferences, budget):
            print("❌ Planning cancelled by user.")
            return

        print(f"\n🤖 AI Agents are analyzing your trip to {destination}...")
        print("⏳ This may take a moment...\n")

        try:
            result = run_travel_planner(destination, travel_dates, days, preferences, budget)
        except Exception as e:
            print(f"❌ Error during travel planning: {str(e)}")
            return

        saved_file = save_travel_plan(result, destination)
        display_travel_plan(result, destination)

        if saved_file:
            print(f"\n📁 Your travel plan is also saved at: {saved_file}")

    except KeyboardInterrupt:
        print("\n\n❌ Planning interrupted by user. Goodbye! 👋")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
