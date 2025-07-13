from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from .tools.tools import get_current_time
from .sub_agents.stock_analyst.agent import stock_analyst
from .sub_agents.funny_nerd.agent import funny_nerd
from .sub_agents.new_analyst.agent import news_analyst

root_agent = Agent(
    name="Manager",
    model='gemini-2.0-flash-001',
    description="An agent that manages other agents and delegates tasks to them.",
    instruction="""You are a manager agent that responsibile for overseeing the work of other agents.

    Always delegate the task to the appropriate agent. Use your best judgement to determine which agent to delegate to.

    You are responsible for delegating tasks to the following agents:
    - stock_analyst
    - funny_nerd

    You also have access to the following tools:
    - news_analyst
    - get_current_time
    """,
    sub_agents=[stock_analyst, funny_nerd],
    tools=[ 
        AgentTool(news_analyst),
        get_current_time
        ]
)