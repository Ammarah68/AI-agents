from agents import function_tool

@function_tool
def get_career_roadmap(field: str) -> str:
    maps = {
      "software ": "Learn Python"
    }
    return maps.get(field.lower(), "no roadmap found ") 