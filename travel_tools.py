from agents import function_tool
@function_tool
def get_flights(destination:str) -> str:
    return f"Fligth found to {destination}: PKR 45000 - PKR 70,000"

@function_tool
def suggest_hotels(destination: str) -> str:
    return f"Hotels in {destination}: Pearl Continental, Marriot, local guest."