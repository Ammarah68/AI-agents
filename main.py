import os
from dotenv import load_dotenv
import chainlit as cl
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from travel_tools import get_flights, suggest_hotels

# 🔑 Load environment variables
load_dotenv()
client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# 🎯 Setup model + config
model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)
config = RunConfig(model=model, tracing_disabled=True)

# 🤖 Agents
destination_agent = Agent(
    name="DestinationAgent",
    instructions="You recommend travel destination based on user's mood",
    model=model
)

booking_agent = Agent(
    name="BookingAgent",
    instructions="You give flight and hotel info using tools",
    model=model,
    tools=[get_flights, suggest_hotels]   # keep simple tools
)

explore_agent = Agent(
    name="ExploreAgent",
    instructions="You suggest food and places to explore in the destination.",
    model=model
)

# 👋 Welcome message
@cl.on_chat_start
async def on_chat_start():
    await cl.Message(
        content="👋 Welcome to AI Travel Designer!\nTell me your travel mood (relaxation, adventure, romantic, etc.)"
    ).send()


#[simple travel agent from here]    

# def main():
#     print("\U0001F393 AI travel Designer\n")
#     mood = input("whats your travel mood(relaxation/adventure/etc? ->  ")

# result1= Runner.run_sync(destination_agent, "mood", run_config=config) 
# dest = result1.final_output.strip()
# print("\n Destination Suggested:", dest)

# result2= Runner.run_sync(booking_agent, dest, run_config=config) 
# print("\n Booking info:", result2.final_output)

# result3= Runner.run_sync(explor_agent, dest, run_config=config) 
# print("\n Explore Tips:", result3.final_output)



# if __name__ == "__main__":
#     main()


#[using chainlit from here]

# 💬 Message handler
@cl.on_message
async def on_message(message: cl.Message):
    mood = message.content

    # 1️⃣ Destination
    result1 = await Runner.run(destination_agent, mood, run_config=config)
    dest = result1.final_output.strip()
    await cl.Message(content=f"🌍 **Destination Suggested:** {dest}").send()

    # 2️⃣ Booking info
    result2 = await Runner.run(booking_agent, dest, run_config=config)
    await cl.Message(content=f"🏨 **Booking Info:** {result2.final_output}").send()

    # 3️⃣ Explore tips
    result3 = await Runner.run(explore_agent, dest, run_config=config)
    await cl.Message(content=f"🍽️ **Explore Tips:** {result3.final_output}").send()
