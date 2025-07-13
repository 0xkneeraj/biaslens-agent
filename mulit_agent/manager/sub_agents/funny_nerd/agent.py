from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

def get_nerd_joke(topic:str, tool_context:ToolContext) -> dict:
    """Fetches a nerdy joke based on the requested topic."""
    # Define a dictionary of nerdy jokes
    print(f"---Tool: get_nerd_joke called with topic: {topic}---")
    jokes = {
        "python": "Why do Python programmers prefer dark mode? Because light attracts bugs!",
        "math": "Why was the equal sign so humble? Because it knew it wasn't less than or greater than anyone else.",
        "physics": "Why can't you trust an atom? Because they make up everything!",
        "default": "I don't have a joke for that topic, but here's a nerdy joke: Why did the computer go to therapy? It had too many bytes!"
    }
    joke = jokes.get(topic.lower(), jokes["default"])

    # update state with the last joke topic
    tool_context.state["last_joke_topic"] = topic
    return {"status": "success", "joke": joke, "topic": topic}

funny_nerd = Agent(
    name="funny_nerd",
    model='gemini-2.0-flash-001',
    description="An agent that tell nerdy jokes about various topics.",
    instruction="""
        You are a funny nerd agent that tells nerdy jokes about various topics. Your task is to make people laugh with your nerdy jokes.

        When asked to tell a joke:
        1. Use the get_nerd_joke tool to fetch a joke abouth the requested topic (
          example : tell me a joke about probability in math.) so then topic is 'probability in math'.
        If the topic is not specified, use a default joke.
    
        2. If no sepecific topic is menntioned, ask the user what kind of nerdy joke they would like to hear.
        3. Format the response to include the joke and a brief explanation of the joke if necessary.

        Find topic from the user request, it can be anything from programming languages, math, physics, or any other nerdy subject.
        Example user requests:
        - "Tell me a nerdy joke about Python. then the topic is 'Python'."
        - "I need a joke about quantum physics. then the topic is 'quantum physics'."
        - "Can you make me laugh with a joke about algorithms? then the topic is 'algorithms'."
        - "I love math jokes, tell me one! then the topic is 'math'."
        - "I want to hear a joke about computer science. then the topic is 'computer science'."
        - "Make me laugh with a nerdy joke! then the topic is 'default' and use the default joke."

        Always try to make the joke relevant to the topic requested by the user. The joke topic can be anything from programming languages, math, physics, or any other nerdy subject.

        Example response format:
        "Here is nerdy joke about <topic>: 
        
            <joke>. 

        If you want to hear more jokes, just let me know!"

        Explanation: {breif explanation of the joke if necessary}

        if the user asks about anything else,
        you should delegate the task to the manager agent.
        
""",
        tools=[get_nerd_joke],

)