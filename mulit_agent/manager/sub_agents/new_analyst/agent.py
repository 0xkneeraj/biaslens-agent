from google.adk.agents import Agent
from google.adk.tools import google_search

news_analyst = Agent(
    name="news_analyst",
    model='gemini-2.0-flash-001',
    description="An agent that provides insights and analysis on various topics.",
    instruction="""
    You are a helpfull assistant that can analyze new articles and provide a summary of the news.

    when asked about news, you should use the google_search tool to search for the news articles related to the topic.

    If the user ask for news using a relative time, you should use the get_current_time tool to get the current time and then search for news articles related to the topic.
""",
    tools=[google_search],
)