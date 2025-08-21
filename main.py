import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from game_tools import roll_dice, generate_event
import chainlit as cl

load_dotenv()
client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"

)
model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)
config = RunConfig(model=model, tracing_disabled=True)

narrator_agent = Agent(
    name= "NarratorAgent",
    instructions="You narrate the advanture. Ask the player for choices",
    model=model
)

monster_agent = Agent(
    name= "MonsterAgent",
    instructions="You handle monster encounter using roll_dice and generate_event.",
   model=model,
   tools=[roll_dice, generate_event] 

)
item_agent = Agent(
    name="ItemAgent",
    instructions="You provide Reward or item to the player.",
    model=model

)
@cl.on_chat_start
async def start_chat():
    await cl.Message(content="🎮 Welcome to Fantasy Adventure Game! Do you enter the forest or turn back?").send()


@cl.on_message
async def handle_message(message: cl.Message):
    user_input = message.content

    # Step 1: Narration
    result1 = await Runner.run(narrator_agent, user_input, run_config=config)
    await cl.Message(content=f"📖 Story: {result1.final_output}").send()

    # Step 2: Monster encounter
    result2 = await Runner.run(monster_agent, "Start encounter", run_config=config)
    await cl.Message(content=f"👹 Encounter: {result2.final_output}").send()

    # Step 3: Reward
    result3 = await Runner.run(item_agent, "Give reward", run_config=config)
    await cl.Message(content=f"🎁 Reward: {result3.final_output}").send()

# From here part of simple agent start.......[Which starts after item agent and for chainlit we use above code of cl.on_message]

# def main():
#     print("\U0001F393 Welcome to Fantacy game\n")
#     choice = input("Do you enter the forest orture back? ->  ")

# result1= Runner.run_sync(narrator_agent, "choice", run_config=config) 
# print("\n Storyr:", result1.final_output)

# result2= Runner.run_sync(monster_agent, "Start encounter", run_config=config) 
# print("\n Encounter:", result2.final_output)

# result3= Runner.run_sync(item_agent, "Give reward", run_config=config) 
# print("\n REward:", result3.final_output)

# if __name__ == "__main__":
#     main()

