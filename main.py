import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig   # keep only this one
from roadmap_tool import get_career_roadmap
import chainlit as cl   # ✅ you forgot this

# Load API key
load_dotenv()
client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Model + Config
model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)
config = RunConfig(model=model, tracing_disabled=True)

# Agents
career_agent = Agent(
    name="CareerAgent",
    instructions="You ask about interest and a career field",
    model=model
)

skill_agent = Agent(
    name="SkillAgent",
    instructions="You share the roadmap using get_career_roadmap tool",
    model=model,
    tools=[get_career_roadmap]
)

job_agent = Agent(
    name="JobAgent",
    instructions="You suggest job title",
    model=model
)

# Chainlit handler
@cl.on_message
async def main(message: cl.Message):
    interest = message.content

    # Step 1 - Career Suggestion
    result1 = await Runner.run(career_agent, interest, run_config=config)
    field = result1.final_output.strip()
    await cl.Message(content=f"💡 Suggested Career: **{field}**").send()

    # Step 2 - Skills
    result2 = await Runner.run(skill_agent, field, run_config=config)
    await cl.Message(content=f"🛠 Required Skills:\n{result2.final_output}").send()

    # Step 3 - Jobs
    result3 = await Runner.run(job_agent, field, run_config=config)
    await cl.Message(content=f"💼 Possible Jobs:\n{result3.final_output}").send()



# def main():
#     print("\U0001F393 Career Mentor Agent\n")
#     interest = input("what are your interests? ->  ")

# result1= Runner.run_sync(career_agent, "interest", run_config=config) 
# field = result1.final_output.strip()
# print("\n Suggested career:", field)

# result2= Runner.run_sync(skill_agent, field, run_config=config) 
# print("\n Required Skill:", result2.final_output)

# result3= Runner.run_sync(job_agent, field, run_config=config) 
# print("\n Possible jobs:", result3.final_output)

# if __name__ == "__main__":
#     main()
