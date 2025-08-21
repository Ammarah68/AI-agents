from agents import function_tool
import random

@function_tool
def roll_dice() -> str:
    return f" You rolled a {random.randiant(1, 6)}!"

@function_tool
def generate_event() -> str: 
    events = [
        "You encounterna dragon!",
        "You found a treasure chest",
        "You fell into a trap!",
        "You met a mysterious wizard."
    ]
    return random.choice(events)





